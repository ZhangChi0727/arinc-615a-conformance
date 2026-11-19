"""Algorithm-visible IUT operations.  No fault overlay, snapshot, or truth API."""

from __future__ import annotations

from typing import Any

from a615a_sim.bound_iut.protocol import SimulatedTarget


class AlgorithmVisibleTarget:
    """Proxy so arm code cannot call evaluator or overlay methods on the IUT."""

    __slots__ = ("_target",)

    def __init__(self, target: SimulatedTarget) -> None:
        self._target = target

    def find(self, correlation_id: str) -> dict[str, Any]:
        return self._target.find(correlation_id)

    def send(self, correlation_id: str) -> dict[str, Any]:
        return self._target.send(correlation_id)

    def abort(self, correlation_id: str) -> dict[str, Any]:
        return self._target.abort(correlation_id)

    def information(self, correlation_id: str) -> dict[str, Any]:
        return self._target.information(correlation_id)

    def algorithm_visible_records(self) -> list[dict[str, Any]]:
        return self._target.algorithm_visible_records()
