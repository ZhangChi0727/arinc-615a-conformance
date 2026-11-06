"""A-stage feasibility witnesses for the bounded 615A scenario package.

The tests intentionally construct only a small, package-derived finite
projection. They do not implement a DATA-LOADER, target hardware, parser,
network, solver, or real experiment. The projection exists solely to prove
that the accepted session seam can consume the new package's actual action
IDs/public outcomes, retain a typed successor after a post-dispatch error, and
enter the honest P3-unavailable route.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
import json
from pathlib import Path

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState
from cltav_runtime.synthetic import (
    EnvironmentExecution,
    ExecutionRequest,
    PrepRecoverResult,
    SyntheticEnvironment,
    VisibleExecutionRecord,
)


ROOT = Path(__file__).resolve().parents[2]
SCENARIO_PACKAGE = ROOT / "configs/engineering/cltav_615a_scenarios.json"
DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
INTERFACE_PATH = "configs/research/cltav_interface_registry.json"
INSPECT_ACTION_ID = "ACT-INSPECT-NO-WRQ-BEFORE-READY"
PREP_ACTION_ID = "ACT-PREP-ENTER-READY-WINDOW"
ORDER_TEST_ACTION_ID = "ACT-TEST-ACK-BEFORE-DATA"
RECOVER_ACTION_ID = "ACT-RECOVER-RECONFIRM-READY"


@dataclass(frozen=True)
class _PublicJournalEvent:
    """One ordered, algorithm-visible A-stage journal entry.

    This tiny DTO intentionally belongs to the feasibility seam rather than a
    future loader or network implementation.  It is sufficient to prove that
    the package's declared public projection really consumes session,
    correlation, sequence and event inputs instead of copying an expected
    outcome into a synthetic return record.
    """

    session_id: str
    correlation_id: str
    sequence_number: int
    event_id: str


@dataclass(frozen=True)
class _PublicCompletionReceipt:
    """A public completion receipt scoped to one bounded journal prefix."""

    session_id: str
    correlation_id: str
    completion_receipt: str
    completed: bool
    prefix_start: int
    prefix_end: int


@dataclass(frozen=True)
class _ActionPublicMaterial:
    """The public material available to one admitted A-stage action."""

    action_id: str
    journal: tuple[_PublicJournalEvent, ...]
    receipt: _PublicCompletionReceipt | None


@dataclass(frozen=True)
class _PublicProjection:
    """The only test-side adapter result permitted to enter ReferenceSession."""

    confirmed: bool
    observable: str | None
    post_summary: str | None
    compatible_hypotheses: tuple[str, ...]


def _unconfirmed_projection() -> _PublicProjection:
    return _PublicProjection(False, None, None, ())


def _scenario_package() -> dict[str, object]:
    value = json.loads(SCENARIO_PACKAGE.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _require_mapping(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return value


def _action(package: dict[str, object], action_id: str) -> dict[str, object]:
    actions = package.get("actionLibrary")
    assert isinstance(actions, list)
    result = next(item for item in actions if isinstance(item, dict) and item.get("id") == action_id)
    assert isinstance(result, dict)
    return result


def _outcome(action: dict[str, object], observable: str) -> dict[str, object]:
    outcomes = action.get("possibleOutcomes")
    assert isinstance(outcomes, list)
    result = next(item for item in outcomes if isinstance(item, dict) and item.get("observable") == observable)
    assert isinstance(result, dict)
    return result


def _case(package: dict[str, object], case_id: str) -> dict[str, object]:
    cases = package.get("cases")
    assert isinstance(cases, list)
    result = next(item for item in cases if isinstance(item, dict) and item.get("id") == case_id)
    assert isinstance(result, dict)
    return result


def _members(package: dict[str, object]) -> list[dict[str, object]]:
    domain = _require_mapping(package.get("hypothesisDomain"))
    rows = domain.get("members")
    assert isinstance(rows, list) and rows
    result = [_require_mapping(row) for row in rows]
    assert all(isinstance(row.get("id"), str) and isinstance(row.get("kind"), str) for row in result)
    return result


def _authority_commit(package: dict[str, object]) -> str:
    identity = _require_mapping(package.get("identity"))
    value = identity.get("acceptedAuthorityCommit")
    assert isinstance(value, str) and len(value) == 40
    return value


def _action_cost(action: dict[str, object]) -> tuple[int, dict[str, int]]:
    declared = _require_mapping(action.get("cost"))
    charges = {
        "acquisition": declared.get("acquisition"),
        "computation": declared.get("computation"),
        "preparation": declared.get("preparation"),
        # The candidate package deliberately does not invent a separate
        # recovery accounting field. The existing seam projects its declared
        # preparation charge; this does not claim a real hardware cost.
        "recovery": 0,
        "retry": declared.get("retry"),
    }
    assert all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in charges.values())
    return max(1, sum(charges.values())), charges


def _finite_action(
    package: dict[str, object],
    action_id: str,
    *,
    state_id: str,
    member_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Map one declared scene action/outcome relation into the finite seam API."""

    declared = _action(package, action_id)
    inspection = _require_mapping(declared.get("inspection"))
    horizon = inspection.get("finiteHorizonTicks")
    assert isinstance(horizon, int) and not isinstance(horizon, bool) and horizon >= 0
    cost, charges = _action_cost(declared)
    outcomes = declared.get("possibleOutcomes")
    assert isinstance(outcomes, list) and outcomes
    emissions: dict[str, str] = {}
    for member in member_rows:
        member_id = member["id"]
        assert isinstance(member_id, str)
        matching = [
            candidate for candidate in outcomes
            if isinstance(candidate, dict) and member_id in candidate.get("compatibleHypotheses", [])
        ]
        # A summary-only Prep/Recover is committed by the existing S8/S9 path,
        # not by an observation class.  The finite API nevertheless requires a
        # total declaration for every model member, including EARLY-WRQ after a
        # predecessor that would normally have ruled it out.  Its package
        # outcome is a typed placeholder only; `_scenario_environment`
        # deliberately returns a summary-only typed result for those actions.
        if not matching and declared["kind"] in {"PREP", "RECOVER"} and len(outcomes) == 1:
            matching = outcomes
        # The order TEST is reached only after the bounded no-WRQ inspection
        # has removed EARLY-WRQ.  Retaining one total placeholder for the
        # initial finite model makes that fact explicit without claiming that
        # an EARLY-WRQ continuation is a valid order-check result.
        if not matching and declared["id"] == ORDER_TEST_ACTION_ID and outcomes:
            matching = [outcomes[0]]
        assert len(matching) == 1
        observable = matching[0].get("observable")
        assert isinstance(observable, str) and observable
        emissions[member_id] = observable
    finite: dict[str, object] = {
        "id": declared["id"],
        "kind": declared["kind"],
        "cost": cost,
        "detailCharges": charges,
        "enabledSummaries": {
            INSPECT_ACTION_ID: ["SCENE-ENTRY"],
            PREP_ACTION_ID: ["Q-PRE-READY-NO-WRQ"],
            ORDER_TEST_ACTION_ID: ["Q-TARGET-READY"],
            # Recover admission is selected only from UNKNOWN and ignores the
            # known-summary list; retain a syntactically valid unused value.
            RECOVER_ACTION_ID: ["RECOVER-ONLY-WHEN-UNKNOWN"],
        }[action_id],
        "transition": {
            "id": f"TR-{declared['id']}",
            "source": state_id,
            "target": state_id,
            "guardAst": {"tag": "TRUE"},
            "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": state_id}],
        },
        "observableByHypothesis": emissions,
        "measurementTicksByHypothesis": {member_id: horizon for member_id in emissions},
    }
    if declared["kind"] in {"PREP", "RECOVER"}:
        receipt = inspection.get("completionReceipt")
        assert isinstance(receipt, str) and receipt
        finite["declaredTarget"] = receipt
        finite["recoverWhenUnknown"] = declared["kind"] == "RECOVER"
    return finite


