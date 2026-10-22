"""Bounded CL-TAV reference runtime.

This package implements only the declared finite engineering model.  It does
not implement a general solver, protocol stack, IUT adapter, or a conformance
verdict engine.
"""

from .kernel import (
    ContractSnapshot,
    FrontierEntry,
    Interval,
    KernelDiagnostic,
    KernelResult,
    ModelContext,
    ProvenanceRecord,
    initial_entry,
    merge_frontier,
    propagate_transition,
)
from .bindings import RuntimeAuthorityBinding, SourceSnapshot
from .types import HistoryHandle, SessionContext

__all__ = [
    "ContractSnapshot",
    "HistoryHandle",
    "FrontierEntry",
    "Interval",
    "KernelDiagnostic",
    "KernelResult",
    "ModelContext",
    "ProvenanceRecord",
    "RuntimeAuthorityBinding",
    "SessionContext",
    "SourceSnapshot",
    "initial_entry",
    "merge_frontier",
    "propagate_transition",
]
