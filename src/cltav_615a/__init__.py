"""Bounded ARINC 615A UPLOAD LUR-start engineering objects.

The package deliberately implements only the small semantic control slice
accepted for PR #26 B-stage work.  It is not a network stack, a wire-packet
codec, a protocol verdict engine, or a CL-TAV session adapter.
"""

from .controller import LurStartController
from .source_identity import LoadedSourceIdentity, SourceIdentityError, register_loaded_module
from .types import (
    ActivationRecord,
    CompletionReceipt,
    FaultInstallationRecord,
    FaultLifecycleReadback,
    FaultVariant,
    FiniteCheckResult,
    JournalSnapshot,
    OperationResult,
    PublicEvent,
    ResetReadback,
)

__all__ = [
    "ActivationRecord",
    "CompletionReceipt",
    "FaultInstallationRecord",
    "FaultLifecycleReadback",
    "FaultVariant",
    "FiniteCheckResult",
    "JournalSnapshot",
    "LurStartController",
    "LoadedSourceIdentity",
    "SourceIdentityError",
    "OperationResult",
    "PublicEvent",
    "ResetReadback",
]


register_loaded_module(__name__, __file__)
