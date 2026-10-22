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
from .model import ActionPrediction, FiniteSessionModel, PredictionClass, SyntheticAction
from .session import (
    AlgorithmResourceView,
    ReferenceSession,
    ResourceState,
    RoundEvidence,
    SelectSnapshot,
    SessionResult,
    SessionState,
)
from .synthetic import ExecutionRequest, SyntheticEnvironment, VisibleExecutionRecord
from .types import HistoryHandle, SessionContext

__all__ = [
    "ContractSnapshot",
    "ExecutionRequest",
    "FiniteSessionModel",
    "HistoryHandle",
    "FrontierEntry",
    "Interval",
    "KernelDiagnostic",
    "KernelResult",
    "ModelContext",
    "ProvenanceRecord",
    "PredictionClass",
    "ActionPrediction",
    "AlgorithmResourceView",
    "ReferenceSession",
    "ResourceState",
    "RoundEvidence",
    "RuntimeAuthorityBinding",
    "SessionContext",
    "SessionResult",
    "SessionState",
    "SelectSnapshot",
    "SourceSnapshot",
    "SyntheticAction",
    "SyntheticEnvironment",
    "VisibleExecutionRecord",
    "initial_entry",
    "merge_frontier",
    "propagate_transition",
]
