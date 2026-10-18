"""Bounded CL-TAV reference runtime.

This package implements only the declared finite engineering model.  It does
not implement a general solver, protocol stack, IUT adapter, or a conformance
verdict engine.
"""

from .kernel import (
    FrontierEntry,
    Interval,
    KernelDiagnostic,
    KernelResult,
    propagate_transition,
)

__all__ = [
    "FrontierEntry",
    "Interval",
    "KernelDiagnostic",
    "KernelResult",
    "propagate_transition",
]
