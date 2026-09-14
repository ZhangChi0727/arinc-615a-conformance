"""First-version CL-TAV session loop specification.

This is a bounded walk-through interpreter for DD-029 resource admission,
charging, ERROR history and stop classification. It is not a verification
engine, scheduler or state estimator.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ResourceMode(str, Enum):
    BUDGET = "BUDGET"
    ROUNDS = "ROUNDS"


class ActionKind(str, Enum):
    TEST = "TEST"
    PREP = "PREP"
    RECOVER = "RECOVER"


class QStatus(str, Enum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"


class ErrorKind(str, Enum):
    NOT_SENT = "NOT_SENT"
    UNKNOWN_EFFECT = "UNKNOWN_EFFECT"


@dataclass(frozen=True)
class Action:
    id: str
    kind: ActionKind
    cost: float
    enabled_at: frozenset[str]
    worst_remaining: int | None = None
    next_q: str | None = None


@dataclass
class Session:
    mode: ResourceMode
    cmin: float
    Hk: set[str]
    q: str
    q_status: QStatus = QStatus.KNOWN
    remaining_B: float | None = None
    B: float | None = None
    Kmax: int | None = None
    rounds: int = 0
    retries: int = 0
    retry_cap: int = 1
    stop: str | None = None
    charges: list[tuple[str, float]] = field(default_factory=list)
    history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.cmin <= 0:
            raise ValueError("cmin must be positive")
        if self.mode is ResourceMode.BUDGET:
            if self.B is None or self.remaining_B is None:
                raise ValueError("BUDGET mode requires finite B and remaining_B")
            self.Kmax = None
        elif self.mode is ResourceMode.ROUNDS:
            if self.Kmax is None:
                raise ValueError("ROUNDS mode requires finite Kmax")
            self.B = None
            self.remaining_B = None
        else:
            raise ValueError("resource mode must be BUDGET or ROUNDS, not both")


def remaining_ok(session: Session, cost: float) -> bool:
    if cost < session.cmin:
        return False
    if session.mode is ResourceMode.BUDGET:
        assert session.remaining_B is not None
        return cost <= session.remaining_B
    assert session.Kmax is not None
    return session.rounds < session.Kmax


def charge(session: Session, action: Action) -> None:
    cost = action.cost
    if not remaining_ok(session, cost):
        raise RuntimeError("cannot charge an action that was not admitted")
    if session.mode is ResourceMode.BUDGET:
        assert session.remaining_B is not None
        session.remaining_B -= cost
    else:
        session.rounds += 1
    session.charges.append((action.id, cost))


def admissible(session: Session, library: list[Action]) -> list[Action]:
    if session.stop:
        return []
    out: list[Action] = []
    for action in library:
        if action.cost < session.cmin:
            continue
        if not remaining_ok(session, action.cost):
            continue
        if session.q_status is QStatus.UNKNOWN:
            if action.kind is ActionKind.RECOVER:
                out.append(action)
            continue
        if session.q not in action.enabled_at:
            continue
        if action.kind is ActionKind.RECOVER:
            continue
        out.append(action)
    return out


def select(actions: list[Action]) -> Action | None:
    if not actions:
        return None
    tests = [action for action in actions if action.kind is ActionKind.TEST]
    if tests:
        return sorted(tests, key=lambda item: (item.worst_remaining, item.cost, item.id))[0]
    preps = [action for action in actions if action.kind is ActionKind.PREP]
    if preps:
        return sorted(preps, key=lambda item: (item.cost, item.id))[0]
    recovers = [action for action in actions if action.kind is ActionKind.RECOVER]
    return sorted(recovers, key=lambda item: (item.cost, item.id))[0]


def classify_empty(session: Session, library: list[Action]) -> str:
    if session.q_status is QStatus.UNKNOWN:
        return "Stop-Error"
    enabled = [action for action in library if session.q in action.enabled_at]
    distinguisher = [
        action
        for action in enabled
        if action.kind is ActionKind.TEST
        and action.worst_remaining is not None
        and action.worst_remaining < len(session.Hk)
    ]
    preps = [action for action in enabled if action.kind is ActionKind.PREP]
    if distinguisher or preps:
        return "Stop-Budget"
    return "Stop-NoDistinguisher"


def admit_or_stop(session: Session, library: list[Action]) -> Action | None:
    actions = admissible(session, library)
    chosen = select(actions)
    if chosen is not None:
        return chosen
    session.stop = classify_empty(session, library)
    return None


def apply_valid_observation(session: Session, action: Action, remaining: set[str]) -> None:
    session.Hk = set(remaining)
    if action.next_q:
        session.q = action.next_q
    session.q_status = QStatus.KNOWN
    session.history.append(f"valid:{action.id}")
    _stop_after_update(session)


def apply_error(session: Session, action: Action, kind: ErrorKind) -> None:
    session.history.append(f"ERROR:{kind.value}:{action.id}")
    session.retries += 1
    if kind is ErrorKind.UNKNOWN_EFFECT:
        session.q_status = QStatus.UNKNOWN
    if session.retries >= session.retry_cap:
        session.stop = "Stop-Error"


def _stop_after_update(session: Session) -> None:
    if session.stop:
        return
    if not session.Hk:
        session.stop = "Stop-Empty"
        return
    if len(session.Hk) == 1:
        session.stop = "Stop-Singleton"
        return
    if session.mode is ResourceMode.BUDGET:
        assert session.remaining_B is not None
        if session.remaining_B < session.cmin:
            session.stop = "Stop-Budget"
    elif session.rounds >= (session.Kmax or 0):
        session.stop = "Stop-Budget"


def step(
    session: Session,
    library: list[Action],
    *,
    observation: set[str] | None = None,
    error: ErrorKind | None = None,
) -> Action | None:
    """Admit, execute one action, charge once, then update or ERROR."""
    if session.stop:
        return None
    chosen = admit_or_stop(session, library)
    if chosen is None:
        return None
    charge(session, chosen)
    if error is not None:
        apply_error(session, chosen, error)
        if session.stop is None and not admissible(session, library):
            session.stop = classify_empty(session, library)
        return chosen
    if observation is None:
        raise ValueError("valid execution requires an observation remaining-set")
    apply_valid_observation(session, chosen, observation)
    return chosen