def _scenario_runtime_parts(
    package: dict[str, object],
    *,
    include_recover: bool,
) -> tuple[RuntimeAuthorityBinding, FiniteSessionModel]:
    """Construct a real binding plus a package-only finite seam projection.

    No test fixture supplies H, states, actions, observables, clock identity or
    resource charges here. The locally necessary AST self-loop is just the
    finite test harness transition; all externally visible identifiers come
    from the controlled scenario package.
    """

    commit = _authority_commit(package)
    binding = RuntimeAuthorityBinding.from_git_objects(
        repository=ROOT,
        development_commit=commit,
        development_path=DEVELOPMENT_PATH,
        interface_commit=commit,
        interface_path=INTERFACE_PATH,
    )
    snapshot = ContractSnapshot.from_git_object(
        repository=ROOT,
        contract_commit=commit,
        contract_path=DEVELOPMENT_PATH,
    )
    time = _require_mapping(package.get("timeAndObservation"))
    clock_id = time.get("virtualClockId")
    uncertainty_id = time.get("uncertaintyIdentity")
    assert isinstance(clock_id, str) and clock_id
    assert isinstance(uncertainty_id, str) and uncertainty_id
    members = _members(package)
    identity = _require_mapping(package.get("identity"))
    family = identity.get("scenarioFamilyId")
    assert isinstance(family, str) and family
    state_id = f"S-{family}-ENTRY"
    kinds = sorted({str(row["kind"]) for row in members})
    model_declaration = {
        "stateIds": [state_id],
        "clockIds": [clock_id],
        "typedDomains": {"scenarioKind": kinds},
    }
    context = ModelContext.build(
        snapshot=snapshot,
        model={
            "stateIds": set(model_declaration["stateIds"]),
            "clockIds": set(model_declaration["clockIds"]),
            "typedDomains": {"scenarioKind": set(kinds)},
        },
        projection_clock=clock_id,
    )
    hypotheses = [
        {
            "id": row["id"],
            "controlStateId": state_id,
            "clockConstraint": {
                clock_id: {
                    "lower": {"numerator": 0, "positiveDenominator": 1},
                    "upper": {"numerator": 0, "positiveDenominator": 1},
                    "lowerClosed": True,
                    "upperClosed": True,
                },
            },
            "typedStore": {"scenarioKind": row["kind"]},
        }
        for row in members
    ]
    action_ids = (
        [
            INSPECT_ACTION_ID,
            PREP_ACTION_ID,
            ORDER_TEST_ACTION_ID,
            RECOVER_ACTION_ID,
        ]
        if include_recover
        else [INSPECT_ACTION_ID]
    )
    actions = [
        _finite_action(package, action_id, state_id=state_id, member_rows=members)
        for action_id in action_ids
    ]
    model = {
        "model": model_declaration,
        "hypotheses": hypotheses,
        "actions": actions,
        "limits": {
            # The direct A11 witness needs one action.  The explicit A15
            # continuation intentionally proves four bounded S3--S9 rounds;
            # its test-only model therefore needs four finite transitions.
            "pathLength": 4 if include_recover else 2,
            "frontierStates": len(members),
            "hypotheses": len(members),
            "actions": len(actions),
            "observationClasses": len({
                observable
                for action in actions
                for observable in _require_mapping(action["observableByHypothesis"]).values()
            }),
        },
        "uncertainty": {
            "id": uncertainty_id,
            "clockId": clock_id,
            "timeUnit": "ticks",
            "maximumErrorTicks": 0,
        },
    }
    return binding, FiniteSessionModel.from_mapping(context=context, value=model)


def _projection_outcome(
    action: dict[str, object], observable: str,
) -> _PublicProjection:
    """Map a derived observable to its controlled package outcome relation."""

    outcome = _outcome(action, observable)
    post_summary = outcome.get("postSummary")
    compatible = outcome.get("compatibleHypotheses")
    assert isinstance(post_summary, str) and post_summary
    assert isinstance(compatible, list) and all(isinstance(value, str) and value for value in compatible)
    return _PublicProjection(True, observable, post_summary, tuple(compatible))


def _validated_completed_public_prefix(
    package: dict[str, object],
    request: ExecutionRequest,
    *,
    correlation_id: str,
    material: _ActionPublicMaterial | None,
) -> tuple[_PublicJournalEvent, ...] | None:
    """Return a valid current-session closed prefix independently of its meaning.

    ``None`` means that material is absent, malformed, incomplete, or belongs
    to a different action/session/correlation.  A tuple, including ``()``, is
    a completed public prefix that may be retained as an actual execution
    fact even when it is not yet sufficient to derive an observable summary.
    """

    if material is None or material.action_id != request.action_id:
        return None
    action = _action(package, request.action_id)
    derivation = _require_mapping(action.get("summaryDerivation"))
    contract = _require_mapping(derivation.get("publicEvidenceProjection"))
    inspection = _require_mapping(action.get("inspection"))
    receipt = material.receipt
    if receipt is None:
        return None
    canonical_empty_prefix = (
        not material.journal
        and receipt.prefix_start == 0
        and receipt.prefix_end == 0
    )
    ordinary_prefix = (
        isinstance(receipt.prefix_start, int)
        and not isinstance(receipt.prefix_start, bool)
        and receipt.prefix_start == 1
        and isinstance(receipt.prefix_end, int)
        and not isinstance(receipt.prefix_end, bool)
        and receipt.prefix_end >= 1
    )
    if (
        receipt.session_id != request.session_id
        or receipt.correlation_id != correlation_id
        or receipt.completion_receipt != contract.get("completionReceipt")
        or receipt.completion_receipt != inspection.get("completionReceipt")
        or receipt.completed is not True
        or not (ordinary_prefix or canonical_empty_prefix)
    ):
        return None

    journal = material.journal
    sequence_numbers = [event.sequence_number for event in journal]
    expected_sequence_numbers = (
        []
        if canonical_empty_prefix
        else list(range(receipt.prefix_start, receipt.prefix_end + 1))
    )
    if (
        any(
            event.session_id != request.session_id
            or event.correlation_id != correlation_id
            or not isinstance(event.event_id, str)
            or not event.event_id
            or not isinstance(event.sequence_number, int)
            or isinstance(event.sequence_number, bool)
            or event.sequence_number < receipt.prefix_start
            or event.sequence_number > receipt.prefix_end
            for event in journal
        )
        or sequence_numbers != sorted(sequence_numbers)
        or len(sequence_numbers) != len(set(sequence_numbers))
        or sequence_numbers != expected_sequence_numbers
        or receipt.prefix_end != (sequence_numbers[-1] if sequence_numbers else 0)
    ):
        return None
    return journal


def _project_public_summary(
    package: dict[str, object],
    request: ExecutionRequest,
    *,
    validated_prefix: tuple[_PublicJournalEvent, ...] | None,
    retained_prefix: tuple[_PublicJournalEvent, ...] = (),
    unresolved_public_action_id: str | None = None,
) -> _PublicProjection:
    """Derive one A-stage observable only after material validation.

    This intentionally tiny projector is a test-side feasibility witness, not
    a loader, protocol parser or network adapter.  It establishes that the
    A-package's bounded public-evidence contract can feed its real
    ``ReferenceSession`` seam without an expected outcome being copied into
    the execution fixture.  Structural public-prefix validity and semantic
    summary confirmation deliberately remain separate.
    """

    if validated_prefix is None:
        return _unconfirmed_projection()
    action = _action(package, request.action_id)
    journal = validated_prefix

    def first_position(event_id: str) -> int | None:
        return next(
            (event.sequence_number for event in journal if event.event_id == event_id),
            None,
        )

    def positions_after(event_id: str, lower_bound: int) -> tuple[int, ...]:
        return tuple(
            event.sequence_number
            for event in journal
            if event.event_id == event_id and event.sequence_number > lower_bound
        )

    if request.action_id == INSPECT_ACTION_ID:
        # The first visible WRQ controls the before-ready predicate.  A later
        # same-correlation WRQ must not overwrite an earlier fault witness.
        wrq = first_position("EV_DL_WRQ_LUR")
        ready = first_position("EV_TH_LUS0001")
        observable = (
            "EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001"
            if wrq is not None and (ready is None or wrq < ready)
            else "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001"
        )
        return _projection_outcome(action, observable)
    if request.action_id == PREP_ACTION_ID:
        if first_position("EV_TH_LUS0001") is None:
            return _unconfirmed_projection()
        return _projection_outcome(action, "EV_TH_LUS0001")
    if request.action_id == ORDER_TEST_ACTION_ID:
        wrq = first_position("EV_DL_WRQ_LUR")
        if wrq is None:
            return _unconfirmed_projection()
        data_after_wrq = positions_after("EV_DL_DATA_LUR", wrq)
        if not data_after_wrq:
            return _unconfirmed_projection()
        data = data_after_wrq[0]
        matching_ack_precedes_data = any(
            wrq < ack < data
            for ack in positions_after("EV_TH_ACK_LUR", wrq)
        )
        observable = (
            "WRQ-ACK-DATA-IN-ORDER"
            if matching_ack_precedes_data
            else "DATA-BEFORE-MATCHING-ACK"
        )
        return _projection_outcome(action, observable)
    if request.action_id == RECOVER_ACTION_ID:
        if unresolved_public_action_id is not None or not retained_prefix:
            return _unconfirmed_projection()
        prefix_length = len(retained_prefix)
        extension = journal[prefix_length:]
        if (
            journal[:prefix_length] != retained_prefix
            or len(extension) != 1
            or extension[0].event_id != "RECOVER-READY-READBACK"
            or extension[0].sequence_number != retained_prefix[-1].sequence_number + 1
        ):
            return _unconfirmed_projection()
        return _projection_outcome(action, "RECOVER-READY-READBACK")
    return _unconfirmed_projection()


def _unknown_effect_record(record: VisibleExecutionRecord) -> VisibleExecutionRecord:
    """Keep the actual successor but make a public confirmation unavailable."""

    return replace(
        record,
        effect_class="UNKNOWN-EFFECT",
        observable=None,
        summary_confirmed=False,
        post_summary=None,
        measurement_tick=None,
        uncertainty_identity=None,
        prep_recover=None,
    )


def _summary_only_record(
    record: VisibleExecutionRecord,
    *,
    projection: _PublicProjection,
    target_confirmed: bool,
) -> VisibleExecutionRecord:
    """Create a typed Prep/Recover return from the public projection."""

    result = record.prep_recover
    assert isinstance(result, PrepRecoverResult)
    assert projection.confirmed is True and projection.post_summary is not None
    return replace(
        record,
        observable=None,
        summary_confirmed=True,
        post_summary=projection.post_summary,
        measurement_tick=None,
        uncertainty_identity=None,
        prep_recover=PrepRecoverResult(
            target_confirmed=target_confirmed,
            summary_confirmed=True,
            prep_error=False,
            ineligible=False,
            declared_target=result.declared_target,
            evidence=f"public:{projection.observable}:{result.declared_target}",
            post_summary=projection.post_summary,
        ),
    )


