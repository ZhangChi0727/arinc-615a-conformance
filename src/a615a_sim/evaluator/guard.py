"""Fail-closed leakage guard for evaluator-only experiment truth.

Algorithm and arm modules must never read IF-EXP-TRUTH.  Access is denied when
any frame on the call stack belongs to a denied prefix, or when no allowed
evaluator/test/injector frame can be identified.
"""

from __future__ import annotations

import inspect

ALGORITHM_PREFIXES = (
    "cltav_runtime",
    "cltav_615a_adapter",
    "cltav_615a_engineering",
    "cltav_offline",
    "a615a_sim.bound_iut",
    "a615a_sim.algorithm",
)

ALLOWED_PREFIXES = (
    "a615a_sim.evaluator",
    "a615a_sim.faults",
    "tests.",
    "test_",
)


class TruthLeakageError(RuntimeError):
    """Raised when algorithm-visible code reaches evaluator truth."""


def _module_name(frame: inspect.FrameInfo) -> str:
    name = frame.frame.f_globals.get("__name__", "")
    return name if isinstance(name, str) else ""


def _is_algorithm(name: str) -> bool:
    return any(name == prefix or name.startswith(prefix + ".") for prefix in ALGORITHM_PREFIXES)


def _is_allowed(name: str) -> bool:
    if any(name == prefix or name.startswith(prefix + ".") for prefix in ALLOWED_PREFIXES):
        return True
    if name.startswith("test_") or ".test_" in name:
        return True
    return False


def deny_algorithm_import(*, operation: str = "import") -> None:
    """Import-time fail-closed companion to runtime access checks."""

    deny_algorithm_truth_access(operation=operation)


def deny_algorithm_truth_access(*, operation: str) -> None:
    """Fail closed: deny unless an allowed frame is present and no algorithm frame is."""

    names = [_module_name(frame) for frame in inspect.stack()[1:]]
    if any(_is_algorithm(name) for name in names if name):
        raise TruthLeakageError(
            f"IF-EXP-TRUTH {operation} denied: algorithm/arm frame on stack"
        )
    if not any(_is_allowed(name) for name in names if name):
        raise TruthLeakageError(
            f"IF-EXP-TRUTH {operation} denied: caller is not an evaluator or test frame"
        )
