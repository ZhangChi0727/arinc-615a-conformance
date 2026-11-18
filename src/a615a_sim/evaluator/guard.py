"""Fail-closed leakage guard for evaluator-only experiment truth.

Algorithm and arm modules must never read IF-EXP-TRUTH.  Access is denied when
any frame on the call stack belongs to a denied prefix, or when the first
non-guard/truth frame is not an evaluator or injector module.
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
    "experiment_arms",
    "a615a_sim.evaluator.pipeline.run",
    "a615a_sim.evaluator.pipeline.collect",
)

ALLOWED_PREFIXES = (
    "a615a_sim.evaluator",
    "a615a_sim.faults",
)

_SKIP_PREFIXES = (
    "a615a_sim.evaluator.guard",
    "a615a_sim.evaluator.truth",
    "importlib",
)


class TruthLeakageError(RuntimeError):
    """Raised when algorithm-visible code reaches evaluator truth."""


def _module_name(frame: inspect.FrameInfo) -> str:
    name = frame.frame.f_globals.get("__name__", "")
    return name if isinstance(name, str) else ""


def _matches(name: str, prefixes: tuple[str, ...]) -> bool:
    return any(name == prefix or name.startswith(prefix + ".") for prefix in prefixes)


def _is_algorithm(name: str) -> bool:
    return _matches(name, ALGORITHM_PREFIXES)


def _is_allowed(name: str) -> bool:
    return _matches(name, ALLOWED_PREFIXES)


def _direct_caller(names: list[str]) -> str | None:
    for name in names:
        if not name or _matches(name, _SKIP_PREFIXES):
            continue
        return name
    return None


def deny_algorithm_import(*, operation: str = "import") -> None:
    """Import-time fail-closed companion to runtime access checks."""

    deny_algorithm_truth_access(operation=operation)


def deny_algorithm_truth_access(*, operation: str) -> None:
    """Fail closed: deny unless the direct caller is allowed and no algorithm frame is."""

    names = [_module_name(frame) for frame in inspect.stack()[1:]]
    if any(_is_algorithm(name) for name in names if name):
        raise TruthLeakageError(
            f"IF-EXP-TRUTH {operation} denied: algorithm/arm frame on stack"
        )
    direct = _direct_caller(names)
    if direct is None or not _is_allowed(direct):
        raise TruthLeakageError(
            f"IF-EXP-TRUTH {operation} denied: caller is not an evaluator or injector frame"
        )
