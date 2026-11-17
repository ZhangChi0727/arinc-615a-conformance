"""Independent evaluator truth store (IF-EXP-TRUTH).

Written only after injection confirmation.  Unconfirmed injection cannot default
to valid truth.  Algorithm/arm modules cannot read this store.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping
from uuid import uuid4

from a615a_sim.evaluator.guard import deny_algorithm_import, deny_algorithm_truth_access
from a615a_sim.faults.catalogue import entry_by_id
from a615a_sim.faults.injector import InjectionAttempt

deny_algorithm_import(operation="import-truth")


@dataclass(frozen=True)
class TruthRecord:
    scene_id: str
    attempt_id: str
    confirmation_ref: str
    independent_generator_id: str
    truth_hypothesis: str | None
    injection_status: str
    equivalence_disposition: str
    fault_domain_class: str
    shared_component_risk: tuple[str, ...]

    def as_mapping(self) -> Mapping[str, Any]:
        deny_algorithm_truth_access(operation="project")
        return MappingProxyType(
            {
                "sceneId": self.scene_id,
                "attemptId": self.attempt_id,
                "confirmationRef": self.confirmation_ref,
                "independentGeneratorId": self.independent_generator_id,
                "truthHypothesis": self.truth_hypothesis,
                "injectionStatus": self.injection_status,
                "equivalenceDisposition": self.equivalence_disposition,
                "faultDomainClass": self.fault_domain_class,
                "sharedComponentRisk": list(self.shared_component_risk),
                "label": "SIMULATED-IUT",
                "producer": "IF-EXP-TRUTH",
            }
        )


class IndependentTruthStore:
    """Module-boundary evaluator store.  Not an algorithm input."""

    GENERATOR_ID = "SIMULATED-TRUTH-GENERATOR-A"

    def __init__(self) -> None:
        deny_algorithm_truth_access(operation="construct")
        self._records: dict[str, TruthRecord] = {}

    def write_from_confirmed_injection(self, attempt: InjectionAttempt) -> TruthRecord:
        deny_algorithm_truth_access(operation="write")
        if not attempt.injection_confirmed:
            raise ValueError("unconfirmed injection cannot default to valid truth")
        entry = entry_by_id(attempt.fault_id)
        record = TruthRecord(
            scene_id=attempt.scene_id,
            attempt_id=attempt.attempt_id,
            confirmation_ref=f"INJ-{attempt.attempt_id}",
            independent_generator_id=self.GENERATOR_ID,
            truth_hypothesis=entry.get("hypothesisId"),
            injection_status=str(entry["injectionStatusIfConfirmed"]),
            equivalence_disposition="unresolved",
            fault_domain_class=str(entry["faultDomainClass"]),
            shared_component_risk=(
                "shared simulated clock SIMULATED-CLOCK-CLTAV-EXP-A",
                "shared bound-model protocol event names",
            ),
        )
        self._records[attempt.attempt_id] = record
        return record

    def get(self, attempt_id: str) -> TruthRecord:
        deny_algorithm_truth_access(operation="read")
        return self._records[attempt_id]

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_") or name in {"GENERATOR_ID"}:
            return object.__getattribute__(self, name)
        deny_algorithm_truth_access(operation=f"attr:{name}")
        return object.__getattribute__(self, name)


def new_attempt_id() -> str:
    deny_algorithm_truth_access(operation="id")
    return f"A-{uuid4().hex[:12]}"
