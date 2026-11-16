"""Git-bound authority and finite-model construction for the C adapter.

The adapter consumes the accepted H-B scenario artifact directly from a Git
object.  It intentionally does not parse the mutable worktree copy of the
scenario package, and it never binds itself to the current implementation
HEAD.  The finite model below is a narrow projection of that artifact's four
declared actions and three declared engineering hypotheses.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha1, sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from cltav_runtime.bindings import RuntimeAuthorityBinding, SourceSnapshot
from cltav_runtime.interpretation import InterpretationContract
from cltav_runtime.kernel import ContractSnapshot, Interval, ModelContext
from cltav_runtime.model import FiniteSessionModel

from .identity import register_loaded_module


H_B_COMMIT = "d0c674f9fdb165b6ff8c2a40565d4deb7226d2a0"
SCENARIO_PATH = "configs/engineering/cltav_615a_scenarios.json"
H_B_SCENARIO_GIT_BLOB_OID = "c620beb8c84d296df191b8d9af3648c9b3664017"
H_B_SCENARIO_RAW_SHA256 = "9c86da50596cbae4f53b23de9ddff8ceed0bad65efe251033c2e1b13e1505d16"
DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
INTERFACE_PATH = "configs/research/cltav_interface_registry.json"

INSPECT_ACTION_ID = "ACT-INSPECT-NO-WRQ-BEFORE-READY"
PREP_ACTION_ID = "ACT-PREP-ENTER-READY-WINDOW"
ORDER_ACTION_ID = "ACT-TEST-ACK-BEFORE-DATA"
RECOVER_ACTION_ID = "ACT-RECOVER-RECONFIRM-READY"
ACTION_IDS = (INSPECT_ACTION_ID, PREP_ACTION_ID, ORDER_ACTION_ID, RECOVER_ACTION_ID)

# This is a C-layer *engineering witness* ownership contract over actual B
# public WRQ/ACK events.  It does not manufacture a reviewed protocol
# deadline.  The fixed strings are deliberately kept here rather than supplied
# by a fixture so that no environment can select its own ownership semantics.
C_OWNERSHIP_CONTRACT_ID = "IC-615A-C-WRQ-ACK-OWNERSHIP-V1"
C_OWNERSHIP_KEY = "LUR-START-CURRENT-CORRELATION"
C_OWNERSHIP_TRIGGER_TYPE = "EV_DL_WRQ_LUR"
C_OWNERSHIP_RESPONSE_TYPE = "EV_TH_ACK_LUR"
C_OWNERSHIP_CANCEL_TYPE = "C-OWNERSHIP-CANCEL"
C_OWNERSHIP_SUPERSEDE_TYPE = "C-OWNERSHIP-SUPERSEDE"
C_ENGINEERING_HORIZON_TICKS = Fraction(3)
# C has a finite eight-action model.  This merely bounds the public ownership
# carrier's virtual-tick domain; it is not a protocol deadline.  The actual
# order witness uses the B WRQ/ACK event ticks and stable sequence numbers.
C_OWNERSHIP_TIMELINE_MAX_TICKS = Fraction(24)


class ScenarioContractError(ValueError):
    """Raised when the fixed H-B scenario authority cannot be consumed."""


@dataclass(frozen=True)
class ScenarioInputIdentity:
    """Identity of the exact scenario bytes consumed by C at runtime."""

    commit: str
    path: str
    git_blob_oid: str
    raw_sha256: str

    def as_mapping(self) -> Mapping[str, str]:
        return MappingProxyType({
            "commit": self.commit,
            "path": self.path,
            "gitBlobOid": self.git_blob_oid,
            "rawSha256": self.raw_sha256,
        })


@dataclass(frozen=True)
class ScenarioSessionContract:
    """Verified H-B scenario source plus the derived finite runtime model."""

    scenario_input: ScenarioInputIdentity
    scenario_snapshot: SourceSnapshot
    authority_binding: RuntimeAuthorityBinding
    model: FiniteSessionModel
    package: Mapping[str, Any]
    action_by_id: Mapping[str, Mapping[str, Any]]

    @property
    def uncertainty_identity(self) -> str:
        return self.model.uncertainty_identity

    @property
    def virtual_clock_id(self) -> str:
        return self.model.context.projection_clock

    def action(self, action_id: str) -> Mapping[str, Any]:
        action = self.action_by_id.get(action_id)
        if action is None:
            raise ScenarioContractError("C-ADAPTER-ACTION-NOT-DECLARED")
        return action


def c_interpretation_contract(contract: ScenarioSessionContract) -> InterpretationContract:
    """Return the immutable C public request/receipt ownership contract.

    C binds the actual current-correlation B ``EV_DL_WRQ_LUR`` public event
    to its matching ``EV_TH_ACK_LUR`` public event.  A completed prefix
    receipt is retained as supporting public evidence, but is never recast as
    a sixth protocol event.  ``METHOD-ONLY`` preserves the required boundary:
    this proves only an engineering witness, never a protocol timeout or a
    no-response FAIL.
    """

    uncertainty = contract.model.uncertainty
    return InterpretationContract(
        contract_id=C_OWNERSHIP_CONTRACT_ID,
        trigger_event_type=C_OWNERSHIP_TRIGGER_TYPE,
        response_event_type=C_OWNERSHIP_RESPONSE_TYPE,
        key=C_OWNERSHIP_KEY,
        policy="UNIQUE-KEY",
        concurrent_same_key=False,
        cancellation_event_type=C_OWNERSHIP_CANCEL_TYPE,
        supersession_event_type=C_OWNERSHIP_SUPERSEDE_TYPE,
        physical_domain=Interval(Fraction(0), C_OWNERSHIP_TIMELINE_MAX_TICKS, True, True),
        requirement_window=Interval(Fraction(0), C_ENGINEERING_HORIZON_TICKS, True, True),
        clock_identity=uncertainty.clock_id,
        uncertainty_identity=uncertainty.uncertainty_id,
        error_budget_identity=uncertainty.identity,
        unit=uncertainty.time_unit,
        clock_valid=True,
        error_budget_valid=True,
        deadline_authority="METHOD-ONLY",
        deadline_identity="C-THREE-TICK-ENGINEERING-HORIZON-V1",
        upper_bound=C_ENGINEERING_HORIZON_TICKS,
        upper_closed=True,
    )


def _git_blob_oid(content: bytes) -> str:
    """Compute the ordinary SHA-1 Git blob identity from the verified bytes."""

    return sha1(f"blob {len(content)}\0".encode("ascii") + content).hexdigest()


def _mapping(value: object, *, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ScenarioContractError(f"C-ADAPTER-{label}-MALFORMED")
    return value


def _rows(value: object, *, label: str) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(value, list) or not value:
        raise ScenarioContractError(f"C-ADAPTER-{label}-MALFORMED")
    return tuple(_mapping(item, label=label) for item in value)


def _exact_string(value: object, *, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise ScenarioContractError(f"C-ADAPTER-{label}-MALFORMED")
    return value


def _action_cost(action: Mapping[str, Any]) -> tuple[int, Mapping[str, int]]:
    declared = _mapping(action.get("cost"), label="ACTION-COST")
    values = {
        "acquisition": declared.get("acquisition"),
        "computation": declared.get("computation"),
        "preparation": declared.get("preparation"),
        "recovery": 0,
        "retry": declared.get("retry"),
    }
    if any(type(value) is not int or value < 0 for value in values.values()):
        raise ScenarioContractError("C-ADAPTER-ACTION-COST-MALFORMED")
    return max(1, sum(values.values())), MappingProxyType(dict(values))


def _action_model_mapping(
    action: Mapping[str, Any], *, state_id: str, members: tuple[Mapping[str, Any], ...],
) -> Mapping[str, Any]:
    """Project one package action into the closed finite runtime grammar."""

    action_id = _exact_string(action.get("id"), label="ACTION-ID")
    kind = _exact_string(action.get("kind"), label="ACTION-KIND")
    if action_id not in ACTION_IDS or kind not in {"TEST", "PREP", "RECOVER"}:
        raise ScenarioContractError("C-ADAPTER-ACTION-KIND-MALFORMED")
    inspection = _mapping(action.get("inspection"), label="ACTION-INSPECTION")
    horizon = inspection.get("finiteHorizonTicks")
    if type(horizon) is not int or horizon < 0:
        raise ScenarioContractError("C-ADAPTER-ACTION-HORIZON-MALFORMED")
    outcomes = _rows(action.get("possibleOutcomes"), label="ACTION-OUTCOMES")
    cost, charges = _action_cost(action)
    emissions: dict[str, str] = {}
    for member in members:
        member_id = _exact_string(member.get("id"), label="HYPOTHESIS-ID")
        matches = [
            candidate for candidate in outcomes
            if member_id in candidate.get("compatibleHypotheses", [])
        ]
        # PREP/RECOVER operate through the runtime's summary-only path.  They
        # still need a total finite model declaration for every initial H
        # member, even for a member excluded by an earlier Test.  The adapter
        # never manufactures that excluded continuation at runtime.
        if not matches and kind in {"PREP", "RECOVER"} and len(outcomes) == 1:
            matches = list(outcomes)
        # The order Test is admitted only after the no-WRQ Test has removed
        # EARLY-WRQ.  Its total finite declaration is not permission to drive
        # an EARLY-WRQ continuation.
        if not matches and action_id == ORDER_ACTION_ID:
            matches = [outcomes[0]]
        if len(matches) != 1:
            raise ScenarioContractError("C-ADAPTER-ACTION-OUTCOME-NOT-TOTAL")
        emissions[member_id] = _exact_string(matches[0].get("observable"), label="ACTION-OBSERVABLE")
    enabled = {
        INSPECT_ACTION_ID: ("SCENE-ENTRY",),
        PREP_ACTION_ID: ("Q-PRE-READY-NO-WRQ",),
        ORDER_ACTION_ID: ("Q-TARGET-READY",),
        RECOVER_ACTION_ID: ("RECOVER-ONLY-WHEN-UNKNOWN",),
    }[action_id]
    result: dict[str, Any] = {
        "id": action_id,
        "kind": kind,
        "cost": cost,
        "detailCharges": dict(charges),
        "enabledSummaries": list(enabled),
        "transition": {
            "id": f"TR-C-{action_id}",
            "source": state_id,
            "target": state_id,
            "guardAst": {"tag": "TRUE"},
            "simultaneousUpdates": [{"tag": "STATE-ASSIGN", "state": state_id}],
        },
        "observableByHypothesis": emissions,
        "measurementTicksByHypothesis": {member_id: horizon for member_id in emissions},
    }
    if kind in {"PREP", "RECOVER"}:
        result["declaredTarget"] = _exact_string(
            inspection.get("completionReceipt"), label="ACTION-COMPLETION-RECEIPT",
        )
        result["recoverWhenUnknown"] = kind == "RECOVER"
    return MappingProxyType(result)


def _package_model(
    package: Mapping[str, Any], *, development: ContractSnapshot,
) -> FiniteSessionModel:
    identity = _mapping(package.get("identity"), label="IDENTITY")
    family = _exact_string(identity.get("scenarioFamilyId"), label="FAMILY-ID")
    time = _mapping(package.get("timeAndObservation"), label="TIME")
    clock_id = _exact_string(time.get("virtualClockId"), label="CLOCK-ID")
    uncertainty_id = _exact_string(time.get("uncertaintyIdentity"), label="UNCERTAINTY-ID")
    domain = _mapping(package.get("hypothesisDomain"), label="HYPOTHESIS-DOMAIN")
    members = _rows(domain.get("members"), label="HYPOTHESES")
    action_rows = _rows(package.get("actionLibrary"), label="ACTIONS")
    action_by_id = {
        _exact_string(action.get("id"), label="ACTION-ID"): action for action in action_rows
    }
    if set(action_by_id) != set(ACTION_IDS):
        raise ScenarioContractError("C-ADAPTER-ACTION-DOMAIN-MISMATCH")
    kinds = {_exact_string(member.get("kind"), label="HYPOTHESIS-KIND") for member in members}
    state_id = f"S-{family}-C-ENTRY"
    declaration = {
        "stateIds": [state_id],
        "clockIds": [clock_id],
        "typedDomains": {"scenarioKind": sorted(kinds)},
    }
    context = ModelContext.build(
        snapshot=development,
        model={
            "stateIds": {state_id},
            "clockIds": {clock_id},
            "typedDomains": {"scenarioKind": set(kinds)},
        },
        projection_clock=clock_id,
    )
    hypotheses = []
    for member in members:
        member_id = _exact_string(member.get("id"), label="HYPOTHESIS-ID")
        member_kind = _exact_string(member.get("kind"), label="HYPOTHESIS-KIND")
        hypotheses.append({
            "id": member_id,
            "controlStateId": state_id,
            "clockConstraint": {
                clock_id: {
                    "lower": {"numerator": 0, "positiveDenominator": 1},
                    "upper": {"numerator": 0, "positiveDenominator": 1},
                    "lowerClosed": True,
                    "upperClosed": True,
                },
            },
            "typedStore": {"scenarioKind": member_kind},
        })
    actions = [
        dict(_action_model_mapping(action_by_id[action_id], state_id=state_id, members=members))
        for action_id in ACTION_IDS
    ]
    model = {
        "model": declaration,
        "hypotheses": hypotheses,
        "actions": actions,
        "limits": {
            "pathLength": 8,
            "frontierStates": len(members),
            "hypotheses": len(members),
            "actions": len(actions),
            "observationClasses": len({
                observable
                for action in actions
                for observable in action["observableByHypothesis"].values()
            }),
        },
        "uncertainty": {
            "id": uncertainty_id,
            "clockId": clock_id,
            "timeUnit": "ticks",
            "maximumErrorTicks": 0,
        },
    }
    return FiniteSessionModel.from_mapping(context=context, value=model)


def load_hb_session_contract(repository: Path | str) -> ScenarioSessionContract:
    """Load the fixed H-B package and derive all runtime inputs from its bytes.

    There is deliberately no ``commit`` argument.  Accepting a caller's
    current HEAD would make a C implementation certify the source it is
    currently editing.  A later C revision may add a separately reviewed
    authority pin, but it may not silently retarget this baseline.
    """

    repository_path = Path(repository).resolve()
    snapshot = SourceSnapshot.from_git_object(
        repository=repository_path,
        commit=H_B_COMMIT,
        path=SCENARIO_PATH,
    )
    content = snapshot._content
    raw_sha256 = sha256(content).hexdigest()
    git_blob_oid = _git_blob_oid(content)
    if raw_sha256 != H_B_SCENARIO_RAW_SHA256 or git_blob_oid != H_B_SCENARIO_GIT_BLOB_OID:
        raise ScenarioContractError("C-ADAPTER-HB-SCENARIO-IDENTITY-MISMATCH")
    package = _mapping(snapshot.json_object(), label="SCENARIO-PACKAGE")
    identity = _mapping(package.get("identity"), label="IDENTITY")
    authority_commit = _exact_string(identity.get("acceptedAuthorityCommit"), label="AUTHORITY-COMMIT")
    if authority_commit != "c577f34e98b91083a69f0a731a990c01aa7fa08b":
        raise ScenarioContractError("C-ADAPTER-AUTHORITY-BASE-MISMATCH")
    input_rows = _rows(package.get("acceptedInputs"), label="ACCEPTED-INPUTS")
    inputs = {
        _exact_string(row.get("role"), label="INPUT-ROLE"): row for row in input_rows
    }
    development_row = inputs.get("DEVELOPMENT-CONTRACT")
    interface_row = inputs.get("INTERFACE-REGISTRY")
    if development_row is None or interface_row is None:
        raise ScenarioContractError("C-ADAPTER-RUNTIME-AUTHORITY-INPUT-MISSING")
    development_path = _exact_string(development_row.get("path"), label="DEVELOPMENT-PATH")
    interface_path = _exact_string(interface_row.get("path"), label="INTERFACE-PATH")
    binding = RuntimeAuthorityBinding.from_git_objects(
        repository=repository_path,
        development_commit=authority_commit,
        development_path=development_path,
        interface_commit=authority_commit,
        interface_path=interface_path,
    )
    development = ContractSnapshot.from_git_object(
        repository=repository_path,
        contract_commit=authority_commit,
        contract_path=development_path,
    )
    model = _package_model(package, development=development)
    action_by_id = {
        _exact_string(row.get("id"), label="ACTION-ID"): MappingProxyType(dict(row))
        for row in _rows(package.get("actionLibrary"), label="ACTIONS")
    }
    return ScenarioSessionContract(
        ScenarioInputIdentity(H_B_COMMIT, SCENARIO_PATH, git_blob_oid, raw_sha256),
        snapshot,
        binding,
        model,
        MappingProxyType(dict(package)),
        MappingProxyType(action_by_id),
    )


def action_horizon(contract: ScenarioSessionContract, action_id: str) -> Fraction:
    """Return the declared engineering observation horizon as an exact tick."""

    inspection = _mapping(contract.action(action_id).get("inspection"), label="ACTION-INSPECTION")
    horizon = inspection.get("finiteHorizonTicks")
    if type(horizon) is not int or horizon < 0:
        raise ScenarioContractError("C-ADAPTER-ACTION-HORIZON-MALFORMED")
    return Fraction(horizon)


def action_outcome(
    contract: ScenarioSessionContract, action_id: str, observable: str,
) -> Mapping[str, Any]:
    """Resolve a declared observable without inventing a code-side default."""

    outcomes = _rows(contract.action(action_id).get("possibleOutcomes"), label="ACTION-OUTCOMES")
    matches = [item for item in outcomes if item.get("observable") == observable]
    if len(matches) != 1:
        raise ScenarioContractError("C-ADAPTER-OBSERVABLE-NOT-DECLARED")
    return matches[0]


def action_receipt_label(contract: ScenarioSessionContract, action_id: str) -> str:
    inspection = _mapping(contract.action(action_id).get("inspection"), label="ACTION-INSPECTION")
    return _exact_string(inspection.get("completionReceipt"), label="ACTION-COMPLETION-RECEIPT")


register_loaded_module(__name__, __file__)
