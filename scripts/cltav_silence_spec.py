"""Specification-level instance pairing for the successor no-response marker.

This is not a protocol engine, timeout implementation, or state estimator.
Witnesses exist so a response for key B cannot hide silence of unmatched A.
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
    unique-key pairing is ERROR, not IUT FAIL.
    """
    if candidate.index <= trigger.index:
        return "NONE"
    if candidate.req != trigger.req or candidate.key != trigger.key:
        return "NONE"
    if candidate.kind not in {EventKind.RESP, EventKind.CANCEL, EventKind.SUPERSEDE}:
        return "NONE"
    same = tuple(ev for ev in active_same_key if ev.key == trigger.key)
    if obligation.pairing is PairingPolicy.UNIQUE_KEY:
        if len(same) > 1 and not obligation.concurrent_same_key:
            return "ERROR"
        if len(same) > 1 and obligation.concurrent_same_key:
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


def instance_disposition(
    obligation: TimedObligation,
    trace: tuple[Event, ...],
    t_H: float,
) -> Disposition:
    """Active-instance state already includes matching, cancel, and supersede."""
    trig = obligation.trigger
    events = tuple(sorted(trace, key=lambda ev: ev.index))
    active: dict[str, list[Event]] = {}
    dispositions: dict[int, Disposition] = {}

    def close(target: Event, disp: Disposition) -> None:
        dispositions[target.index] = disp
        bucket = active.get(target.key, [])
        active[target.key] = [item for item in bucket if item.index != target.index]

    for ev in events:
        if ev.time > t_H:
            break
        if ev.req != trig.req:
            continue
        if ev.kind is EventKind.TRIG:
            same = list(active.get(ev.key, []))
            if (
                same
                and obligation.pairing is PairingPolicy.UNIQUE_KEY
                and not obligation.concurrent_same_key
            ):
                for old in same:
                    close(old, Disposition.SUPERSEDED)
            active.setdefault(ev.key, []).append(ev)
            dispositions[ev.index] = Disposition.ACTIVE
            continue
        same = tuple(active.get(ev.key, []))
        verdict = match_r(obligation, trig if ev.key == trig.key else (same[0] if same else trig), ev, same)
        if obligation.pairing is PairingPolicy.UNIQUE_KEY and len(same) > 1:
            for old in same:
                dispositions[old.index] = Disposition.ERROR
            active[ev.key] = []
            continue
        target = None
        for item in same:
            if match_r(obligation, item, ev, same) == "MATCH":
                target = item
                break
        if verdict == "ERROR" or (
            obligation.pairing is PairingPolicy.UNIQUE_KEY
            and obligation.concurrent_same_key
            and len(same) > 1
            and ev.key == trig.key
        ):
            for old in same:
                dispositions[old.index] = Disposition.ERROR
            active[ev.key] = []
            continue
        if target is None:
            continue
        if ev.kind is EventKind.RESP:
            close(target, Disposition.DISCHARGED)
        elif ev.kind is EventKind.CANCEL:
            close(target, Disposition.CANCELLED)
        elif ev.kind is EventKind.SUPERSEDE:
            close(target, Disposition.SUPERSEDED)
            successor = Event(ev.index, ev.time, EventKind.TRIG, ev.key, ev.req)
            active.setdefault(ev.key, []).append(successor)
            dispositions[successor.index] = Disposition.ACTIVE
    return dispositions.get(trig.index, Disposition.ACTIVE)


def no_response(
    obligation: TimedObligation,
    trace: tuple[Event, ...],
    t_H: float,
) -> bool | Disposition:
    """Successor marker: expired still-active instance. No global Resp_r conjunct."""
    disp = instance_disposition(obligation, trace, t_H)
    if disp is Disposition.ERROR:
        return Disposition.ERROR
    if disp is not Disposition.ACTIVE:
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
    active = instance_disposition(obligation, trace, t_H) is Disposition.ACTIVE
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
    """Bounded-response schematic: a Match_r pair whose delay lies in I_r."""
    trig = obligation.trigger
    same = (trig,)
    for ev in sorted(trace, key=lambda item: item.index):
        if ev.kind is not EventKind.RESP:
            continue
        if match_r(obligation, trig, ev, same) != "MATCH":
            continue
        delta = ev.time - trig.time
        if delta < lower_bound:
            continue
        if expired(delta, obligation.upper_bound, obligation.upper_closed):
            continue
        return True
    return False