def _unconfirmed_recovery_record(record: VisibleExecutionRecord) -> VisibleExecutionRecord:
    """A Recover read-back failure stays UNKNOWN rather than becoming KNOWN."""

    result = record.prep_recover
    assert isinstance(result, PrepRecoverResult)
    return replace(
        record,
        observable=None,
        summary_confirmed=False,
        post_summary=None,
        measurement_tick=None,
        uncertainty_identity=None,
        prep_recover=PrepRecoverResult(
            target_confirmed=False,
            summary_confirmed=False,
            prep_error=False,
            ineligible=False,
            declared_target=result.declared_target,
            evidence=f"public:unconfirmed:{result.declared_target}",
            post_summary=None,
        ),
    )


@dataclass(frozen=True)
class _LoaderScenarioEnvironment(SyntheticEnvironment):
    """Constrained, immutable A seam; this is not the future object model.

    ``public_materials`` are immutable action-scoped journal/receipt snapshots.
    ``retained_public_journal`` records the latest valid actual boundary;
    ``unresolved_public_action_id`` prevents an earlier boundary from being
    mistaken for a later action with missing or invalid public material.  The
    environment has no evaluator-fault label field, and a public result is
    derived only by ``_project_public_summary`` before it enters the accepted
    ReferenceSession seam.
    """

    correlation_id: str = ""
    public_materials: tuple[_ActionPublicMaterial, ...] = ()
    retained_public_journal: tuple[_PublicJournalEvent, ...] = ()
    unresolved_public_action_id: str | None = None
    visible_evidence_refs: tuple[str, ...] = ()
    loader_state: str = ""
    target_hardware_state: str = ""
    current_session_ready_receipt: str | None = None
    prep_branch: str = "confirmed"
    force_post_dispatch_summary_error: bool = False

    def _next(
        self,
        *,
        state: str | None = None,
        pending: VisibleExecutionRecord | None = None,
        retained_public_journal: tuple[_PublicJournalEvent, ...] | None = None,
        unresolved_public_action_id: str | None = None,
        evidence_refs: tuple[str, ...] | None = None,
        loader_state: str | None = None,
        target_hardware_state: str | None = None,
        ready_receipt: str | None = None,
    ) -> "_LoaderScenarioEnvironment":
        return _LoaderScenarioEnvironment(
            _state=state if state is not None else self._state,
            _uncertainty_identity=self._uncertainty_identity,
            _states=self._states,
            _pending_delivery=pending,
            correlation_id=self.correlation_id,
            public_materials=self.public_materials,
            retained_public_journal=(
                self.retained_public_journal
                if retained_public_journal is None
                else retained_public_journal
            ),
            unresolved_public_action_id=(
                self.unresolved_public_action_id
                if unresolved_public_action_id is None
                else unresolved_public_action_id
            ),
            visible_evidence_refs=(
                self.visible_evidence_refs if evidence_refs is None else evidence_refs
            ),
            loader_state=self.loader_state if loader_state is None else loader_state,
            target_hardware_state=(
                self.target_hardware_state
                if target_hardware_state is None
                else target_hardware_state
            ),
            current_session_ready_receipt=(
                self.current_session_ready_receipt if ready_receipt is None else ready_receipt
            ),
            prep_branch=self.prep_branch,
            force_post_dispatch_summary_error=self.force_post_dispatch_summary_error,
        )

    def with_pending_delivery(self, record: VisibleExecutionRecord) -> "_LoaderScenarioEnvironment":
        if self._pending_delivery is not None:
            raise ValueError("scenario seam already has an unconsumed pending delivery")
        return self._next(pending=record)

    def take_pending_delivery(self) -> tuple[VisibleExecutionRecord, "_LoaderScenarioEnvironment"] | None:
        if self._pending_delivery is None:
            return None
        return self._pending_delivery, self._next()

    def _material(self, action_id: str) -> _ActionPublicMaterial | None:
        matching = [item for item in self.public_materials if item.action_id == action_id]
        return matching[0] if len(matching) == 1 else None

    def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
        execution = super().execute(request)
        record = execution.record
        material = self._material(request.action_id)
        package = _scenario_package()
        validated_prefix = _validated_completed_public_prefix(
            package,
            request,
            correlation_id=self.correlation_id,
            material=material,
        )
        projection = _project_public_summary(
            package,
            request,
            validated_prefix=validated_prefix,
            retained_prefix=self.retained_public_journal,
            unresolved_public_action_id=self.unresolved_public_action_id,
        )
        retained_public_journal = self.retained_public_journal
        unresolved_public_action_id = self.unresolved_public_action_id
        ready_receipt = self.current_session_ready_receipt
        loader_state = self.loader_state
        target_state = self.target_hardware_state

        if request.action_id == INSPECT_ACTION_ID:
            if not projection.confirmed:
                record = _unknown_effect_record(record)
            else:
                record = replace(
                    record,
                    observable=projection.observable,
                    summary_confirmed=True,
                    post_summary=projection.post_summary,
                )
            loader_state = "LOADER-INSPECTION-COMPLETE"
            target_state = "TH-STATE-PRESERVED-DURING-INSPECTION"
        elif request.action_id == PREP_ACTION_ID:
            if self.prep_branch == "confirmedNotSent":
                record = replace(
                    record,
                    effect_class="CONFIRMED-NOT-SENT",
                    observable=None,
                    summary_confirmed=False,
                    post_summary=None,
                    measurement_tick=None,
                    uncertainty_identity=None,
                    prep_recover=None,
                )
                # A confirmed non-send has no object transition.  Return the
                # same immutable environment rather than the base successor.
                return EnvironmentExecution(record, self)
            if self.prep_branch == "executedSummaryUnconfirmed" or not projection.confirmed:
                record = _unknown_effect_record(record)
                loader_state = "LOADER-READY-WINDOW-EXECUTED-UNCONFIRMED"
                target_state = "TH-READY-MAY-HAVE-ADVANCED"
            else:
                record = _summary_only_record(
                    record,
                    projection=projection,
                    target_confirmed=self.prep_branch != "targetNotReachedWithConfirmedSuccessor",
                )
                ready_receipt = _require_mapping(_action(_scenario_package(), PREP_ACTION_ID)["inspection"])["completionReceipt"]
                assert isinstance(ready_receipt, str)
                loader_state = "LOADER-READY-WINDOW-ENTERED"
                target_state = "TH-READY-RECEIPT-RETAINED"
        elif request.action_id == ORDER_TEST_ACTION_ID:
            if not projection.confirmed:
                record = _unknown_effect_record(record)
            else:
                record = replace(
                    record,
                    observable=projection.observable,
                    summary_confirmed=True,
                    post_summary=projection.post_summary,
                )
                if self.force_post_dispatch_summary_error:
                    # Deliberately emulate an adapter that loses the returned
                    # summary after dispatch.  The session must retain the
                    # actual successor and enter UNKNOWN rather than rewind.
                    record = replace(record, post_summary=None)
            loader_state = "LOADER-CONTROL-STEP-ISSUED"
            target_state = "TH-CONTROL-STEP-MAY-HAVE-ADVANCED"
        elif request.action_id == RECOVER_ACTION_ID:
            if not projection.confirmed:
                record = _unconfirmed_recovery_record(record)
            else:
                record = _summary_only_record(record, projection=projection, target_confirmed=True)
                ready_receipt = _require_mapping(_action(_scenario_package(), RECOVER_ACTION_ID)["inspection"])["completionReceipt"]
                assert isinstance(ready_receipt, str)
                loader_state = "LOADER-READY-RECONFIRMED"
                target_state = "TH-READY-READBACK-RETAINED"

        # Retention records an actual, valid completed public prefix; it is
        # deliberately independent from whether that prefix was informative
        # enough to derive an observable/post-summary.  A malformed or absent
        # action material leaves a named unresolved execution boundary so that
        # Recover cannot silently reuse an earlier checkpoint.  A structurally
        # valid but non-extending Recover also cannot replace that checkpoint;
        # it may remain retryable with the real retained prefix.
        if validated_prefix is None:
            unresolved_public_action_id = request.action_id
        elif request.action_id == RECOVER_ACTION_ID:
            if projection.confirmed and unresolved_public_action_id is None:
                retained_public_journal = validated_prefix
        elif unresolved_public_action_id is None:
            retained_public_journal = validated_prefix

        successor = self._next(
            state=execution.successor._state,
            retained_public_journal=retained_public_journal,
            unresolved_public_action_id=unresolved_public_action_id,
            evidence_refs=self.visible_evidence_refs + (record.evidence_ref,),
            loader_state=loader_state,
            target_hardware_state=target_state,
            ready_receipt=ready_receipt,
        )
        return EnvironmentExecution(record, successor)


def _public_materials(
    package: dict[str, object], *, session_id: str, correlation_id: str,
) -> tuple[_ActionPublicMaterial, ...]:
    """Return bounded current-session snapshots for the four A actions."""

    def material(action_id: str, events: tuple[str, ...]) -> _ActionPublicMaterial:
        action = _action(package, action_id)
        receipt = _require_mapping(action["inspection"])["completionReceipt"]
        assert isinstance(receipt, str)
        journal = tuple(
            _PublicJournalEvent(session_id, correlation_id, index, event)
            for index, event in enumerate(events, start=1)
        )
        return _ActionPublicMaterial(
            action_id,
            journal,
            _PublicCompletionReceipt(
                session_id,
                correlation_id,
                receipt,
                True,
                1,
                len(journal),
            ),
        )

    prefix = ("EV_DL_OFFER_LIST",)
    return (
        material(INSPECT_ACTION_ID, prefix),
        material(PREP_ACTION_ID, prefix + ("EV_TH_LUS0001",)),
        material(
            ORDER_TEST_ACTION_ID,
            prefix + ("EV_TH_LUS0001", "EV_DL_WRQ_LUR", "EV_TH_ACK_LUR", "EV_DL_DATA_LUR"),
        ),
        material(
            RECOVER_ACTION_ID,
            prefix
            + (
                "EV_TH_LUS0001",
                "EV_DL_WRQ_LUR",
                "EV_TH_ACK_LUR",
                "EV_DL_DATA_LUR",
                "RECOVER-READY-READBACK",
            ),
        ),
    )


