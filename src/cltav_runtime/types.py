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
_SESSION_STATUS = frozenset({"KNOWN", "UNKNOWN", "CONSERVATIVE-UNKNOWN"})


def _stable_string_set(values: frozenset[str] | set[str] | tuple[str, ...]) -> frozenset[str]:
    if not isinstance(values, (frozenset, set, tuple)):
        raise ValueError("hypothesis set must be an explicit finite collection")
    result = frozenset(values)
    if any(not isinstance(value, str) or not value for value in result):
        raise ValueError("hypothesis identifiers must be nonempty strings")
    return result


def _frontier_mapping(
    hypotheses: frozenset[str], values: Mapping[str, str], *, complete: bool,
) -> Mapping[str, str]:
    if not isinstance(values, Mapping):
        raise ValueError("compatible-state map must be a mapping")
    copied = dict(values)
    if set(copied) != hypotheses:
        raise ValueError("compatible-state map keys must equal the hypothesis set")
    if any(not isinstance(key, str) or not isinstance(value, str) or not value for key, value in copied.items()):
        raise ValueError("compatible-state map values must be nonempty strings")
    return MappingProxyType(copied)


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
    compatible_state_by_hypothesis: Mapping[str, str]
    status_by_hypothesis: Mapping[str, str]
    version: int
    processed: bool

    @classmethod
    def initial(
        cls,
        *,
        hypotheses: frozenset[str] | set[str] | tuple[str, ...],
        compatible_state_by_hypothesis: Mapping[str, str],
        status_by_hypothesis: Mapping[str, str] | None = None,
    ) -> "HistoryHandle":
        members = _stable_string_set(hypotheses)
        states = _frontier_mapping(members, compatible_state_by_hypothesis, complete=False)
        statuses = _status_mapping(members, status_by_hypothesis or {}, complete=False)
        return cls(members, states, statuses, 0, False)

    @classmethod
    def committed(
        cls,
        *,
        hypotheses: frozenset[str] | set[str] | tuple[str, ...],
        compatible_state_by_hypothesis: Mapping[str, str],
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
    model_identity: str
    current_summary: str | None
    q_status: str

    @classmethod
    def create(
        cls, *, session_id: str, model_identity: str, current_summary: str | None, q_status: str,
    ) -> "SessionContext":
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session identity must be a nonempty string")
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
        return cls(session_id, model_identity, current_summary, q_status)
