"""CL-LOOP: drive existing ReferenceSession.  Do not copy its selection semantics."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState
from cltav_runtime.synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    VisibleExecutionRecord,
)

from a615a_sim.algorithm.execute import issue
from a615a_sim.algorithm.library import (
    ACTION_TEST_ABORT,
    ACTION_TEST_FIND,
    ACTION_TEST_INFORMATION,
    ACTION_TEST_SEND,
    ArmRun,
    ExclusiveResource,
    FAIR_DETAIL_CHARGES,
    predetermined_test_sequence,
)
from a615a_sim.algorithm.target_view import AlgorithmVisibleTarget

_ROOT = Path(__file__).resolve().parents[3]
_DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
_INTERFACE_PATH = "configs/research/cltav_interface_registry.json"


class SimulatedIutEnvironment:
    """Duck-typed environment for ReferenceSession.execute.  Not a runtime fork."""

    def __init__(self, target: AlgorithmVisibleTarget, correlation_id: str, run: ArmRun, resource: ExclusiveResource) -> None:
        self._target = target
        self._correlation_id = correlation_id
        self._run = run
        self._resource = resource

    def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
        if not isinstance(request, ExecutionRequest):
            raise ValueError("simulated IUT environment requires an execution request")
        visible = issue(
            self._target,
            self._run,
            self._resource,
            request.action_id,
            correlation_id=self._correlation_id,
        )
        if visible is None:
            record = VisibleExecutionRecord(
                execution_attempt_id=request.execution_attempt_id,
                action_id=request.action_id,
                effect_class="CONFIRMED-NOT-SENT",
                observable=None,
                summary_confirmed=False,
                post_summary=None,
                measurement_tick=None,
                uncertainty_identity=None,
                evidence_ref=f"sim-iut:{request.execution_attempt_id}:budget",
            )
            return EnvironmentExecution(record, self)
        record = VisibleExecutionRecord(
            execution_attempt_id=request.execution_attempt_id,
            action_id=request.action_id,
            effect_class="NONE",
            observable=visible["kind"],
            summary_confirmed=True,
            post_summary=visible["kind"],
            measurement_tick=Fraction(visible["tick"]),
            uncertainty_identity="sim-iut-u-1",
            evidence_ref=f"sim-iut:{request.execution_attempt_id}",
        )
        return EnvironmentExecution(record, self)


def _hypothesis(identifier: str) -> dict[str, object]:
    return {
        "id": identifier,
        "controlStateId": "q0",
        "clockConstraint": {
            "x": {
                "lower": {"numerator": 0, "positiveDenominator": 1},
                "upper": {"numerator": 0, "positiveDenominator": 1},
                "lowerClosed": True,
                "upperClosed": True,
            }
        },
        "typedStore": {"mode": "normal"},
    }


def _test_action(action_id: str, emissions: dict[str, str]) -> dict[str, object]:
    detail = dict(FAIR_DETAIL_CHARGES[action_id])
    return {
        "id": action_id,
        "kind": "TEST",
        "cost": max(1, sum(detail.values())),
        "detailCharges": detail,
        "enabledSummaries": ["q0"],
        "transition": {
            "id": f"tr-{action_id}",
            "source": "q0",
            "target": "q0",
            "guardAst": {"tag": "TRUE"},
            "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": "q0"}],
        },
        "observableByHypothesis": emissions,
        "measurementTicksByHypothesis": {key: 0 for key in emissions},
    }


def experiment_session_model() -> dict[str, object]:
    hyps = ("h0", "h1", "h2", "h3")
    kinds = {
        ACTION_TEST_FIND: {h: "FIND-ANSWER" for h in hyps},
        ACTION_TEST_SEND: {h: "COMPLETED" for h in hyps},
        ACTION_TEST_ABORT: {h: "ABORT" for h in hyps},
        ACTION_TEST_INFORMATION: {h: "STATUS" for h in hyps},
    }
    return {
        "model": {
            "stateIds": ["q0"],
            "clockIds": ["x"],
            "typedDomains": {"mode": ["normal"]},
        },
        "hypotheses": [_hypothesis(h) for h in hyps],
        "actions": [_test_action(action_id, kinds[action_id]) for action_id in kinds],
        "limits": {
            "pathLength": 3,
            "frontierStates": 8,
            "hypotheses": 4,
            "actions": 4,
            "observationClasses": 8,
        },
        "uncertainty": {
            "id": "sim-iut-u-1",
            "clockId": "x",
            "timeUnit": "ticks",
            "maximumErrorTicks": 0,
        },
    }


def _session(resource: ExclusiveResource) -> ReferenceSession:
    import subprocess

    head = subprocess.run(
        ["git", "-C", str(_ROOT), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()
    binding = RuntimeAuthorityBinding.from_git_objects(
        repository=_ROOT,
        development_commit=head,
        development_path=_DEVELOPMENT_PATH,
        interface_commit=head,
        interface_path=_INTERFACE_PATH,
    )
    snapshot = ContractSnapshot.from_git_object(
        repository=_ROOT, contract_commit=head, contract_path=_DEVELOPMENT_PATH,
    )
    public = experiment_session_model()["model"]
    context = ModelContext.build(
        snapshot=snapshot,
        model={
            "stateIds": set(public["stateIds"]),
            "clockIds": set(public["clockIds"]),
            "typedDomains": {name: set(domain) for name, domain in public["typedDomains"].items()},
        },
        projection_clock="x",
    )
    model = FiniteSessionModel.from_mapping(context=context, value=experiment_session_model())
    resources = (
        ResourceState.rounds(resource.remaining)
        if resource.mode == "ROUNDS"
        else ResourceState.budget(resource.remaining)
    )
    return ReferenceSession(
        binding=binding,
        model=model,
        session_id="sim-iut-loop",
        run_id="sim-iut-loop-run",
        initial_summary="q0",
        resources=resources,
        retry_cap=4,
    )


def run_cl_loop(
    target: AlgorithmVisibleTarget,
    initial: dict[str, str],
    resource: ExclusiveResource,
    *,
    correlation_id: str,
) -> ArmRun:
    """Closed loop: analysis-guided next action via existing ReferenceSession."""

    run = ArmRun("CL-LOOP", resource_mode=resource.mode, resource_remaining=resource.remaining)
    session = _session(resource)
    run.runtime_session_type = type(session).__qualname__
    if run.runtime_session_type != "ReferenceSession":
        raise RuntimeError("CL-LOOP must construct cltav_runtime.session.ReferenceSession")
    environment = SimulatedIutEnvironment(target, correlation_id, run, resource)
    # Seed the same predetermined library members as CL-T so the first issued
    # TEST is in-library; subsequent TESTs are chosen by ReferenceSession.
    seed = predetermined_test_sequence(initial)
    result = session.run(environment, maximum_rounds=max(1, len(seed) + 2))
    run.stop_class = result.stop_reason or "Stop-Error"
    run.resource_remaining = resource.remaining
    run.analysis_notes = {
        "usedInitialFields": sorted(initial.keys()),
        "referenceSession": run.runtime_session_type,
        "runtimeStop": result.stop_reason,
    }
    return run