def _replace_material(
    materials: tuple[_ActionPublicMaterial, ...],
    replacement: _ActionPublicMaterial,
) -> tuple[_ActionPublicMaterial, ...]:
    return tuple(
        replacement if item.action_id == replacement.action_id else item
        for item in materials
    )


def _scenario_environment(
    package: dict[str, object],
    model: FiniteSessionModel,
    *,
    session_id: str = "scenario-session",
    correlation_id: str = "scenario-current-lur-start",
    public_materials: tuple[_ActionPublicMaterial, ...] | None = None,
    prep_branch: str = "confirmed",
    force_post_dispatch_summary_error: bool = False,
) -> _LoaderScenarioEnvironment:
    inspect = _action(package, INSPECT_ACTION_ID)
    inspect_outcome = _outcome(inspect, "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001")
    prep = _action(package, PREP_ACTION_ID)
    prep_outcome = _outcome(prep, "EV_TH_LUS0001")
    order_test = _action(package, ORDER_TEST_ACTION_ID)
    order_outcome = _outcome(order_test, "WRQ-ACK-DATA-IN-ORDER")
    recover = _action(package, RECOVER_ACTION_ID)
    recover_outcome = _outcome(recover, "RECOVER-READY-READBACK")

    def test_outcome(
        action: dict[str, object], outcome: dict[str, object], next_state: str,
    ) -> dict[str, object]:
        return {
            "effectClass": "NONE",
            "observable": outcome["observable"],
            "summaryConfirmed": True,
            "postSummary": outcome["postSummary"],
            "measurementTick": _require_mapping(action["inspection"])["finiteHorizonTicks"],
            "nextPrivateState": next_state,
        }

    def summary_outcome(
        action: dict[str, object], outcome: dict[str, object], next_state: str,
    ) -> dict[str, object]:
        receipt = _require_mapping(action["inspection"])["completionReceipt"]
        assert isinstance(receipt, str)
        return {
            "effectClass": "NONE",
            "observable": None,
            "summaryConfirmed": True,
            "postSummary": outcome["postSummary"],
            "measurementTick": None,
            "nextPrivateState": next_state,
            "prepRecover": {
                "targetConfirmed": True,
                "summaryConfirmed": True,
                "prepError": False,
                "ineligible": False,
                "declaredTarget": receipt,
                "evidence": f"current-session:{outcome['observable']}:{receipt}",
                "postSummary": outcome["postSummary"],
            },
        }

    states = {
        "LOADER-PRE-READY": {
            INSPECT_ACTION_ID: test_outcome(
                inspect, inspect_outcome, "LOADER-AFTER-INSPECTION",
            ),
        },
        "LOADER-AFTER-INSPECTION": {
            PREP_ACTION_ID: summary_outcome(
                prep, prep_outcome, "LOADER-AFTER-PREP",
            ),
        },
        "LOADER-AFTER-PREP": {
            ORDER_TEST_ACTION_ID: test_outcome(
                order_test, order_outcome, "LOADER-AFTER-TEST",
            ),
        },
        "LOADER-AFTER-TEST": {
            RECOVER_ACTION_ID: summary_outcome(
                recover, recover_outcome, "LOADER-RECOVERED",
            ),
        },
        "LOADER-RECOVERED": {
            RECOVER_ACTION_ID: summary_outcome(
                recover, recover_outcome, "LOADER-RECOVERED",
            ),
        },
    }
    source = {
        "initialPrivateState": "LOADER-PRE-READY",
        "uncertaintyIdentity": model.uncertainty_identity,
        "states": states,
    }
    base = SyntheticEnvironment.from_mapping(source)
    return _LoaderScenarioEnvironment(
        _state=base._state,
        _uncertainty_identity=base._uncertainty_identity,
        _states=base._states,
        _pending_delivery=None,
        correlation_id=correlation_id,
        public_materials=(
            _public_materials(package, session_id=session_id, correlation_id=correlation_id)
            if public_materials is None
            else public_materials
        ),
        visible_evidence_refs=(),
        loader_state="LOADER-LIST-OFFERED",
        target_hardware_state="TH-AWAITING-CURRENT-SESSION-WRQ",
        current_session_ready_receipt=None,
        prep_branch=prep_branch,
        force_post_dispatch_summary_error=force_post_dispatch_summary_error,
    )


def _run_public_inspection(
    package: dict[str, object],
    *,
    session_id: str,
    materials: tuple[_ActionPublicMaterial, ...] | None = None,
) -> tuple[object, ...]:
    """Run the package's public no-WRQ projection through ReferenceSession."""

    binding, model = _scenario_runtime_parts(package, include_recover=False)
    environment = _scenario_environment(
        package,
        model,
        session_id=session_id,
        public_materials=materials,
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id=session_id,
        run_id=session_id,
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(2),
        retry_cap=2,
    )
    result = session.step(session.initial_state, environment)
    evidence = result.state.evidence[-1]
    snapshot = evidence.snapshot
    # Keep every A-level consumer-visible outcome, not merely a summary.  This
    # makes public material mutations observable through the real session seam.
    return (
        evidence.execution.action_id,
        snapshot.action_id,
        tuple((item.observable, tuple(sorted(item.hypotheses))) for item in snapshot.classes),
        result.state.history.hypotheses,
        result.state.history.status_by_hypothesis,
        result.state.history.version,
        evidence.resource_before,
        evidence.resource_after,
        tuple(sorted(evidence.detail_charges.items())),
        tuple(sorted(evidence.projected_cost.items())),
        result.stop_reason,
        evidence.execution.observable,
        evidence.execution.post_summary,
        result.state.context.current_summary,
        result.state.context.q_status,
        result.state.evidence[-1].resolution_code,
    )


def _inspection_result(
    package: dict[str, object],
    *,
    session_id: str,
    materials: tuple[_ActionPublicMaterial, ...] | None = None,
) -> tuple[object, ReferenceSession, _LoaderScenarioEnvironment, object]:
    """Return the full first-step result for public-material negative tests."""

    binding, model = _scenario_runtime_parts(package, include_recover=False)
    environment = _scenario_environment(
        package,
        model,
        session_id=session_id,
        public_materials=materials,
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id=session_id,
        run_id=session_id,
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(2),
        retry_cap=2,
    )
    return session.step(session.initial_state, environment), session, environment, model


def test_a11_finite_normal_test_returns_package_public_summary_and_exact_tick() -> None:
    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=False)
    assert binding.development.contract_commit == _authority_commit(package)
    session_id = "scenario-finite-test"
    environment = _scenario_environment(package, model, session_id=session_id)
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id=session_id,
        run_id=session_id,
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(1),
        retry_cap=1,
    )
    result = session.step(session.initial_state, environment)
    evidence = result.state.evidence[-1]
    inspect = _action(package, INSPECT_ACTION_ID)
    no_wrq = _outcome(inspect, "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001")
    assert evidence.execution.action_id == INSPECT_ACTION_ID
    assert evidence.execution.observable == no_wrq["observable"]
    assert evidence.execution.summary_confirmed is True
    assert evidence.execution.post_summary == no_wrq["postSummary"]
    assert evidence.execution.measurement_tick == Fraction(
        _require_mapping(inspect["inspection"])["finiteHorizonTicks"],
    )
    assert evidence.execution.response_id is None and evidence.execution.observation_input is None
    assert evidence.observation_assessment is None
    assert all("NO-RESPONSE" not in diagnostic.code for diagnostic in result.diagnostics)
    assert result.state.history.hypotheses == frozenset({"NORMAL", "EARLY-DATA"})


