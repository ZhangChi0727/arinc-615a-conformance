"""First-version CL-TAV session loop specification.

This is a bounded walk-through interpreter for DD-029 resource admission,
charging, ERROR history and stop classification. It is not a verification
engine, scheduler or state estimator.

Resource quantities are integer units. Infinite, NaN and non-integer round
caps are not legal witnesses for the finite-termination argument.
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


# Update-path arbitration used by FIG-CL-TAV-05, FIG-CL-TAV-07 and this walker.
# First matching class wins. Continue-to-Admit is the residual, not a stop.
UPDATE_STOP_PRIORITY = (
    "Stop-Empty",
    "Stop-Singleton",
    "Stop-645",
    "Stop-Equivalent",
    "Stop-Budget",
)

# Admit/Select table shared with FIG-CL-TAV-05/07. A is resource-admissible;
# S is the finally selectable subset. A nonempty does not imply Execute.
ADMIT_SELECT_TABLE = {
    "A1": "S nonempty: execute the chosen action",
    "A2": "KNOWN: a strictly-reducing TEST or Prep exists but is unaffordable: Stop-Budget",
    "A3": "KNOWN: no strictly-reducing TEST and no Prep: Stop-NoDistinguisher",
    "A4": "UNKNOWN: Recover not eligible: Stop-Error",
    "A5": "UNKNOWN: Recover eligible but unaffordable: Stop-Budget",
}


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _require_nonneg_int(value: object, name: str) -> int:
    if not _is_int(value) or int(value) < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return int(value)


def _require_pos_int(value: object, name: str) -> int:
    if not _is_int(value) or int(value) < 1:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


@dataclass(frozen=True)
class Action:
    id: str
    kind: ActionKind
    cost: int
    enabled_at: frozenset[str]
    worst_remaining: int | None = None
    next_q: str | None = None
    obs_classes: tuple[frozenset[str], ...] = ()
    recover_when_unknown: bool = False

    def __post_init__(self) -> None:
        _require_nonneg_int(self.cost, "action cost")
        if self.worst_remaining is not None:
            _require_nonneg_int(self.worst_remaining, "worst_remaining")
        if self.kind is ActionKind.RECOVER and self.recover_when_unknown and not self.next_q:
            raise ValueError("eligible Recover must declare a recovery target next_q")


@dataclass
class Session:
    mode: ResourceMode
    cmin: int
    Hk: set[str]
    q: str
    q_status: QStatus = QStatus.KNOWN
    remaining_B: int | None = None
    B: int | None = None
    Kmax: int | None = None
    rounds: int = 0
    retries: int = 0
    retry_cap: int = 1
    stop: str | None = None
    charges: list[tuple[str, int]] = field(default_factory=list)
    history: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.cmin = _require_pos_int(self.cmin, "cmin")
        self.rounds = _require_nonneg_int(self.rounds, "rounds")
        self.retries = _require_nonneg_int(self.retries, "retries")
        self.retry_cap = _require_pos_int(self.retry_cap, "retry_cap")
        if self.mode is ResourceMode.BUDGET:
            if self.B is None or self.remaining_B is None:
                raise ValueError("BUDGET mode requires finite B and remaining_B")
            self.B = _require_nonneg_int(self.B, "B")
            self.remaining_B = _require_nonneg_int(self.remaining_B, "remaining_B")
            if self.remaining_B > self.B:
                raise ValueError("remaining_B must not exceed B")
            self.Kmax = None
        elif self.mode is ResourceMode.ROUNDS:
            if self.Kmax is None:
                raise ValueError("ROUNDS mode requires finite Kmax")
            self.Kmax = _require_nonneg_int(self.Kmax, "Kmax")
            self.B = None
            self.remaining_B = None
        else:
            raise ValueError("resource mode must be BUDGET or ROUNDS, not both")


def remaining_ok(session: Session, cost: int) -> bool:
    if not _is_int(cost) or cost < session.cmin:
        return False
    if session.mode is ResourceMode.BUDGET:
        assert session.remaining_B is not None
        return cost <= session.remaining_B
    assert session.Kmax is not None
    return session.rounds < session.Kmax


def resource_exhausted(session: Session) -> bool:
    if session.mode is ResourceMode.BUDGET:
        assert session.remaining_B is not None
        return session.remaining_B < session.cmin
    assert session.Kmax is not None
    return session.rounds >= session.Kmax


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


def recover_eligible(action: Action) -> bool:
    """Unknown-effect recovery is an explicit eligibility, not enabled_at(q)."""
    return (
        action.kind is ActionKind.RECOVER
        and action.recover_when_unknown is True
        and isinstance(action.next_q, str)
        and action.next_q != ""
    )


def remaining_after(action: Action, hk: set[str], obs: frozenset[str]) -> set[str]:
    return set(hk) & set(obs)


def current_valid_classes(action: Action, hk: set[str]) -> tuple[set[str], ...]:
    """Project declared classes onto Hk and keep currently realizable nonempty sets.

    Empty intersections belong to already-excluded hypotheses or are out-of-model
    at selection time. They are not extra score classes. A later executed
    observation that empties Hk is still Stop-Empty.
    """
    if not action.obs_classes:
        return ()
    return tuple(
        remaining
        for obs in action.obs_classes
        if (remaining := remaining_after(action, hk, obs))
    )


def can_strictly_reduce(action: Action, hk: set[str]) -> bool:
    """True iff some *currently valid* nonempty class leaves a proper subset of Hk.

    Require 0 < |survivors| < |Hk|. s(t)=|Hk| is worst-case non-shrinkage, not
    'no diagnostic value'. Classes that project to empty are not distinguishing
    value. A test with obs_classes but no current valid class is a prediction
    gap, not a score-0 perfect test.
    """
    if action.kind is not ActionKind.TEST or not hk:
        return False
    if action.obs_classes:
        valid = current_valid_classes(action, hk)
        if not valid:
            return False
        return any(len(survivors) < len(hk) for survivors in valid)
    if action.worst_remaining is not None:
        return 0 < action.worst_remaining < len(hk)
    return False


def worst_remaining_count(action: Action, hk: set[str]) -> int:
    valid = current_valid_classes(action, hk)
    if valid:
        return max(len(survivors) for survivors in valid)
    if action.obs_classes:
        return len(hk)
    if action.worst_remaining is not None:
        return action.worst_remaining
    return len(hk)


def admissible(session: Session, library: list[Action]) -> list[Action]:
    if session.stop:
        return []
    out: list[Action] = []
    for action in library:
        if not remaining_ok(session, action.cost):
            continue
        if session.q_status is QStatus.UNKNOWN:
            if recover_eligible(action):
                out.append(action)
            continue
        if action.kind is ActionKind.RECOVER:
            continue
        if session.q not in action.enabled_at:
            continue
        out.append(action)
    return out


def select(session: Session, actions: list[Action]) -> Action | None:
    if not actions:
        return None
    tests = [action for action in actions if can_strictly_reduce(action, session.Hk)]
    if tests:
        return sorted(
            tests,
            key=lambda item: (worst_remaining_count(item, session.Hk), item.cost, item.id),
        )[0]
    preps = [action for action in actions if action.kind is ActionKind.PREP]
    if preps:
        return sorted(preps, key=lambda item: (item.cost, item.id))[0]
    recovers = [action for action in actions if recover_eligible(action)]
    if not recovers:
        return None
    return sorted(recovers, key=lambda item: (item.cost, item.id))[0]


def classify_empty(session: Session, library: list[Action]) -> str:
    """Admit table A2–A5 when selectable S is empty, even if A is not."""
    if session.q_status is QStatus.UNKNOWN:
        eligible = [action for action in library if recover_eligible(action)]
        if eligible:
            return "Stop-Budget"
        return "Stop-Error"
    enabled = [
        action
        for action in library
        if action.kind is not ActionKind.RECOVER and session.q in action.enabled_at
    ]
    distinguisher = [action for action in enabled if can_strictly_reduce(action, session.Hk)]
    preps = [action for action in enabled if action.kind is ActionKind.PREP]
    if distinguisher or preps:
        return "Stop-Budget"
    return "Stop-NoDistinguisher"


def admit_decision(session: Session, library: list[Action]) -> str:
    actions = admissible(session, library)
    if select(session, actions) is not None:
        return "A1"
    if session.q_status is QStatus.UNKNOWN:
        if any(recover_eligible(action) for action in library):
            return "A5"
        return "A4"
    enabled = [
        action
        for action in library
        if action.kind is not ActionKind.RECOVER and session.q in action.enabled_at
    ]
    if any(can_strictly_reduce(action, session.Hk) for action in enabled) or any(
        action.kind is ActionKind.PREP for action in enabled
    ):
        return "A2"
    return "A3"


def admit_or_stop(session: Session, library: list[Action]) -> Action | None:
    actions = admissible(session, library)
    chosen = select(session, actions)
    if chosen is not None:
        return chosen
    session.stop = classify_empty(session, library)
    return None


def classify_update(
    session: Session,
    *,
    named_645: bool = False,
    equivalent: bool = False,
) -> str | None:
    if not session.Hk:
        return "Stop-Empty"
    if len(session.Hk) == 1:
        return "Stop-Singleton"
    if named_645:
        return "Stop-645"
    if equivalent:
        return "Stop-Equivalent"
    if resource_exhausted(session):
        return "Stop-Budget"
    return None


def apply_valid_observation(
    session: Session,
    action: Action,
    remaining: set[str] | None,
    *,
    confirmed_q: str | None = None,
    named_645: bool = False,
    equivalent: bool = False,
) -> None:
    if remaining is not None:
        session.Hk = set(remaining)
    if action.kind is ActionKind.RECOVER:
        session.history.append(f"recover:{action.id}")
        if confirmed_q is not None and confirmed_q == action.next_q:
            session.q = confirmed_q
            session.q_status = QStatus.KNOWN
            session.stop = classify_update(session, named_645=named_645, equivalent=equivalent)
        else:
            session.q_status = QStatus.UNKNOWN
        return
    if action.next_q:
        session.q = action.next_q
    session.q_status = QStatus.KNOWN
    session.history.append(f"valid:{action.id}")
    session.stop = classify_update(session, named_645=named_645, equivalent=equivalent)


def apply_error(session: Session, action: Action, kind: ErrorKind) -> None:
    session.history.append(f"ERROR:{kind.value}:{action.id}")
    session.retries += 1
    if kind is ErrorKind.UNKNOWN_EFFECT:
        session.q_status = QStatus.UNKNOWN
    if session.retries >= session.retry_cap:
        session.stop = "Stop-Error"


def step(
    session: Session,
    library: list[Action],
    *,
    observation: set[str] | None = None,
    error: ErrorKind | None = None,
    confirmed_q: str | None = None,
    named_645: bool = False,
    equivalent: bool = False,
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
        if session.stop is None and session.q_status is QStatus.UNKNOWN:
            if not admissible(session, library):
                session.stop = classify_empty(session, library)
        return chosen
    if chosen.kind is ActionKind.RECOVER:
        apply_valid_observation(
            session,
            chosen,
            observation,
            confirmed_q=confirmed_q,
            named_645=named_645,
            equivalent=equivalent,
        )
        if session.stop is None and session.q_status is QStatus.UNKNOWN:
            if select(session, admissible(session, library)) is None:
                session.stop = classify_empty(session, library)
        return chosen
    if observation is None:
        raise ValueError("valid execution requires an observation remaining-set")
    apply_valid_observation(
        session,
        chosen,
        observation,
        confirmed_q=confirmed_q,
        named_645=named_645,
        equivalent=equivalent,
    )
    return chosen
