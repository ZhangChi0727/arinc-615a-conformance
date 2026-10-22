"""Finite public model parsing and prediction for the reference session.

The model declares per-hypothesis *observable emissions*.  Prediction groups
those public emissions after actual finite-kernel propagation.  The synthetic
environment holds a separate private state and is never asked for a candidate
set or a predicted class.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from .kernel import (
    FrontierEntry,
    Interval,
    KernelDiagnostic,
    ModelContext,
    initial_entry,
    propagate_transition,
)


_ACTION_KINDS = frozenset({"TEST", "PREP", "RECOVER"})


def _canonical_digest(value: Mapping[str, Any]) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8"),
    ).hexdigest()


@dataclass(frozen=True)
class SyntheticAction:
    """One public action declared by a finite reference model."""

    action_id: str
    kind: str
    cost: int
    detail_charges: Mapping[str, int]
    enabled_summaries: frozenset[str]
    transition: Mapping[str, Any]
    observable_by_hypothesis: Mapping[str, tuple[str, ...]]

    def projected_cost(self) -> Mapping[str, int]:
        """Return the declared four-component projection without recharging."""

        return MappingProxyType(
            {
                "acquisition": self.detail_charges["acquisition"],
                "computation": self.detail_charges["computation"],
                "preparation": self.detail_charges["preparation"] + self.detail_charges["recovery"],
                "retry": self.detail_charges["retry"],
            },
        )


@dataclass(frozen=True)
class PredictionClass:
    """A nonempty current observation class, produced by model calculation."""

    action_id: str
    observable: str
    hypotheses: frozenset[str]
    successors: Mapping[str, FrontierEntry]
    conservative_hypotheses: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ActionPrediction:
    """Finite prediction for exactly one action and one history version."""

    action_id: str
    classes: tuple[PredictionClass, ...]
    diagnostics: tuple[KernelDiagnostic, ...]

    @property
    def has_distinguishing_value(self) -> bool:
        universe = frozenset().union(*(value.hypotheses for value in self.classes))
        return any(0 < len(value.hypotheses) < len(universe) for value in self.classes)


@dataclass(frozen=True)
class FiniteSessionModel:
    """Validated public model data for the bounded reference session."""

    context: ModelContext
    actions: Mapping[str, SyntheticAction]
    initial_frontiers: Mapping[str, FrontierEntry]
    path_limit: int
    frontier_limit: int
    hypothesis_limit: int
    action_limit: int
    observation_class_limit: int
    identity: str
    uncertainty_identity: str

    @classmethod
    def from_mapping(
        cls, *, context: ModelContext, value: Mapping[str, Any],
    ) -> "FiniteSessionModel":
        if not isinstance(value, Mapping):
            raise ValueError("finite session model must be an object")
        required = {
            "model", "hypotheses", "actions", "limits", "uncertaintyIdentity",
        }
        if set(value) != required:
            raise ValueError("finite session model uses unknown or missing fields")
        model = value["model"]
        if not isinstance(model, Mapping):
            raise ValueError("finite session model declaration is invalid")
        expected_model = {
            "stateIds": sorted(context.state_ids),
            "clockIds": sorted(context.clock_ids),
            "typedDomains": {
                key: sorted(domain) for key, domain in sorted(context.typed_domains.items())
            },
        }
        if _canonical_model(model) != expected_model:
            raise ValueError("finite session model differs from its verified context")
        hypotheses = value["hypotheses"]
        actions = value["actions"]
        limits = value["limits"]
        uncertainty_identity = value["uncertaintyIdentity"]
        if not isinstance(hypotheses, list) or not hypotheses:
            raise ValueError("finite session model needs at least one hypothesis")
        if not isinstance(actions, list) or not actions:
            raise ValueError("finite session model needs at least one action")
        if not isinstance(limits, Mapping) or set(limits) != {
            "pathLength", "frontierStates", "hypotheses", "actions", "observationClasses",
        }:
            raise ValueError("finite session model limits are invalid")
        path_limit = _positive_int(limits["pathLength"], "path length")
        frontier_limit = _positive_int(limits["frontierStates"], "frontier limit")
        hypothesis_limit = _positive_int(limits["hypotheses"], "hypothesis limit")
        action_limit = _positive_int(limits["actions"], "action limit")
        observation_class_limit = _positive_int(limits["observationClasses"], "observation-class limit")
        if not isinstance(uncertainty_identity, str) or not uncertainty_identity:
            raise ValueError("finite session model uncertainty identity is invalid")
        hypothesis_ids: list[str] = []
        frontiers: dict[str, FrontierEntry] = {}
        for item in hypotheses:
            identifier, entry = _initial_frontier(context, item)
            if identifier in frontiers:
                raise ValueError("finite session model has duplicate hypothesis IDs")
            hypothesis_ids.append(identifier)
            frontiers[identifier] = entry
        parsed_actions: dict[str, SyntheticAction] = {}
        for item in actions:
            action = _parse_action(item, frozenset(hypothesis_ids))
            if action.action_id in parsed_actions:
                raise ValueError("finite session model has duplicate action IDs")
            parsed_actions[action.action_id] = action
        if len(parsed_actions) > action_limit:
            raise ValueError("finite session action count exceeds its declared bound")
        if len(frontiers) > hypothesis_limit:
            raise ValueError("finite session hypothesis count exceeds its declared bound")
        identity = _canonical_digest(value)
        return cls(
            context=context,
            actions=MappingProxyType(parsed_actions),
            initial_frontiers=MappingProxyType(frontiers),
            path_limit=path_limit,
            frontier_limit=frontier_limit,
            hypothesis_limit=hypothesis_limit,
            action_limit=action_limit,
            observation_class_limit=observation_class_limit,
            identity=identity,
            uncertainty_identity=uncertainty_identity,
        )

    def predict(
        self, *, hypotheses: frozenset[str], frontiers: Mapping[str, FrontierEntry],
        status_by_hypothesis: Mapping[str, str], action_id: str,
    ) -> ActionPrediction:
        """Compute current classes by propagating each current public path."""

        action = self.actions.get(action_id)
        if action is None:
            return ActionPrediction(
                action_id, (), (KernelDiagnostic("UNKNOWN-ACTION", "action is not in the declared finite model"),),
            )
        if not hypotheses or not hypotheses <= set(frontiers):
            return ActionPrediction(
                action_id, (), (KernelDiagnostic("INVALID-HISTORY", "current hypotheses/frontiers are inconsistent"),),
            )
        grouped: dict[str, dict[str, FrontierEntry]] = {}
        conservative: dict[str, FrontierEntry] = {}
        diagnostics: list[KernelDiagnostic] = []
        for hypothesis in sorted(hypotheses):
            if status_by_hypothesis.get(hypothesis) == "CONSERVATIVE-UNKNOWN":
                conservative[hypothesis] = frontiers[hypothesis]
                continue
            result = propagate_transition(
                frontiers[hypothesis],
                action.transition,
                state_ids=set(self.context.state_ids),
                clock_ids=set(self.context.clock_ids),
                typed_domains={key: set(domain) for key, domain in self.context.typed_domains.items()},
                context=self.context,
                path_limit=self.path_limit,
                frontier_limit=self.frontier_limit,
            )
            diagnostics.extend(result.diagnostics)
            if result.kind == "FEASIBLE" and len(result.entries) == 1:
                for observable in action.observable_by_hypothesis[hypothesis]:
                    grouped.setdefault(observable, {})[hypothesis] = result.entries[0]
            elif result.kind != "INFEASIBLE":
                # A bounded/unsupported computation keeps its hypothesis in a
                # conservative continuation.  It is included in every normal
                # class below, so a visible normal observation cannot exclude
                # a hypothesis whose applicable computation was not completed.
                conservative[hypothesis] = frontiers[hypothesis]
        if conservative:
            if grouped:
                for successors in grouped.values():
                    successors.update(conservative)
            else:
                # No completed calculation produced a visible class.  Keeping
                # a synthetic ``unknown`` class here would make an incomplete
                # calculation look like an admissible, distinguishing TEST
                # outcome.  The coordinator must instead treat this as the
                # named prediction gap and may consider an admitted PREP.
                return ActionPrediction(
                    action_id,
                    (),
                    tuple(
                        diagnostics
                        + [
                            KernelDiagnostic(
                                "CONSERVATIVE-PREDICTION-GAP",
                                "no completed visible class exists; conservative hypotheses are retained",
                            ),
                        ]
                    ),
                )
        if len(grouped) > self.observation_class_limit:
            retained = {hypothesis: frontiers[hypothesis] for hypothesis in hypotheses}
            return ActionPrediction(
                action_id,
                (
                    PredictionClass(
                        action_id=action_id,
                        observable="__conservative_unknown__",
                        hypotheses=frozenset(retained),
                        successors=MappingProxyType(retained),
                        conservative_hypotheses=frozenset(retained),
                    ),
                ),
                tuple(diagnostics + [KernelDiagnostic("OBSERVATION-CLASS-LIMIT", "declared observation-class bound reached; hypotheses retained")]),
            )
        classes = tuple(
            PredictionClass(
                action_id=action_id,
                observable=observable,
                hypotheses=frozenset(successors),
                successors=MappingProxyType(dict(successors)),
                conservative_hypotheses=frozenset(conservative),
            )
            for observable, successors in sorted(grouped.items())
        )
        return ActionPrediction(action_id, classes, tuple(diagnostics))


def _canonical_model(value: Mapping[str, Any]) -> dict[str, Any]:
    if set(value) != {"stateIds", "clockIds", "typedDomains"}:
        raise ValueError("finite session model declaration is invalid")
    states, clocks, domains = value.get("stateIds"), value.get("clockIds"), value.get("typedDomains")
    if not isinstance(states, list) or not isinstance(clocks, list) or not isinstance(domains, Mapping):
        raise ValueError("finite session model declaration is invalid")
    if any(not isinstance(item, str) for item in states + clocks):
        raise ValueError("finite session model identifiers are invalid")
    normalized_domains: dict[str, list[Any]] = {}
    for key, domain in domains.items():
        if not isinstance(key, str) or not isinstance(domain, list):
            raise ValueError("finite session model typed domains are invalid")
        normalized_domains[key] = sorted(domain)
    return {"stateIds": sorted(states), "clockIds": sorted(clocks), "typedDomains": normalized_domains}


def _initial_frontier(context: ModelContext, item: Any) -> tuple[str, FrontierEntry]:
    if not isinstance(item, Mapping):
        raise ValueError("finite session hypothesis is invalid")
    required = {"id", "controlStateId", "clockConstraint", "typedStore"}
    if set(item) != required:
        raise ValueError("finite session hypothesis uses unknown or missing fields")
    identifier = item.get("id")
    state = item.get("controlStateId")
    clocks = item.get("clockConstraint")
    store = item.get("typedStore")
    if not isinstance(identifier, str) or not identifier or not isinstance(state, str):
        raise ValueError("finite session hypothesis identity is invalid")
    if not isinstance(clocks, Mapping) or set(clocks) != set(context.clock_ids):
        raise ValueError("finite session hypothesis clock constraint is invalid")
    parsed_clocks = {name: Interval.from_mapping(interval) for name, interval in clocks.items()}
    if not isinstance(store, Mapping):
        raise ValueError("finite session hypothesis typed store is invalid")
    return identifier, initial_entry(
        context,
        hypothesis_id=identifier,
        control_state_id=state,
        clocks=parsed_clocks,
        typed_store=store,
        root_id=f"root:{identifier}",
    )


def _parse_action(item: Any, hypothesis_ids: frozenset[str]) -> SyntheticAction:
    if not isinstance(item, Mapping):
        raise ValueError("finite session action is invalid")
    required = {
        "id", "kind", "cost", "detailCharges", "enabledSummaries", "transition", "observableByHypothesis",
    }
    if set(item) != required:
        raise ValueError("finite session action uses unknown or missing fields")
    identifier = item.get("id")
    kind = item.get("kind")
    cost = item.get("cost")
    detail_charges = item.get("detailCharges")
    summaries = item.get("enabledSummaries")
    transition = item.get("transition")
    emissions = item.get("observableByHypothesis")
    if not isinstance(identifier, str) or not identifier or kind not in _ACTION_KINDS:
        raise ValueError("finite session action identity or kind is invalid")
    if isinstance(cost, bool) or not isinstance(cost, int) or cost < 1:
        raise ValueError("finite session action cost must be a positive integer")
    if not isinstance(detail_charges, Mapping) or set(detail_charges) != {
        "acquisition", "computation", "preparation", "recovery", "retry",
    }:
        raise ValueError("finite session action detail charges are invalid")
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in detail_charges.values()):
        raise ValueError("finite session action detail charge is invalid")
    if not isinstance(summaries, list) or not summaries or any(not isinstance(value, str) or not value for value in summaries):
        raise ValueError("finite session action enabled summaries are invalid")
    if not isinstance(transition, Mapping):
        raise ValueError("finite session action transition is invalid")
    if not isinstance(emissions, Mapping) or set(emissions) != hypothesis_ids:
        raise ValueError("finite session action emissions must cover exactly the declared hypotheses")
    parsed_emissions: dict[str, tuple[str, ...]] = {}
    for hypothesis, emission in emissions.items():
        values = (emission,) if isinstance(emission, str) else tuple(emission) if isinstance(emission, list) else ()
        if not values or any(not isinstance(item, str) or not item for item in values) or len(values) != len(set(values)):
            raise ValueError("finite session action observable emission is invalid")
        parsed_emissions[hypothesis] = values
    return SyntheticAction(
        identifier,
        kind,
        cost,
        MappingProxyType(dict(detail_charges)),
        frozenset(summaries),
        MappingProxyType(dict(transition)),
        MappingProxyType(parsed_emissions),
    )


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"finite session {label} must be a positive integer")
    return value