def test_a12_public_projection_has_no_evaluator_label_input_and_preserves_full_result() -> None:
    package = _scenario_package()
    inspect = _action(package, INSPECT_ACTION_ID)
    derivation = _require_mapping(inspect["summaryDerivation"])
    forbidden = derivation.get("forbiddenPrivateSources")
    assert isinstance(forbidden, list) and "ACTIVE-FAULT-ID" in forbidden
    assert "evaluator_only_fault_label" not in _LoaderScenarioEnvironment.__dataclass_fields__

    # Repeating the identical public evidence is deterministic.  The external
    # metadata below is intentionally never an input of the environment or
    # projector; type-level absence above is the isolation assertion.
    session_id = "scenario-public-input"
    same_public_material = _public_materials(
        package,
        session_id=session_id,
        correlation_id="scenario-current-lur-start",
    )
    normal_first = _run_public_inspection(
        package, session_id=session_id, materials=same_public_material,
    )
    normal_second = _run_public_inspection(
        package, session_id=session_id, materials=same_public_material,
    )
    assert normal_first == normal_second

    # A genuinely empty completed prefix is a valid bounded inspection input;
    # it is not itself an error or an assertion of a protocol timeout.
    original = next(item for item in same_public_material if item.action_id == INSPECT_ACTION_ID)
    assert original.receipt is not None
    empty_material = _ActionPublicMaterial(
        INSPECT_ACTION_ID,
        (),
        replace(original.receipt, prefix_start=0, prefix_end=0),
    )
    empty_result = _run_public_inspection(
        package,
        session_id=session_id,
        materials=_replace_material(same_public_material, empty_material),
    )
    assert empty_result[-5:] == (
        "NO-EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
        "Q-PRE-READY-NO-WRQ",
        "Q-PRE-READY-NO-WRQ",
        "KNOWN",
        "COMMIT",
    )

    # The first WRQ is before ready while a second same-correlation WRQ occurs
    # after ready.  This guards against a dict-style overwrite that would hide
    # the early public fact and incorrectly derive the no-WRQ outcome.
    early_journal = (
        _PublicJournalEvent(session_id, "scenario-current-lur-start", 1, "EV_DL_OFFER_LIST"),
        _PublicJournalEvent(session_id, "scenario-current-lur-start", 2, "EV_DL_WRQ_LUR"),
        _PublicJournalEvent(session_id, "scenario-current-lur-start", 3, "EV_TH_LUS0001"),
        _PublicJournalEvent(session_id, "scenario-current-lur-start", 4, "EV_DL_WRQ_LUR"),
    )
    early_receipt = _PublicCompletionReceipt(
        session_id,
        "scenario-current-lur-start",
        original.receipt.completion_receipt if original.receipt is not None else "",
        True,
        1,
        4,
    )
    early_material = _ActionPublicMaterial(INSPECT_ACTION_ID, early_journal, early_receipt)
    early_result = _run_public_inspection(
        package,
        session_id=session_id,
        materials=_replace_material(same_public_material, early_material),
    )
    assert early_result != normal_first
    assert early_result[-5:] == (
        "EV_DL_WRQ_LUR-BEFORE-EV_TH_LUS0001",
        "Q-EARLY-WRQ-OBSERVED",
        "Q-EARLY-WRQ-OBSERVED",
        "KNOWN",
        "COMMIT",
    )


def test_a12b_invalid_public_receipts_become_unknown_without_a_summary_commit() -> None:
    package = _scenario_package()
    session_id = "scenario-invalid-public-receipt"
    correlation_id = "scenario-current-lur-start"
    materials = _public_materials(package, session_id=session_id, correlation_id=correlation_id)
    current = next(item for item in materials if item.action_id == INSPECT_ACTION_ID)
    assert current.receipt is not None
    invalid_materials = (
        _ActionPublicMaterial(INSPECT_ACTION_ID, current.journal, None),
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            current.journal,
            replace(current.receipt, completed=False),
        ),
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            current.journal,
            replace(current.receipt, session_id="another-session"),
        ),
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            current.journal,
            replace(current.receipt, correlation_id="other-correlation"),
        ),
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            (replace(current.journal[0], session_id="foreign-journal-session"),),
            current.receipt,
        ),
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            current.journal,
            replace(current.receipt, prefix_end=0),
        ),
        # A completed receipt claims a closed [1, 2] prefix, but the first
        # available event is 2.  The projector must not treat this as a
        # generic "no WRQ" observation and silently shrink H.
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            (replace(current.journal[0], sequence_number=2),),
            replace(current.receipt, prefix_start=1, prefix_end=2),
        ),
        # The same witness with a missing middle event: a receipt for [1, 3]
        # cannot be confirmed from journal entries 1 and 3 alone.
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            (
                current.journal[0],
                replace(current.journal[0], sequence_number=3),
            ),
            replace(current.receipt, prefix_start=1, prefix_end=3),
        ),
        # Nor may a receipt for [1, 2] accept a prefix with its endpoint
        # absent, even though the remaining event happens to support no WRQ.
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            current.journal,
            replace(current.receipt, prefix_start=1, prefix_end=2),
        ),
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            (
                current.journal[0],
                replace(current.journal[0], sequence_number=1),
            ),
            replace(current.receipt, prefix_start=1, prefix_end=1),
        ),
        _ActionPublicMaterial(
            INSPECT_ACTION_ID,
            (replace(current.journal[0], sequence_number=3),),
            replace(current.receipt, prefix_start=1, prefix_end=2),
        ),
    )
    for invalid in invalid_materials:
        result, _session, _environment, _model = _inspection_result(
            package,
            session_id=session_id,
            materials=_replace_material(materials, invalid),
        )
        evidence = result.state.evidence[-1]
        assert evidence.execution.effect_class == "UNKNOWN-EFFECT"
        assert evidence.resolution_code == "UNKNOWN-EFFECT"
        assert result.state.context.q_status == "UNKNOWN"
        assert result.state.context.current_summary is None
        assert result.state.history.hypotheses == frozenset({"NORMAL", "EARLY-WRQ", "EARLY-DATA"})
        assert type(result.environment) is _LoaderScenarioEnvironment
        assert result.environment._state == "LOADER-AFTER-INSPECTION"


def test_a12c_order_projection_classifies_first_data_without_matching_ack_as_early_data() -> None:
    """Exercise both normal and early order witnesses through ReferenceSession.

    This is deliberately a public-journal seam test, not a simulated timeout.
    A completed prefix that reaches DATA before a matching ACK establishes the
    EARLY-DATA observation whether or not a later ACK is present; absent WRQ
    or absent DATA instead leaves the result UNKNOWN.
    """

    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=True)

    def run_order_case(
        case_id: str,
        event_ids: tuple[str, ...],
    ) -> object:
        session_id = f"scenario-order-{case_id}"
        correlation_id = "scenario-current-lur-start"
        materials = _public_materials(
            package,
            session_id=session_id,
            correlation_id=correlation_id,
        )
        base = next(item for item in materials if item.action_id == ORDER_TEST_ACTION_ID)
        assert base.receipt is not None
        order_material = _ActionPublicMaterial(
            ORDER_TEST_ACTION_ID,
            tuple(
                _PublicJournalEvent(session_id, correlation_id, index, event_id)
                for index, event_id in enumerate(event_ids, start=1)
            ),
            replace(base.receipt, prefix_start=1, prefix_end=len(event_ids)),
        )
        environment = _scenario_environment(
            package,
            model,
            session_id=session_id,
            correlation_id=correlation_id,
            public_materials=_replace_material(materials, order_material),
        )
        session = ReferenceSession(
            binding=binding,
            model=model,
            session_id=session_id,
            run_id=session_id,
            initial_summary="SCENE-ENTRY",
            resources=ResourceState.rounds(4),
            retry_cap=4,
        )
        inspected = session.step(session.initial_state, environment)
        prepared = session.step(inspected.state, inspected.environment)
        assert prepared.state.context.current_summary == "Q-TARGET-READY"
        return session.step(prepared.state, prepared.environment)

    normal = run_order_case(
        "ack-before-data",
        (
            "EV_DL_OFFER_LIST",
            "EV_TH_LUS0001",
            "EV_DL_WRQ_LUR",
            "EV_TH_ACK_LUR",
            "EV_DL_DATA_LUR",
        ),
    )
    normal_evidence = normal.state.evidence[-1]
    # A singleton is a normal finite-session stop, not a timeout or a FAIL.
    assert normal.stop_reason == "Stop-Singleton"
    assert normal_evidence.snapshot.action_id == ORDER_TEST_ACTION_ID
    assert normal_evidence.execution.observable == "WRQ-ACK-DATA-IN-ORDER"
    assert normal_evidence.resolution_code == "COMMIT"
    assert normal.state.context.q_status == "KNOWN"
    assert normal.state.history.hypotheses == frozenset({"NORMAL"})

    for case_id, event_ids in (
        (
            "data-before-ack",
            (
                "EV_DL_OFFER_LIST",
                "EV_TH_LUS0001",
                "EV_DL_WRQ_LUR",
                "EV_DL_DATA_LUR",
            ),
        ),
        (
            "data-before-late-ack",
            (
                "EV_DL_OFFER_LIST",
                "EV_TH_LUS0001",
                "EV_DL_WRQ_LUR",
                "EV_DL_DATA_LUR",
                "EV_TH_ACK_LUR",
            ),
        ),
    ):
        early = run_order_case(case_id, event_ids)
        early_evidence = early.state.evidence[-1]
        # A later ACK cannot rewrite the already observed DATA-first order.
        assert early.stop_reason == "Stop-Singleton"
        assert early_evidence.execution.observable == "DATA-BEFORE-MATCHING-ACK"
        assert early_evidence.resolution_code == "COMMIT"
        assert early.state.context.q_status == "KNOWN"
        assert early.state.context.current_summary == "Q-LUR-ORDER-ASSESSED"
        assert early.state.history.hypotheses == frozenset({"EARLY-DATA"})

    for case_id, event_ids in (
        (
            "missing-wrq",
            (
                "EV_DL_OFFER_LIST",
                "EV_TH_LUS0001",
                "EV_TH_ACK_LUR",
                "EV_DL_DATA_LUR",
            ),
        ),
        (
            "incomplete-before-data",
            (
                "EV_DL_OFFER_LIST",
                "EV_TH_LUS0001",
                "EV_DL_WRQ_LUR",
                "EV_TH_ACK_LUR",
            ),
        ),
    ):
        unconfirmed = run_order_case(case_id, event_ids)
        unconfirmed_evidence = unconfirmed.state.evidence[-1]
        assert unconfirmed.stop_reason is None
        assert unconfirmed_evidence.execution.observable is None
        assert unconfirmed_evidence.resolution_code == "UNKNOWN-EFFECT"
        assert unconfirmed.state.context.q_status == "UNKNOWN"
        assert unconfirmed.state.context.current_summary is None
        assert unconfirmed.state.history.hypotheses == frozenset({"NORMAL", "EARLY-DATA"})
        assert all("NO-RESPONSE" not in diagnostic.code for diagnostic in unconfirmed.diagnostics)
        assert all("FAIL" not in diagnostic.code for diagnostic in unconfirmed.diagnostics)


