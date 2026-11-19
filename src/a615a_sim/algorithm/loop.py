"""CL-LOOP: drive existing ReferenceSession.  Do not copy its selection semantics."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState
from types import MappingProxyType

from cltav_runtime.synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    SyntheticEnvironment,
    VisibleExecutionRecord,
)

from a615a_sim.algorithm.execute import issue
from a615a_sim.algorithm.hypothesis_model import (
    classify_observable,
    declare_arm_result,
    experiment_session_model,
)
from a615a_sim.algorithm.library import (
    ArmRun,
    ExclusiveResource,
    predetermined_test_sequence,
)
from a615a_sim.algorithm.target_view import AlgorithmVisibleTarget

_ROOT = Path(__file__).resolve().parents[3]
_DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
_INTERFACE_PATH = "configs/research/cltav_interface_registry.json"


class SimulatedIutEnvironment(SyntheticEnvironment):
    """IUT-backed environment for ReferenceSession.execute.  Not a runtime fork."""

    def __init__(self, target: AlgorithmVisibleTarget, correlation_id: str, run: ArmRun, resource: ExclusiveResource) -> None:
        dummy = MappingProxyType({"sim": MappingProxyType({})})
        SyntheticEnvironment.__init__(self, "sim", "sim-iut-u-1", dummy)
        object.__setattr__(self, "_visible", target)
        object.__setattr__(self, "_correlation_id", correlation_id)
        object.__setattr__(self, "_run", run)
        object.__setattr__(self, "_resource", resource)

    def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
        if not isinstance(request, ExecutionRequest):
            raise ValueError("simulated IUT environment requires an execution request")
        visible = issue(
            self._visible,
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
            observable=classify_observable(request.action_id, visible),
            summary_confirmed=True,
            post_summary="q0",
            measurement_tick=Fraction(visible["tick"]),
            uncertainty_identity="sim-iut-u-1",
            evidence_ref=f"sim-iut:{request.execution_attempt_id}",
        )
        return EnvironmentExecution(record, self)


def _session(resource: ExclusiveResource) -> tuple[ReferenceSession, str]:
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
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="sim-iut-loop",
        run_id="sim-iut-loop-run",
        initial_summary="q0",
        resources=resources,
        retry_cap=4,
    )
    return session, head


def run_cl_loop(
    target: AlgorithmVisibleTarget,
    initial: dict[str, str],
    resource: ExclusiveResource,
    *,
    correlation_id: str,
) -> ArmRun:
    """Closed loop: analysis-guided next action via existing ReferenceSession."""

    run = ArmRun("CL-LOOP", resource_mode=resource.mode, resource_remaining=resource.remaining)
    session, head = _session(resource)
    run.runtime_session_type = type(session).__qualname__
    run.runtime_binding_sha = head
    if run.runtime_session_type != "ReferenceSession":
        raise RuntimeError("CL-LOOP must construct cltav_runtime.session.ReferenceSession")
    environment = SimulatedIutEnvironment(target, correlation_id, run, resource)
    seed = predetermined_test_sequence(initial)
    result = session.run(environment, maximum_rounds=max(1, len(seed) + 2))
    run.resource_remaining = resource.remaining
    run.analysis_notes = {
        "usedInitialFields": sorted(initial.keys()),
        "referenceSession": run.runtime_session_type,
        "runtimeStop": result.stop_reason,
        "runtimeBindingSha": head,
    }
    declare_arm_result(run, session_stop=result.stop_reason or "Stop-Error")
    return run
