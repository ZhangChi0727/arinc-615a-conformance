"""Specification-level instance pairing for the successor no-response marker.

This is not a protocol engine, timeout implementation, or state estimator.
Witnesses exist so a response for key B cannot hide silence of unmatched A.
T2 and silence consume the same trace-replay ownership.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EventKind(str, Enum):
    TRIG = "TRIG"
    RESP = "RESP"
    CANCEL = "CANCEL"
    SUPERSEDE = "SUPERSEDE"


class PairingPolicy(str, Enum):
    UNIQUE_KEY = "UNIQUE-KEY"
    FIFO = "FIFO"
    MOST_RECENT = "MOST-RECENT"


class Disposition(str, Enum):
    ACTIVE = "ACTIVE"
    DISCHARGED = "DISCHARGED"
    CANCELLED = "CANCELLED"
    SUPERSEDED = "SUPERSEDED"
    ERROR = "ERROR"


@dataclass(frozen=True)
class Event:
    index: int
    time: float
    kind: EventKind
    key: str
    req: str = "r"


@dataclass(frozen=True)
class TimedObligation:
    trigger: Event
    upper_bound: float
    upper_closed: bool = True
    pairing: PairingPolicy = PairingPolicy.UNIQUE_KEY
    concurrent_same_key: bool = False


@dataclass(frozen=True)
class InstanceOutcome:
    """Disposition plus the event that closed the instance, if any."""

    disposition: Disposition
    closer: Event | None = None


def expired(delta: float, upper_bound: float, upper_closed: bool) -> bool:
    if upper_closed:
        return delta > upper_bound
    return delta >= upper_bound


def match_r(
    obligation: TimedObligation,
    trigger: Event,
    candidate: Event,
    active_same_key: tuple[Event, ...],
) -> str:
    """Instance matcher: response type, correlation key, pairing policy, and j > i.

    Equal timestamps are allowed when the candidate index is later. Ambiguous
    unique-key pairing is ERROR, not IUT FAIL. ``active_same_key`` must be the
    live active set from trace replay, not a fabricated singleton.
    """
    if candidate.index <= trigger.index:
        return "NONE"
    if candidate.req != trigger.req or candidate.key != trigger.key:
        return "NONE"
    if candidate.kind not in {EventKind.RESP, EventKind.CANCEL, EventKind.SUPERSEDE}:
        return "NONE"
    same = tuple(ev for ev in active_same_key if ev.key == trigger.key)
    if obligation.pairing is PairingPolicy.UNIQUE_KEY:
        if len(same) > 1:
            return "ERROR"
        if len(same) == 1 and same[0].index == trigger.index:
            return "MATCH"
        return "NONE"
    if not same:
        return "NONE"
    chosen = (
        min(same, key=lambda ev: ev.index)
        if obligation.pairing is PairingPolicy.FIFO
        else max(same, key=lambda ev: ev.index)
    )
    return "MATCH" if chosen.index == trigger.index else "NONE"


def replay_instances(
    obligation: TimedObligation,
    trace: tuple[Event, ...],
    t_H: float | None = None,
) -> dict[int, InstanceOutcome]:
    """Shared ownership replay for T2 and silence. Not a protocol engine."""
    events = tuple(sorted(trace, key=lambda ev: ev.index))
    active: dict[str, list[Event]] = {}
    outcomes: dict[int, InstanceOutcome] = {}

    def close(target: Event, disp: Disposition, closer: Event) -> None:
        outcomes[target.index] = InstanceOutcome(disp, closer)
        bucket = active.get(target.key, [])
        active[target.key] = [item for item in bucket if item.index != target.index]

    for ev in events:
        if t_H is not None and ev.time > t_H:
            break
        if ev.req != obligation.trigger.req:
            continue
        if ev.kind is EventKind.TRIG:
            same = list(active.get(ev.key, []))
            if (
                same
                and obligation.pairing is PairingPolicy.UNIQUE_KEY
                and not obligation.concurrent_same_key
            ):
                for old in same:
                    close(old, Disposition.SUPERSEDED, ev)
            active.setdefault(ev.key, []).append(ev)
            outcomes[ev.index] = InstanceOutcome(Disposition.ACTIVE)
            continue
        same = tuple(active.get(ev.key, []))
        owner: Event | None = None
        ambiguous = False
        for item in same:
            verdict = match_r(obligation, item, ev, same)
            if verdict == "ERROR":
                ambiguous = True
                break
            if verdict == "MATCH":
                owner = item
        if ambiguous:
            for old in same:
                outcomes[old.index] = InstanceOutcome(Disposition.ERROR, ev)
            active[ev.key] = []
            continue
        if owner is None:
            continue
        if ev.kind is EventKind.RESP:
            close(owner, Disposition.DISCHARGED, ev)
        elif ev.kind is EventKind.CANCEL:
            close(owner, Disposition.CANCELLED, ev)
        elif ev.kind is EventKind.SUPERSEDE:
            close(owner, Disposition.SUPERSEDED, ev)
            successor = Event(ev.index, ev.time, EventKind.TRIG, ev.key, ev.req)
            active.setdefault(ev.key, []).append(successor)
            outcomes[successor.index] = InstanceOutcome(Disposition.ACTIVE)
    return outcomes


def instance_outcome(
    obligation: TimedObligation,
    trace: tuple[Event, ...],
    t_H: float | None = None,
) -> InstanceOutcome:
    outcomes = replay_instances(obligation, trace, t_H)
    return outcomes.get(obligation.trigger.index, InstanceOutcome(Disposition.ACTIVE))


def instance_disposition(
    obligation: TimedObligation,
    trace: tuple[Event, ...],
    t_H: float,
) -> Disposition:
    """Active-instance state already includes matching, cancel, and supersede."""
    return instance_outcome(obligation, trace, t_H).disposition


def paired_response(
    obligation: TimedObligation,
    trace: tuple[Event, ...],
    t_H: float | None = None,
) -> Event | None:
    rec = instance_outcome(obligation, trace, t_H)
    if rec.disposition is not Disposition.DISCHARGED:
        return None
    closer = rec.closer
    if closer is None or closer.kind is not EventKind.RESP:
        return None
    return closer


def no_response(
    obligation: TimedObligation,
    trace: tuple[Event, ...],
    t_H: float,
) -> bool | Disposition:
    """Successor marker: expired still-active instance. No global Resp_r conjunct."""
    rec = instance_outcome(obligation, trace, t_H)
    if rec.disposition is Disposition.ERROR:
        return Disposition.ERROR
    if rec.disposition is not Disposition.ACTIVE:
        return False
    trig = obligation.trigger
    return expired(t_H - trig.time, obligation.upper_bound, obligation.upper_closed)


def displayed_global_resp_no_response(
    obligation: TimedObligation,
    trace: tuple[Event, ...],
    t_H: float,
) -> bool:
    """Defective displayed formula: any later Resp_r event suppresses the marker."""
    trig = obligation.trigger
    rec = instance_outcome(obligation, trace, t_H)
    active = rec.disposition is Disposition.ACTIVE
    late = expired(t_H - trig.time, obligation.upper_bound, obligation.upper_closed)
    has_any_resp = any(
        ev.kind is EventKind.RESP
        and ev.req == trig.req
        and ev.index > trig.index
        and trig.time < ev.time <= t_H
        for ev in trace
    )
    return bool(active and late and not has_any_resp)


def t2_holds(obligation: TimedObligation, trace: tuple[Event, ...], lower_bound: float = 0.0) -> bool:
    """Bounded-response schematic using the same ownership replay as silence.

    Returns a bool only. Ambiguous pairing, cancellation and supersession are
    not T2 success. A late correctly paired response discharges but is not timely.
    """
    rec = instance_outcome(obligation, trace, t_H=None)
    if rec.disposition is Disposition.ERROR:
        return False
    closer = rec.closer
    if rec.disposition is not Disposition.DISCHARGED or closer is None or closer.kind is not EventKind.RESP:
        return False
    delta = closer.time - obligation.trigger.time
    if delta < lower_bound:
        return False
    if expired(delta, obligation.upper_bound, obligation.upper_closed):
        return False
    return True