def test_a12d_unconfirmed_complete_order_prefix_is_retained_and_controls_recover() -> None:
    """Keep an executed, valid no-DATA prefix distinct from its unknown summary.

    A completed LIST/READY/WRQ/ACK prefix is structurally valid but does not
    yet establish either normal order or EARLY-DATA.  The actual four-event
    boundary must nevertheless be retained for Recover.  In contrast, an
    absent or malformed current TEST material creates a named unresolved
    boundary that an old Prep prefix cannot silently close.
    """

    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=True)

    def fresh_materials(
        session_id: str,
    ) -> tuple[tuple[_ActionPublicMaterial, ...], str]:
        correlation_id = "scenario-current-lur-start"
        return _public_materials(
            package,
            session_id=session_id,
            correlation_id=correlation_id,
        ), correlation_id

    def action_material(
        base: _ActionPublicMaterial,
        action_id: str,
        journal: tuple[_PublicJournalEvent, ...],
        *,
        completed: bool = True,
    ) -> _ActionPublicMaterial:
        assert base.receipt is not None
        return _ActionPublicMaterial(
            action_id,
            journal,
            replace(
                base.receipt,
                completed=completed,
                prefix_start=1,
                prefix_end=len(journal),
            ),
        )

    def run_to_order(
        case_id: str,
        materials: tuple[_ActionPublicMaterial, ...],
        correlation_id: str,
    ) -> tuple[ReferenceSession, object, object]:
        session_id = f"scenario-retained-prefix-{case_id}"
        environment = _scenario_environment(
            package,
            model,
            session_id=session_id,
            correlation_id=correlation_id,
            public_materials=materials,
        )
        session = ReferenceSession(
            binding=binding,
            model=model,
            session_id=session_id,
            run_id=session_id,
            initial_summary="SCENE-ENTRY",
            resources=ResourceState.rounds(4),
            retry_cap=4,
        )
        inspected = session.step(session.initial_state, environment)
        prepared = session.step(inspected.state, inspected.environment)
        assert prepared.state.context.current_summary == "Q-TARGET-READY"
        return session, prepared, session.step(prepared.state, prepared.environment)

    # The semantic order is unconfirmed because DATA is absent, but this is a
    # valid completed current-session prefix and therefore an actual boundary.
    session_id = "scenario-retained-prefix-no-data"
    materials, correlation_id = fresh_materials(session_id)
    base_order = next(item for item in materials if item.action_id == ORDER_TEST_ACTION_ID)
    no_data_journal = tuple(
        _PublicJournalEvent(session_id, correlation_id, index, event_id)
        for index, event_id in enumerate(
            (
                "EV_DL_OFFER_LIST",
                "EV_TH_LUS0001",
                "EV_DL_WRQ_LUR",
                "EV_TH_ACK_LUR",
            ),
            start=1,
        )
    )
    no_data_order = action_material(base_order, ORDER_TEST_ACTION_ID, no_data_journal)
    materials = _replace_material(materials, no_data_order)
    session, prepared, unknown = run_to_order("no-data", materials, correlation_id)
    unknown_evidence = unknown.state.evidence[-1]
    assert unknown_evidence.snapshot.action_id == ORDER_TEST_ACTION_ID
    assert unknown_evidence.resolution_code == "UNKNOWN-EFFECT"
    assert unknown.stop_reason is None
    assert unknown.state.context.q_status == "UNKNOWN"
    assert unknown.state.context.current_summary is None
    assert unknown.state.history.hypotheses == frozenset({"NORMAL", "EARLY-DATA"})
    assert type(unknown.environment) is _LoaderScenarioEnvironment
    assert unknown.environment._state == "LOADER-AFTER-TEST"
    assert unknown.environment.loader_state == "LOADER-CONTROL-STEP-ISSUED"
    assert unknown.environment.retained_public_journal == no_data_journal
    assert unknown.environment.unresolved_public_action_id is None
    assert all("NO-RESPONSE" not in diagnostic.code for diagnostic in unknown.diagnostics)
    assert all("FAIL" not in diagnostic.code for diagnostic in unknown.diagnostics)

    base_recover = next(item for item in materials if item.action_id == RECOVER_ACTION_ID)

    def with_readback(
        prefix: tuple[_PublicJournalEvent, ...],
    ) -> tuple[_PublicJournalEvent, ...]:
        return prefix + (
            _PublicJournalEvent(
                session_id,
                correlation_id,
                len(prefix) + 1,
                "RECOVER-READY-READBACK",
            ),
        )

    def recover_material_for(
        journal: tuple[_PublicJournalEvent, ...],
    ) -> _ActionPublicMaterial:
        return action_material(base_recover, RECOVER_ACTION_ID, journal)

    # The actual four-event checkpoint plus exactly one ready readback closes
    # Recover; the result is an explicit re-confirmation, not a replay.
    actual_recover = recover_material_for(with_readback(no_data_journal))
    recovered = session.step(
        unknown.state,
        replace(
            unknown.environment,
            public_materials=_replace_material(unknown.environment.public_materials, actual_recover),
        ),
    )
    recovered_evidence = recovered.state.evidence[-1]
    assert recovered_evidence.snapshot.action_id == RECOVER_ACTION_ID
    assert recovered_evidence.resolution_code == "COMMIT"
    assert recovered.state.context.q_status == "KNOWN"
    assert recovered.state.context.current_summary == "Q-TARGET-READY"
    assert recovered.state.history.hypotheses == unknown.state.history.hypotheses
    assert type(recovered.environment) is _LoaderScenarioEnvironment
    assert recovered.environment.loader_state == "LOADER-READY-RECONFIRMED"
    assert recovered.environment.retained_public_journal == actual_recover.journal
    assert recovered.environment.unresolved_public_action_id is None

    stale_prep_prefix = prepared.environment.retained_public_journal
    assert stale_prep_prefix != no_data_journal
    stale_anchor = recover_material_for(with_readback(stale_prep_prefix))
    cropped_prefix = tuple(
        replace(event, sequence_number=index)
        for index, event in enumerate(no_data_journal[1:], start=1)
    )
    replaced_prefix = tuple(
        replace(event, event_id="EV_TH_LUS0001-REPLACED") if index == 1 else event
        for index, event in enumerate(no_data_journal)
    )
    reordered_prefix = tuple(
        replace(
            event,
            event_id=(
                no_data_journal[2].event_id if index == 1
                else no_data_journal[1].event_id if index == 2
                else event.event_id
            ),
        )
        for index, event in enumerate(no_data_journal)
    )
    invalid_recover_materials = (
        stale_anchor,
        recover_material_for((
            _PublicJournalEvent(
                session_id,
                correlation_id,
                1,
                "RECOVER-READY-READBACK",
            ),
        )),
        recover_material_for(with_readback(cropped_prefix)),
        recover_material_for(with_readback(replaced_prefix)),
        recover_material_for(with_readback(reordered_prefix)),
    )
    for invalid_recover in invalid_recover_materials:
        failed = session.step(
            unknown.state,
            replace(
                unknown.environment,
                public_materials=_replace_material(
                    unknown.environment.public_materials,
                    invalid_recover,
                ),
            ),
        )
        failed_evidence = failed.state.evidence[-1]
        assert failed_evidence.snapshot.action_id == RECOVER_ACTION_ID
        assert failed_evidence.committed is False
        assert failed_evidence.resolution_code == "RECOVER-TARGET-UNCONFIRMED"
        assert failed.state.context.q_status == "UNKNOWN"
        assert failed.state.context.current_summary is None
        assert failed.state.history.hypotheses == unknown.state.history.hypotheses
        assert type(failed.environment) is _LoaderScenarioEnvironment
        assert failed.environment.retained_public_journal == no_data_journal
        assert failed.environment.unresolved_public_action_id is None
        assert failed.environment.loader_state != "LOADER-READY-RECONFIRMED"

    # An absent or malformed current TEST prefix must fail closed instead of
    # letting the retained two-event Prep anchor authorize a later Recover.
    for case_id, incomplete_materials in (
        (
            "missing-order-material",
            tuple(item for item in materials if item.action_id != ORDER_TEST_ACTION_ID),
        ),
        (
            "incomplete-order-receipt",
            _replace_material(
                materials,
                action_material(
                    base_order,
                    ORDER_TEST_ACTION_ID,
                    no_data_journal,
                    completed=False,
                ),
            ),
        ),
        (
            "wrong-order-correlation",
            _replace_material(
                materials,
                action_material(base_order, ORDER_TEST_ACTION_ID, no_data_journal),
            ),
        ),
    ):
        invalid_session_id = f"scenario-retained-prefix-{case_id}"
        invalid_materials = tuple(
            replace(
                item,
                journal=tuple(
                    replace(event, session_id=invalid_session_id)
                    for event in item.journal
                ),
                receipt=(
                    None
                    if item.receipt is None
                    else replace(item.receipt, session_id=invalid_session_id)
                ),
            )
            for item in incomplete_materials
        )
        if case_id == "wrong-order-correlation":
            wrong_order = next(
                item
                for item in invalid_materials
                if item.action_id == ORDER_TEST_ACTION_ID
            )
            assert wrong_order.receipt is not None
            invalid_materials = _replace_material(
                invalid_materials,
                replace(
                    wrong_order,
                    receipt=replace(wrong_order.receipt, correlation_id="foreign-correlation"),
                ),
            )
        invalid_session, invalid_prepared, invalid_unknown = run_to_order(
            case_id,
            invalid_materials,
            correlation_id,
        )
        # The material fixture is rebuilt for a distinct session ID above;
        # its current operation correlation remains the same controlled one.
        invalid_evidence = invalid_unknown.state.evidence[-1]
        assert invalid_evidence.snapshot.action_id == ORDER_TEST_ACTION_ID
        assert invalid_evidence.resolution_code == "UNKNOWN-EFFECT"
        assert invalid_unknown.state.context.q_status == "UNKNOWN"
        assert invalid_unknown.state.context.current_summary is None
        assert invalid_unknown.state.history.hypotheses == frozenset({"NORMAL", "EARLY-DATA"})
        assert type(invalid_unknown.environment) is _LoaderScenarioEnvironment
        assert invalid_unknown.environment._state == "LOADER-AFTER-TEST"
        assert invalid_unknown.environment.loader_state == "LOADER-CONTROL-STEP-ISSUED"
        assert invalid_unknown.environment.unresolved_public_action_id == ORDER_TEST_ACTION_ID
        old_prefix = invalid_prepared.environment.retained_public_journal
        assert invalid_unknown.environment.retained_public_journal == old_prefix
        invalid_base_recover = next(
            item for item in invalid_materials if item.action_id == RECOVER_ACTION_ID
        )
        assert invalid_base_recover.receipt is not None
        old_anchor_recover = _ActionPublicMaterial(
            RECOVER_ACTION_ID,
            old_prefix + (
                _PublicJournalEvent(
                    invalid_session_id,
                    correlation_id,
                    len(old_prefix) + 1,
                    "RECOVER-READY-READBACK",
                ),
            ),
            replace(
                invalid_base_recover.receipt,
                prefix_start=1,
                prefix_end=len(old_prefix) + 1,
            ),
        )
        failed_old_anchor = invalid_session.step(
            invalid_unknown.state,
            replace(
                invalid_unknown.environment,
                public_materials=_replace_material(
                    invalid_unknown.environment.public_materials,
                    old_anchor_recover,
                ),
            ),
        )
        failed_evidence = failed_old_anchor.state.evidence[-1]
        assert failed_evidence.snapshot.action_id == RECOVER_ACTION_ID
        assert failed_evidence.committed is False
        assert failed_evidence.resolution_code == "RECOVER-TARGET-UNCONFIRMED"
        assert failed_old_anchor.state.context.q_status == "UNKNOWN"
        assert failed_old_anchor.state.context.current_summary is None
        assert failed_old_anchor.state.history.hypotheses == invalid_unknown.state.history.hypotheses
        assert type(failed_old_anchor.environment) is _LoaderScenarioEnvironment
        assert failed_old_anchor.environment.retained_public_journal == old_prefix
        assert failed_old_anchor.environment.unresolved_public_action_id == ORDER_TEST_ACTION_ID
        assert failed_old_anchor.environment.loader_state != "LOADER-READY-RECONFIRMED"


