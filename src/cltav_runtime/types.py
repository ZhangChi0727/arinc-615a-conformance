"""Closed runtime values at the reference-session boundary.

These are engineering representations of the controlled `SessionContext` and
`HistoryHandle` interfaces.  They intentionally do not redefine the method or
the contract package.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping


_HYPOTHESIS_STATUS = frozenset({"KNOWN", "CONSERVATIVE-UNKNOWN"})
# ``UNKNOWN`` describes the session-level summary state.  The separate
# ``CONSERVATIVE-UNKNOWN`` value belongs to the per-hypothesis history handle:
# conflating the two loses the distinction between an unusable session summary
# and the conservative retention of an individual candidate path.
_SESSION_STATUS = frozenset({"KNOWN", "UNKNOWN"})


def _stable_string_set(values: frozenset[str] | set[str] | tuple[str, ...]) -> frozenset[str]:
    if not isinstance(values, (frozenset, set, tuple)):
        raise ValueError("hypothesis set must be an explicit finite collection")
    result = frozenset(values)
    if any(not isinstance(value, str) or not value for value in result):
        raise ValueError("hypothesis identifiers must be nonempty strings")
    return result


def _frontier_mapping(
    hypotheses: frozenset[str], values: Mapping[str, str | tuple[str, ...]], *, complete: bool,
) -> Mapping[str, tuple[str, ...]]:
    if not isinstance(values, Mapping):
        raise ValueError("compatible-state map must be a mapping")
    copied = dict(values)
    if set(copied) != hypotheses:
        raise ValueError("compatible-state map keys must equal the hypothesis set")
    normalized: dict[str, tuple[str, ...]] = {}
    for key, value in copied.items():
        if not isinstance(key, str):
            raise ValueError("compatible-state map keys must be strings")
        references = (value,) if isinstance(value, str) else value
        if (
            not isinstance(references, tuple)
            or not references
            or any(not isinstance(reference, str) or not reference for reference in references)
            or len(references) != len(set(references))
        ):
            raise ValueError("compatible-state map values must be nonempty unique reference tuples")
        normalized[key] = references
    return MappingProxyType(normalized)


def _status_mapping(
    hypotheses: frozenset[str], values: Mapping[str, str], *, complete: bool,
) -> Mapping[str, str]:
    if not isinstance(values, Mapping):
        raise ValueError("hypothesis status map must be a mapping")
    copied = dict(values)
    if not set(copied) <= hypotheses:
        raise ValueError("hypothesis status map contains an undeclared hypothesis")
    if complete and set(copied) != hypotheses:
        raise ValueError("committed history status map must cover every surviving hypothesis")
    if any(value not in _HYPOTHESIS_STATUS for value in copied.values()):
        raise ValueError("hypothesis status is outside the controlled vocabulary")
    return MappingProxyType(copied)


@dataclass(frozen=True)
class HistoryHandle:
    """Immutable versioned history, with separate input/output constructors.

    Initial S0 input may omit member statuses.  A processed result must cover
    every surviving member, so conservative propagation cannot be represented
    by an apparently known partial result.
    """

    hypotheses: frozenset[str]
    compatible_state_by_hypothesis: Mapping[str, tuple[str, ...]]
    status_by_hypothesis: Mapping[str, str]
    version: int
    processed: bool

    @classmethod
    def initial(
        cls,
        *,
        hypotheses: frozenset[str] | set[str] | tuple[str, ...],
        compatible_state_by_hypothesis: Mapping[str, str | tuple[str, ...]],
        status_by_hypothesis: Mapping[str, str] | None = None,
    ) -> "HistoryHandle":
        members = _stable_string_set(hypotheses)
        if not members:
            raise ValueError("initial history must contain at least one hypothesis")
        states = _frontier_mapping(members, compatible_state_by_hypothesis, complete=False)
        statuses = _status_mapping(members, status_by_hypothesis or {}, complete=False)
        return cls(members, states, statuses, 0, False)

    @classmethod
    def committed(
        cls,
        *,
        hypotheses: frozenset[str] | set[str] | tuple[str, ...],
        compatible_state_by_hypothesis: Mapping[str, str | tuple[str, ...]],
        status_by_hypothesis: Mapping[str, str],
        version: int,
    ) -> "HistoryHandle":
        members = _stable_string_set(hypotheses)
        if isinstance(version, bool) or not isinstance(version, int) or version < 1:
            raise ValueError("committed history version must be a positive integer")
        states = _frontier_mapping(members, compatible_state_by_hypothesis, complete=True)
        statuses = _status_mapping(members, status_by_hypothesis, complete=True)
        return cls(members, states, statuses, version, True)


@dataclass(frozen=True)
class SessionContext:
    """Read-only algorithm session state before action selection."""

    session_id: str
    run_id: str
    experiment_attempt_id: str | None
    model_identity: str
    current_summary: str | None
    q_status: str
    resource_remainder: int = 0
    retry_count: int = 0
    retry_cap: int = 1
    known_target: str | None = None
    known_evidence: tuple[str, ...] = ()
    error_history: tuple[str, ...] = ()
    unknown_history: tuple[str, ...] = ()

    @classmethod
    def create(
        cls, *, session_id: str, run_id: str, experiment_attempt_id: str | None,
        model_identity: str, current_summary: str | None, q_status: str,
        resource_remainder: int = 0,
        retry_count: int = 0,
        retry_cap: int = 1,
        known_target: str | None = None,
        known_evidence: tuple[str, ...] | list[str] = (),
        error_history: tuple[str, ...] | list[str] = (),
        unknown_history: tuple[str, ...] | list[str] = (),
    ) -> "SessionContext":
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session identity must be a nonempty string")
        if not isinstance(run_id, str) or not run_id:
            raise ValueError("run identity must be a nonempty string")
        if experiment_attempt_id is not None and (
            not isinstance(experiment_attempt_id, str) or not experiment_attempt_id
        ):
            raise ValueError("experiment attempt identity must be absent or a nonempty string")
        if not isinstance(model_identity, str) or not model_identity:
            raise ValueError("model identity must be a nonempty string")
        if q_status not in _SESSION_STATUS:
            raise ValueError("session status is outside the controlled vocabulary")
        if current_summary is not None and (not isinstance(current_summary, str) or not current_summary):
            raise ValueError("session summary must be a nonempty string or absent")
        if q_status == "KNOWN" and current_summary is None:
            raise ValueError("KNOWN session status requires a current summary")
        if q_status != "KNOWN" and current_summary is not None:
            raise ValueError("non-KNOWN session status cannot retain a current summary")
        if (
            isinstance(resource_remainder, bool)
            or not isinstance(resource_remainder, int)
            or resource_remainder < 0
        ):
            raise ValueError("session resource remainder must be a nonnegative integer")
        if isinstance(retry_count, bool) or not isinstance(retry_count, int) or retry_count < 0:
            raise ValueError("session retry count must be a nonnegative integer")
        if isinstance(retry_cap, bool) or not isinstance(retry_cap, int) or retry_cap < 1:
            raise ValueError("session retry cap must be a positive integer")
        if retry_count > retry_cap:
            raise ValueError("session retry count cannot exceed the retry cap")
        if known_target is not None and (not isinstance(known_target, str) or not known_target):
            raise ValueError("known recovery target must be absent or a nonempty string")

        def _audit_values(value: tuple[str, ...] | list[str], *, label: str) -> tuple[str, ...]:
            if not isinstance(value, (tuple, list)) or any(
                not isinstance(item, str) or not item.strip() for item in value
            ):
                raise ValueError(f"session {label} must be a sequence of nonblank strings")
            return tuple(value)

        evidence = _audit_values(known_evidence, label="known evidence")
        errors = _audit_values(error_history, label="error history")
        unknowns = _audit_values(unknown_history, label="unknown history")
        if q_status != "KNOWN" and (known_target is not None or evidence):
            raise ValueError("non-KNOWN session status cannot retain confirmed recovery data")
        return cls(
            session_id,
            run_id,
            experiment_attempt_id,
            model_identity,
            current_summary,
            q_status,
            resource_remainder,
            retry_count,
            retry_cap,
            known_target,
            evidence,
            errors,
            unknowns,
        )