def test_a13_actual_package_bound_runtime_binding_keeps_p3_unavailable() -> None:
    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=False)
    witness_rows = package.get("feasibilityWitnesses")
    assert isinstance(witness_rows, list)
    witness = next(row for row in witness_rows if isinstance(row, dict) and row.get("id") == "WIT-P3-UNAVAILABLE")
    assert INSPECT_ACTION_ID in model.actions
    assert "P3-UNAVAILABLE" in str(witness["claim"])
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="scenario-p3-unavailable",
        run_id="scenario-p3-unavailable",
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(0),
        retry_cap=1,
    )

    class _NoDispatch:
        calls = 0

        def execute(self, _request: object) -> object:  # pragma: no cover - dispatch is the failure
            self.calls += 1
            raise AssertionError("P3-unavailable checkpoint must not dispatch")

    no_dispatch = _NoDispatch()
    result = session.step(session.initial_state, no_dispatch)  # type: ignore[arg-type]
    assert no_dispatch.calls == 0
    assert result.stop_reason == "Stop-Budget"
    assert result.stop_trace is not None
    assert result.stop_trace.applicability_status == "P3-UNAVAILABLE"
    assert result.stop_trace.applicability_context_id is None
    assert result.stop_trace.active_named_645_residuals == ()


def test_a14_prep_effect_branches_preserve_the_declared_history_and_successor_split() -> None:
    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=True)
    expected = _require_mapping(_action(package, PREP_ACTION_ID)["prepEffectBranches"])

    for branch in (
        "confirmed",
        "confirmedNotSent",
        "executedSummaryUnconfirmed",
        "targetNotReachedWithConfirmedSuccessor",
    ):
        session_id = f"scenario-prep-{branch}"
        environment = _scenario_environment(
            package, model, session_id=session_id, prep_branch=branch,
        )
        session = ReferenceSession(
            binding=binding,
            model=model,
            session_id=session_id,
            run_id=session_id,
            initial_summary="SCENE-ENTRY",
            resources=ResourceState.rounds(4),
            retry_cap=4,
        )
        after_inspect = session.step(session.initial_state, environment)
        before_prep = after_inspect.state
        after_prep = session.step(before_prep, after_inspect.environment)
        evidence = after_prep.state.evidence[-1]
        assert evidence.execution.action_id == PREP_ACTION_ID
        assert evidence.execution.effect_class == expected[branch]["effectClass"]
        assert type(after_prep.environment) is _LoaderScenarioEnvironment
        # All four package branches are post-admission results: the existing
        # session must record exactly one attempt and one charge even when the
        # object did not send or the public successor summary is unavailable.
        assert evidence.issued_to_executor is True
        assert evidence.charged_once is True
        assert evidence.resource_before.mode == "ROUNDS"
        assert evidence.resource_before.remaining == before_prep.resources.remaining
        assert evidence.resource_after.remaining == before_prep.resources.remaining - 1
        assert after_prep.state.resources.remaining == before_prep.resources.remaining - 1
        assert after_prep.state.attempts == before_prep.attempts + 1
        assert len(after_prep.state.evidence) == len(before_prep.evidence) + 1

        if branch == "confirmedNotSent":
            assert evidence.resolution_code == "CONFIRMED-NOT-SENT"
            assert after_prep.state.context.q_status == "KNOWN"
            assert after_prep.state.context.current_summary == before_prep.context.current_summary
            assert after_prep.state.history == before_prep.history
            assert after_prep.environment._state == "LOADER-AFTER-INSPECTION"
            assert after_prep.environment.loader_state == after_inspect.environment.loader_state
            # CNS is explicitly not dispatched: it must not manufacture a
            # post-action public prefix or an unresolved execution boundary.
            assert (
                after_prep.environment.retained_public_journal
                == after_inspect.environment.retained_public_journal
            )
            assert (
                after_prep.environment.unresolved_public_action_id
                == after_inspect.environment.unresolved_public_action_id
            )
        elif branch == "executedSummaryUnconfirmed":
            assert evidence.resolution_code == "UNKNOWN-EFFECT"
            assert after_prep.state.context.q_status == "UNKNOWN"
            assert after_prep.state.context.current_summary is None
            assert after_prep.environment._state == "LOADER-AFTER-PREP"
            assert after_prep.environment.loader_state == "LOADER-READY-WINDOW-EXECUTED-UNCONFIRMED"
            assert after_prep.state.history.hypotheses == before_prep.history.hypotheses
            prep_material = next(
                item
                for item in after_prep.environment.public_materials
                if item.action_id == PREP_ACTION_ID
            )
            assert after_prep.environment.retained_public_journal == prep_material.journal
            assert after_prep.environment.unresolved_public_action_id is None
        else:
            assert evidence.resolution_code == "COMMIT"
            assert after_prep.state.context.q_status == "KNOWN"
            assert after_prep.state.context.current_summary == "Q-TARGET-READY"
            assert after_prep.environment._state == "LOADER-AFTER-PREP"
            result = evidence.execution.prep_recover
            assert isinstance(result, PrepRecoverResult)
            assert result.target_confirmed is (branch == "confirmed")
            assert result.summary_confirmed is True


def test_a15_explicit_continuation_preserves_post_dispatch_state_then_recovers_without_rewind() -> None:
    package = _scenario_package()
    binding, model = _scenario_runtime_parts(package, include_recover=True)
    continuation_case = _case(package, "CASE-UNKNOWN-RECOVER-CONTINUATION")
    initial_context = _require_mapping(continuation_case["initialContext"])
    unknown_contract = _require_mapping(continuation_case["unknownRecoverContract"])
    continuation_rounds = continuation_case["rounds"]
    assert isinstance(continuation_rounds, list) and len(continuation_rounds) == 3
    prior_action_ids = initial_context["completedActionIds"]
    retained_prefix = initial_context["retainedPublicPrefix"]
    initial_members = initial_context["compatibleHypotheses"]
    assert isinstance(prior_action_ids, list) and len(prior_action_ids) == 1
    assert isinstance(retained_prefix, list) and len(retained_prefix) == 3
    assert isinstance(initial_members, list) and initial_members
    prior_action_id = prior_action_ids[0]
    assert isinstance(prior_action_id, str)
    prior_action = _action(package, prior_action_id)
    trigger_action_id = unknown_contract["triggerActionId"]
    trigger_round = unknown_contract["triggerRound"]
    assert isinstance(trigger_action_id, str)
    assert isinstance(trigger_round, int) and not isinstance(trigger_round, bool)
    assert continuation_rounds[0]["actionId"] == PREP_ACTION_ID
    assert continuation_rounds[1]["actionId"] == trigger_action_id
    assert continuation_rounds[2]["actionId"] == RECOVER_ACTION_ID
    assert initial_context["entryKind"] == "INHERITED-CONTINUATION"
    assert initial_context["sessionBinding"] == "CURRENT-SESSION-ONLY"
    assert initial_context["correlationBinding"] == "CURRENT-OPERATION-CORRELATION"

    clean = _scenario_environment(package, model, session_id="direct")
    issued = clean.execute(ExecutionRequest("direct", "direct-1", INSPECT_ACTION_ID, "TEST"))
    assert type(issued.successor) is _LoaderScenarioEnvironment
    assert issued.successor.loader_state == "LOADER-INSPECTION-COMPLETE"
    assert issued.successor.target_hardware_state == "TH-STATE-PRESERVED-DURING-INSPECTION"
    assert clean.loader_state == "LOADER-LIST-OFFERED"
    pending = issued.successor.with_pending_delivery(issued.record)
    delivery = pending.take_pending_delivery()
    assert delivery is not None
    consumed, after_receive = delivery
    assert consumed is issued.record
    assert type(after_receive) is _LoaderScenarioEnvironment
    assert after_receive.visible_evidence_refs == issued.successor.visible_evidence_refs
    assert pending.visible_evidence_refs == issued.successor.visible_evidence_refs

    session_id = "scenario-unknown-recover"
    environment = _scenario_environment(
        package,
        model,
        session_id=session_id,
        force_post_dispatch_summary_error=True,
    )
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id=session_id,
        run_id=session_id,
        initial_summary="SCENE-ENTRY",
        resources=ResourceState.rounds(4),
        retry_cap=4,
    )
    inspected = session.step(session.initial_state, environment)
    # Reconstruct the declared inherited entry using its named prior action,
    # then compare the real session state to the package rather than a second
    # hard-coded copy of H/q/prefix values in this test.
    prior_evidence = inspected.state.evidence[-1]
    prior_outcome = _outcome(prior_action, prior_evidence.execution.observable or "")
    expected_retained_prefix = [
        _require_mapping(package["scope"])["startBoundary"],
        _require_mapping(prior_action["inspection"])["completionReceipt"],
        prior_outcome["observable"],
    ]
    assert retained_prefix == expected_retained_prefix
    assert inspected.state.context.q_status == initial_context["qStatus"]
    assert inspected.state.context.current_summary == initial_context["currentSummary"]
    assert inspected.state.history.hypotheses == frozenset(initial_members)
    assert tuple(item.snapshot.action_id for item in inspected.state.evidence) == tuple(prior_action_ids)

    prepared = session.step(inspected.state, inspected.environment)
    assert prepared.state.context.q_status == "KNOWN"
    assert prepared.state.context.current_summary == "Q-TARGET-READY"
    assert prepared.environment._state == "LOADER-AFTER-PREP"
    assert prepared.environment.current_session_ready_receipt == "TH-LUS0001-READY-RECEIPT"

    unknown = session.step(prepared.state, prepared.environment)
    assert unknown.stop_reason is None
    assert unknown_contract["trigger"] == "POST-DISPATCH-TEST-SUMMARY-CONFIRMATION-FAILURE"
    assert unknown.state.context.q_status == unknown_contract["recoverEntryQStatus"]
    assert unknown.state.context.current_summary is None
    assert unknown.state.evidence[-1].snapshot.action_id == trigger_action_id
    assert unknown.state.evidence[-1].resolution_code == "SUMMARY-CONFIRMATION-ERROR"
    assert len(unknown.state.evidence) == len(prior_action_ids) + trigger_round
    assert type(unknown.environment) is _LoaderScenarioEnvironment
    assert unknown.environment._state == "LOADER-AFTER-TEST"
    assert unknown.environment.loader_state == "LOADER-CONTROL-STEP-ISSUED"
    assert unknown.environment.target_hardware_state == "TH-CONTROL-STEP-MAY-HAVE-ADVANCED"
    assert unknown.environment.visible_evidence_refs != prepared.environment.visible_evidence_refs
    trigger_material = next(
        item for item in unknown.environment.public_materials if item.action_id == trigger_action_id
    )
    assert set(unknown_contract["mayHaveVisibleEvents"]) <= {
        event.event_id for event in trigger_material.journal
    }
    assert unknown.environment.retained_public_journal == trigger_material.journal
    assert unknown_contract["sessionDisposition"] == (
        "UNKNOWN-PRESERVE-ACTUAL-SUCCESSOR-AND-POST-DISPATCH-JOURNAL"
    )
    # UNKNOWN has no summary; it must not revive the inherited continuation
    # summary, and its actual successor/public evidence are retained.
    assert unknown.state.context.current_summary != initial_context["currentSummary"]

    recover_material = next(
        item for item in unknown.environment.public_materials if item.action_id == RECOVER_ACTION_ID
    )
    assert recover_material.receipt is not None
    recover_action = _action(package, RECOVER_ACTION_ID)
    recover_receipt_id = _require_mapping(recover_action["inspection"])["completionReceipt"]
    assert isinstance(recover_receipt_id, str)
    assert set(unknown_contract["recoverRequiredPublicEvidence"]) == {
        "CURRENT-SESSION-READY-READBACK",
        recover_receipt_id,
        "EXACT-RETAINED-POST-DISPATCH-PUBLIC-PREFIX",
        "RECOVER-READY-READBACK-ONLY-EXTENSION",
    }
    assert unknown_contract["targetAndSummaryConfirmation"] == (
        "SEPARATE-REQUIRED-NO-REWIND-OR-REPLAY"
    )
    assert recover_material.receipt.session_id == session_id
    assert recover_material.receipt.correlation_id == unknown.environment.correlation_id
    retained_journal = unknown.environment.retained_public_journal
    assert recover_material.journal[:len(retained_journal)] == retained_journal
    assert recover_material.journal[len(retained_journal):] == (
        _PublicJournalEvent(
            session_id,
            unknown.environment.correlation_id,
            retained_journal[-1].sequence_number + 1,
            "RECOVER-READY-READBACK",
        ),
    )

    def recover_material_for(journal: tuple[_PublicJournalEvent, ...]) -> _ActionPublicMaterial:
        return _ActionPublicMaterial(
            RECOVER_ACTION_ID,
            journal,
            replace(recover_material.receipt, prefix_start=1, prefix_end=len(journal)),
        )

    # Every variant below has a syntactically complete current-session receipt.
    # They fail because Recover must extend the actual retained post-dispatch
    # prefix, not because the test merely omitted a receipt.
    missing_readback = recover_material_for(retained_journal)
    readback_only = recover_material_for((
        _PublicJournalEvent(
            session_id,
            unknown.environment.correlation_id,
            1,
            "RECOVER-READY-READBACK",
        ),
    ))
    cropped_prefix = recover_material_for(tuple(
        replace(event, sequence_number=index)
        for index, event in enumerate(recover_material.journal[1:], start=1)
    ))
    replaced_prefix = recover_material_for(tuple(
        replace(event, event_id="EV_DL_OFFER_LIST-REPLACED") if index == 1 else event
        for index, event in enumerate(recover_material.journal)
    ))
    reordered_prefix = recover_material_for(tuple(
        replace(event, event_id=(
            recover_material.journal[2].event_id if index == 1
            else recover_material.journal[1].event_id if index == 2
            else event.event_id
        ))
        for index, event in enumerate(recover_material.journal)
    ))

    for invalid_material in (
        missing_readback,
        readback_only,
        cropped_prefix,
        replaced_prefix,
        reordered_prefix,
    ):
        failed_environment = replace(
            unknown.environment,
            public_materials=_replace_material(
                unknown.environment.public_materials, invalid_material,
            ),
        )
        failed_recover = session.step(unknown.state, failed_environment)
        failed_evidence = failed_recover.state.evidence[-1]
        assert failed_evidence.snapshot.action_id == RECOVER_ACTION_ID
        assert failed_evidence.committed is False
        assert failed_evidence.resolution_code == "RECOVER-TARGET-UNCONFIRMED"
        assert failed_recover.state.context.q_status == unknown_contract["recoverEntryQStatus"]
        assert failed_recover.state.context.current_summary is None
        assert failed_recover.state.history.hypotheses == unknown.state.history.hypotheses
        assert failed_recover.state.context.current_summary != initial_context["currentSummary"]
        assert type(failed_recover.environment) is _LoaderScenarioEnvironment
        assert failed_recover.environment.retained_public_journal == retained_journal
        assert failed_recover.environment.unresolved_public_action_id is None
        assert failed_recover.environment.loader_state != "LOADER-READY-RECONFIRMED"

    recovered = session.step(unknown.state, unknown.environment)
    recover_outcome = _outcome(recover_action, "RECOVER-READY-READBACK")
    assert recovered.state.evidence[-1].snapshot.action_id == RECOVER_ACTION_ID
    assert recovered.state.evidence[-1].resolution_code == "COMMIT"
    assert recovered.state.context.q_status == "KNOWN"
    assert recovered.state.context.current_summary == recover_outcome["postSummary"]
    assert type(recovered.environment) is _LoaderScenarioEnvironment
    assert recovered.environment._state == "LOADER-RECOVERED"
    assert recovered.environment.loader_state == "LOADER-READY-RECONFIRMED"
    assert recovered.environment.target_hardware_state == "TH-READY-READBACK-RETAINED"
    assert recovered.environment.current_session_ready_receipt == recover_receipt_id
    result = recovered.state.evidence[-1].execution.prep_recover
    assert isinstance(result, PrepRecoverResult)
    assert result.target_confirmed is True and result.summary_confirmed is True
    assert unknown_contract["rewindProhibited"] == f"NO-REWIND-TO-{initial_context['currentSummary']}"
    assert recovered.state.context.current_summary != initial_context["currentSummary"]
