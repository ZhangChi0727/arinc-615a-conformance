from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import check_615a_scenarios as checker  # noqa: E402
import sync_615a_scenarios as reader  # noqa: E402


PACKAGE = json.loads((ROOT / checker.PACKAGE_PATH).read_text(encoding="utf-8"))
SCHEMA = json.loads((ROOT / checker.SCHEMA_PATH).read_text(encoding="utf-8"))


def errors_for(mutator) -> list[str]:
    candidate = copy.deepcopy(PACKAGE)
    mutator(candidate)
    return checker.validate_package(ROOT, candidate, SCHEMA)


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


@pytest.fixture()
def isolated_snapshot_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, dict]:
    """Build a base snapshot and its separately introduced G0 control record."""

    root = tmp_path / "scenario-snapshot"
    root.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Scenario test"], cwd=root, check=True)
    subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=root, check=True)
    for binding in PACKAGE["acceptedInputs"]:
        source = ROOT / binding["path"]
        target = root / binding["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "accepted authority"], cwd=root, check=True)
    base_commit = _git(root, "rev-parse", "HEAD")

    # The production checker derives the allowed authority base from the Git
    # commit that first adds CR-2026-022.  Make the fixture reproduce that
    # topology rather than weakening the immutable-control test.
    control_path = root / checker.CONTROL_CHANGE_PATH
    control_path.parent.mkdir(parents=True, exist_ok=True)
    original_control = (ROOT / checker.CONTROL_CHANGE_PATH).read_text(encoding="utf-8")
    original_base = PACKAGE["identity"]["acceptedAuthorityCommit"]
    assert original_control.count(original_base) == 2
    control_path.write_text(original_control.replace(original_base, base_commit), encoding="utf-8", newline="\n")
    subprocess.run(["git", "add", checker.CONTROL_CHANGE_PATH.as_posix()], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "G0 control"], cwd=root, check=True)
    control_commit = _git(root, "rev-parse", "HEAD")

    candidate = copy.deepcopy(PACKAGE)
    candidate["identity"]["acceptedAuthorityCommit"] = base_commit
    for binding in candidate["acceptedInputs"]:
        path = binding["path"]
        raw = subprocess.check_output(["git", "cat-file", "blob", f"{base_commit}:{path}"], cwd=root)
        binding.update(
            commit=base_commit,
            gitBlobOid=_git(root, "rev-parse", f"{base_commit}:{path}"),
            rawSha256=hashlib.sha256(raw).hexdigest(),
        )
    control_bytes = subprocess.check_output(
        ["git", "cat-file", "blob", f"{control_commit}:{checker.CONTROL_CHANGE_PATH.as_posix()}"], cwd=root
    )
    candidate["controlBinding"].update(
        controlCommit=control_commit,
        gitBlobOid=_git(root, "rev-parse", f"{control_commit}:{checker.CONTROL_CHANGE_PATH.as_posix()}"),
        rawSha256=hashlib.sha256(control_bytes).hexdigest(),
    )
    package_path = root / checker.PACKAGE_PATH
    schema_path = root / checker.SCHEMA_PATH
    package_path.parent.mkdir(parents=True, exist_ok=True)
    package_path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    schema_path.write_text(json.dumps(SCHEMA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    yield root, candidate


def test_a01_package_is_valid_and_reordering_is_semantic_noop() -> None:
    assert checker.validate_package(ROOT) == []
    candidate = copy.deepcopy(PACKAGE)
    for collection in ("acceptedInputs", "sourceRelations", "actionLibrary", "cases", "experimentRelations", "feasibilityWitnesses"):
        candidate[collection].reverse()
    assert checker.validate_package(ROOT, candidate, SCHEMA) == []
    assert reader.render(candidate) == reader.render(PACKAGE)


def test_a02_schema_and_controlled_chinese_fields_fail_closed() -> None:
    assert any("additional properties" in error.lower() for error in errors_for(lambda data: data.update(uncontrolled="value")))
    assert any("BILINGUAL" in error for error in errors_for(lambda data: data["translationsZh"].pop("actions.ACT-TEST-ACK-BEFORE-DATA.summary")))
    assert any("scope.summary" in error for error in errors_for(lambda data: data["translationsZh"].__setitem__("scope.summary", " \r\n ")))
    assert any("additional properties" in error.lower() for error in errors_for(lambda data: data["sourceRelations"][0].update(unexpected="field")))


def test_a03_bound_authorities_are_consumed_from_the_indexed_snapshot_not_worktree(
    isolated_snapshot_repo: tuple[Path, dict],
) -> None:
    root, candidate = isolated_snapshot_repo
    (root / "configs/requirements/arinc_615a3_m1_crs.json").write_text("{}", encoding="utf-8")
    (root / "configs/models/arinc_615a3_m2_model.json").write_text("{}", encoding="utf-8")
    (root / "configs/research/cltav_interface_registry.json").write_text("{}", encoding="utf-8")
    (root / "configs/research/cltav_experiment_design.json").write_text("{}", encoding="utf-8")
    assert checker.validate_package(root, candidate) == []


def test_a03b_complete_rebinding_to_a_real_later_commit_cannot_replace_the_g0_base() -> None:
    candidate = copy.deepcopy(PACKAGE)
    later_commit = _git(ROOT, "rev-parse", "HEAD")
    assert later_commit != candidate["identity"]["acceptedAuthorityCommit"]
    candidate["identity"]["acceptedAuthorityCommit"] = later_commit
    for binding in candidate["acceptedInputs"]:
        path = binding["path"]
        raw = subprocess.check_output(["git", "cat-file", "blob", f"{later_commit}:{path}"], cwd=ROOT)
        binding.update(
            commit=later_commit,
            gitBlobOid=_git(ROOT, "rev-parse", f"{later_commit}:{path}"),
            rawSha256=hashlib.sha256(raw).hexdigest(),
        )
    errors = checker.validate_package(ROOT, candidate, SCHEMA)
    assert any("acceptedAuthorityCommit differs from the immutable CR-2026-022 base" in error for error in errors)


def test_a04_unsafe_and_forged_input_bindings_are_rejected_before_their_path_is_read(monkeypatch: pytest.MonkeyPatch) -> None:
    candidate = copy.deepcopy(PACKAGE)
    unsafe_path = f"{chr(67)}:{chr(47)}outside/arinc_615a3_m1_crs.json"
    candidate["acceptedInputs"][0]["path"] = unsafe_path
    calls: list[tuple[str, ...]] = []
    original = checker._git_bytes

    def observe(root: Path, *args: str) -> bytes:
        calls.append(args)
        return original(root, *args)

    monkeypatch.setattr(checker, "_git_bytes", observe)
    errors = checker.validate_package(ROOT, candidate, SCHEMA)
    assert any("unsafe binding path" in error for error in errors)
    assert all(unsafe_path not in " ".join(args) for args in calls)
    assert any("Git blob OID mismatch" in error for error in errors_for(lambda data: data["acceptedInputs"][1].update(gitBlobOid="0" * 40)))
    assert any("role mismatch" in error for error in errors_for(lambda data: data["acceptedInputs"][0].update(role="RUNTIME-SEAM")))


def test_a05_source_mapping_rejects_forged_crs_m2_endpoint_and_layer_relations() -> None:
    assert any("actor does not match" in error for error in errors_for(lambda data: data["sourceRelations"][2].update(actor="DLA")))
    assert any("eventId does not match" in error for error in errors_for(lambda data: data["sourceRelations"][3].update(eventId="EV_DL_DATA_LUR")))
    assert any("event direction" in error for error in errors_for(lambda data: data["sourceRelations"][4].update(eventDirection="TH-TO-DL")))
    assert any("semanticOpcodeClass" in error for error in errors_for(lambda data: data["sourceRelations"][2].update(semanticOpcodeClass="TFTP-DATA-SEMANTIC")))
    assert any("fileRole" in error for error in errors_for(lambda data: data["sourceRelations"][3].update(fileRole="LOAD-LIST")))
    assert any("scenarioRationale" in error for error in errors_for(lambda data: data["sourceRelations"][4].update(scenarioRationale="forged rationale")))
    assert any("sourceUnitId does not match" in error for error in errors_for(lambda data: data["sourceRelations"][0].update(sourceUnitId="SU-FORGED")))
    assert any("document/PDF page" in error for error in errors_for(lambda data: data["sourceRelations"][1].update(documentPage=999)))
    assert any("document/PDF page" in error for error in errors_for(lambda data: data["sourceRelations"][1].update(pdfPage=999)))
    assert any(error.startswith("SCOPE:") for error in errors_for(lambda data: data["scope"].update(preparedButNotExecuted=[])))


def test_a06_finite_no_wrq_public_summary_and_lifecycle_guards_are_not_relaxable() -> None:
    action = next(row for row in PACKAGE["actionLibrary"] if row["id"] == "ACT-INSPECT-NO-WRQ-BEFORE-READY")

    def protocol_timeout(data: dict) -> None:
        next(row for row in data["actionLibrary"] if row["id"] == action["id"])["inspection"]["isProtocolNoResponseVerdict"] = True

    def private_summary(data: dict) -> None:
        next(row for row in data["actionLibrary"] if row["id"] == action["id"])["summaryDerivation"]["forbiddenPrivateSources"].remove("ACTIVE-FAULT-ID")

    def omit_reset(data: dict) -> None:
        data["lifecycle"]["fullReset"]["scope"].remove("PENDING-DELIVERY")

    def stale_recover(data: dict) -> None:
        next(
            row for row in data["cases"] if row["id"] == "CASE-UNKNOWN-RECOVER-CONTINUATION"
        )["rounds"][2]["actionId"] = "ACT-PREP-ENTER-READY-WINDOW"

    assert any("no-WRQ" in error for error in errors_for(protocol_timeout))
    assert any("private summary" in error for error in errors_for(private_summary))
    assert any("full reset scope" in error for error in errors_for(omit_reset))
    assert any("timeline differs" in error for error in errors_for(stale_recover))


def test_a06b_object_contract_locator_resource_case_and_revocation_are_closed() -> None:
    def guard_mutation(field: str, value: object) -> list[str]:
        return errors_for(
            lambda data: next(
                row
                for row in data["objectContract"]["guardTransitions"]
                if row["id"] == "GUARD-TH-ACK-AFTER-MATCHING-WRQ"
            ).update({field: value})
        )

    assert any(
        "state variables" in error
        for error in errors_for(
            lambda data: next(
                row for row in data["objectContract"]["stateVariables"] if row["id"] == "TARGET-LIST-READY"
            ).update(sourceAnchor="M2-VARIABLE:listAccepted")
        )
    )
    assert any(
        "invariant differs" in error
        for error in errors_for(
            lambda data: next(
                row for row in data["objectContract"]["stateVariables"] if row["id"] == "LIST-ACCEPTED"
            ).update(invariant="banana")
        )
    )
    assert any(
        "OBJECT:" in error and "TH-ACK guard requiresState" in error
        for error in guard_mutation("requiresState", ["TH-MATCHING-LUR-WRQ-RECEIVED=FALSE"])
    )
    assert any(
        "OBJECT:" in error and "TH-ACK guard sourceRelationId" in error
        for error in guard_mutation("sourceRelationId", "SRC-LUR-DATA")
    )
    assert any(
        "OBJECT:" in error and "TH-ACK guard normalVisibleOutputId" in error
        for error in guard_mutation("normalVisibleOutputId", "OUT-DL-DATA-LUR")
    )
    assert any(
        "sourceLocator" in error
        for error in errors_for(
            lambda data: next(
                row for row in data["sourceRelations"] if row["id"] == "SRC-LUR-WRQ"
            ).update(sourceLocator="forged locator")
        )
    )
    assert any(
        "opaque-payload boundary" in error
        for error in errors_for(
            lambda data: data["objectContract"]["semanticPayloadBoundary"].update(
                notWirePacketImplementation=False
            )
        )
    )
    assert any(
        "evaluator-only" in error
        for error in errors_for(
            lambda data: data["objectContract"]["privateBoundary"]["algorithmForbidden"].remove("ACTIVE-FAULT-ID")
        )
    )
    assert any(
        "fault revocation" in error
        for error in errors_for(
            lambda data: data["lifecycle"]["faultInjection"].update(
                revocationAction="PERSIST-FAULT-INTO-NEXT-ATTEMPT"
            )
        )
    )
    def resource_errors(field: str, value: object, *, expectation: bool = True) -> list[str]:
        def mutate(data: dict) -> None:
            round_ = next(
                row for row in data["cases"] if row["id"] == "CASE-RESOURCE-ADMISSION-BLOCK"
            )["rounds"][0]
            target = round_["resourceExpectation"] if expectation else round_
            target[field] = value

        return errors_for(mutate)

    for field, value in {
        "admission": "ADMITTED",
        "reason": "POST-DISPATCH-RESOURCE-ERROR",
        "mode": "BUDGET",
        "availableRounds": 1,
        "requiredRounds": 2,
        "actionCostCharged": True,
        "successorDisposition": "ROLL-BACK-SUCCESSOR",
    }.items():
        assert any("resource-admission witness" in error for error in resource_errors(field, value))
    assert any(
        "resource-admission witness" in error
        for error in resource_errors("expectedVisibleEvents", ["EV_DL_WRQ_LUR"], expectation=False)
    )
    assert any(
        "resource-admission witness" in error
        for error in resource_errors("expectedCandidates", ["EARLY-WRQ"], expectation=False)
    )


def test_a06c_action_history_and_bilingual_operational_contracts_are_not_decorative() -> None:
    action_id = "ACT-PREP-ENTER-READY-WINDOW"
    assert any(
        "MAP-PREP-READY existingInterfaceIds differs" in error
        for error in errors_for(
            lambda data: next(
                row for row in data["traceabilityMatrix"] if row["id"] == "MAP-PREP-READY"
            ).update(existingInterfaceIds=["IF-EXECUTE-RECORD", "IF-PREP-RECOVER"])
        )
    )
    assert any(
        "successor confirmation" in error
        for error in errors_for(
            lambda data: next(row for row in data["actionLibrary"] if row["id"] == action_id).update(
                successorConfirmation="SUMMARY-ONLY"
            )
        )
    )
    assert any(
        "Chinese eligibility" in error
        for error in errors_for(
            lambda data: next(row for row in data["actionLibrary"] if row["id"] == action_id)["zh"].update(
                eligibility=" \r\n "
            )
        )
    )
    assert any(
        "Chinese summary confirmation" in error
        for error in errors_for(
            lambda data: next(row for row in data["actionLibrary"] if row["id"] == action_id)[
                "possibleOutcomes"
            ][0].update(summaryConfirmedWhenZh=" ")
        )
    )


def test_a06d_scope_action_lifecycle_experiment_and_private_boundary_contracts_are_controlled() -> None:
    def action_row(data: dict, action_id: str) -> dict:
        return next(row for row in data["actionLibrary"] if row["id"] == action_id)

    assert any(
        error.startswith("DOMAIN:")
        for error in errors_for(
            lambda data: data["hypothesisDomain"]["algorithmMayKnow"].append("ACTIVE-FAULT-ID")
        )
    )
    for field, value in {
        "startBoundary": "FULL-UPLOAD-COMPLETED",
        "endBoundary": "PROTOCOL-NO-RESPONSE-DEADLINE",
        "notEvaluatedObligations": ["NONE"],
    }.items():
        assert any(
            error.startswith("SCOPE:")
            for error in errors_for(lambda data, field=field, value=value: data["scope"].update({field: value}))
        )
    assert any(
        error.startswith("TIME:")
        for error in errors_for(
            lambda data: data["timeAndObservation"].update(
                finiteObservationBoundary="PROTOCOL-NO-RESPONSE-DEADLINE"
            )
        )
    )

    for mutate in (
        lambda data: action_row(data, "ACT-TEST-ACK-BEFORE-DATA")["possibleOutcomes"][0].update(
            observable="FORGED-NORMAL"
        ),
        lambda data: action_row(data, "ACT-TEST-ACK-BEFORE-DATA")["inspection"].update(
            journalPredicate="FORGED-PREDICATE"
        ),
        lambda data: action_row(data, "ACT-TEST-ACK-BEFORE-DATA")["inspection"].update(
            finiteHorizonTicks=99
        ),
        lambda data: action_row(data, "ACT-TEST-ACK-BEFORE-DATA")["cost"].update(acquisition=0),
        lambda data: action_row(data, "ACT-PREP-ENTER-READY-WINDOW")["possibleOutcomes"][0].update(
            observable="FORGED-PREP-OBSERVABLE"
        ),
        lambda data: action_row(data, "ACT-RECOVER-RECONFIRM-READY")["possibleOutcomes"][0].update(
            observable="FORGED-RECOVER-OBSERVABLE"
        ),
    ):
        assert any(error.startswith("ACTION:") for error in errors_for(mutate))

    for mutate in (
        lambda data: data["lifecycle"]["fullReset"].update(successEvidence="FORGED-EVIDENCE"),
        lambda data: data["lifecycle"]["faultInjection"].update(installationEvidence="FORGED-EVIDENCE"),
        lambda data: data["lifecycle"]["faultInjection"].update(activationEvidence="FORGED-EVIDENCE"),
        lambda data: data["lifecycle"]["faultInjection"].update(unconfirmedDisposition="FORGED-EVIDENCE"),
    ):
        assert any(error.startswith("LIFECYCLE:") for error in errors_for(mutate))

    for field, value in {
        "publicProjection": "ACTIVE-FAULT-ID is public",
        "evaluatorProjection": "no evaluator-only data",
        "sharedComponentRisk": "no shared risk",
        "notAdmitted": "formal experiment fully admitted",
    }.items():
        assert any(
            error.startswith("EXPERIMENT:")
            for error in errors_for(
                lambda data, field=field, value=value: next(
                    row for row in data["experimentRelations"] if row["interfaceId"] == "IF-EXP-TRUTH"
                ).update({field: value})
            )
        )

    for mutate in (
        lambda data: next(row for row in data["sourceRelations"] if row["id"] == "SRC-LUR-WRQ")["stateFacts"].update(
            assertions=["FORGED-ASSERTION"]
        ),
        lambda data: next(row for row in data["sourceRelations"] if row["id"] == "SRC-LUR-WRQ").update(
            scenarioRationaleZh="伪造理由"
        ),
    ):
        assert any(error.startswith("SOURCE:") for error in errors_for(mutate))


def test_a07_p3_and_successor_feasibility_witnesses_cannot_borrow_old_applicability() -> None:
    assert any("P3-UNAVAILABLE" in error for error in errors_for(lambda data: next(row for row in data["feasibilityWitnesses"] if row["id"] == "WIT-P3-UNAVAILABLE").update(claim="P3 established")))
    assert any("successor witness" in error for error in errors_for(lambda data: next(row for row in data["feasibilityWitnesses"] if row["id"] == "WIT-SUCCESSOR-AND-RECOVER").update(claim="A generic adapter continues.")))


def test_a08_traceability_matrix_closes_source_interface_witness_and_nonclaim_boundaries() -> None:
    row = next(item for item in PACKAGE["traceabilityMatrix"] if item["id"] == "MAP-LUR-ORDER-TEST")
    assert row["sourceRelationIds"] == ["SRC-LUR-WRQ", "SRC-LUR-ACK", "SRC-LUR-DATA"]
    assert row["existingInterfaceIds"] == ["IF-EXECUTE-RECORD", "IF-OBS-INTERPRET", "IF-HIST-UPDATE"]
    assert "LUR-PAYLOAD-INTEGRITY" in row["notCovered"]
    assert any("existingInterfaceIds differs" in error for error in errors_for(lambda data: next(item for item in data["traceabilityMatrix"] if item["id"] == row["id"]).update(existingInterfaceIds=["IF-EQUIV"])))
    assert any("sourceRelationIds differs" in error for error in errors_for(lambda data: next(item for item in data["traceabilityMatrix"] if item["id"] == row["id"]).update(sourceRelationIds=["SRC-LUR-WRQ"])))
    assert any("acceptanceWitnessIds differs" in error for error in errors_for(lambda data: next(item for item in data["traceabilityMatrix"] if item["id"] == row["id"]).update(acceptanceWitnessIds=["WIT-FINITE-NO-WRQ-TEST"])))
    assert any("non-claim boundary" in error for error in errors_for(lambda data: next(item for item in data["traceabilityMatrix"] if item["id"] == row["id"]).update(notCovered=[])))


def test_a08a_experiment_handoffs_declare_public_evaluator_risk_and_nonadmission_boundaries() -> None:
    relation = next(row for row in PACKAGE["experimentRelations"] if row["interfaceId"] == "IF-EXP-TRUTH")
    assert relation["publicProjection"]
    assert relation["evaluatorProjection"]
    assert relation["sharedComponentRisk"]
    assert relation["notAdmitted"]
    assert relation["zh"]["sharedComponentRisk"]
    assert any(
        "sharedComponentRisk" in error
        for error in errors_for(
            lambda data: next(
                row for row in data["experimentRelations"] if row["interfaceId"] == "IF-EXP-TRUTH"
            ).update(sharedComponentRisk=" ")
        )
    )
    assert any(
        "Chinese notAdmitted" in error
        for error in errors_for(
            lambda data: next(
                row for row in data["experimentRelations"] if row["interfaceId"] == "IF-EXP-RUN"
            )["zh"].update(notAdmitted=" ")
        )
    )


def test_a08b_resource_admission_and_single_fault_contracts_cannot_be_relaxed() -> None:
    assert any(
        "admission/accounting ownership" in error
        for error in errors_for(lambda data: data["resourceContract"].update(admissionOwner="IF-EXECUTE-RECORD"))
    )
    assert any(
        "controlled modes" in error
        for error in errors_for(lambda data: data["resourceContract"].update(allowedModes=["ROUNDS"]))
    )
    assert any(
        "post-dispatch successor boundary" in error
        for error in errors_for(lambda data: data["resourceContract"].update(postDispatchError="ROLL-BACK-ON-ERROR"))
    )
    assert any(
        "non-claim boundaries" in error
        for error in errors_for(lambda data: data["resourceContract"].update(notEvaluated=["REAL-HARDWARE-COST"]))
    )

    def wrong_activation(data: dict) -> None:
        next(
            row
            for row in data["lifecycle"]["faultInjection"]["variants"]
            if row["hypothesisId"] == "EARLY-WRQ"
        )["activationObservable"] = "EV_DL_WRQ_LUR-AFTER-EV_TH_LUS0001"

    def duplicate_variant(data: dict) -> None:
        data["lifecycle"]["faultInjection"]["variants"][1]["hypothesisId"] = "EARLY-WRQ"

    assert any("EARLY-WRQ activationObservable" in error for error in errors_for(wrong_activation))
    assert any("fault variants" in error for error in errors_for(duplicate_variant))


def test_a09_generated_bilingual_view_renders_controlled_fields_by_section_and_detects_drift() -> None:
    def section(text: str, heading: str) -> str:
        start = text.index(heading)
        next_heading = text.find("\n## ", start + len(heading))
        return text[start:] if next_heading < 0 else text[start:next_heading]

    def record_line(text: str, record_id: str) -> str:
        return next(line for line in text.splitlines() if line.startswith(f"| {record_id} |"))

    rendered = reader.render(PACKAGE)
    english, chinese = rendered.split("# 中文版", 1)
    action = next(row for row in PACKAGE["actionLibrary"] if row["id"] == "ACT-TEST-ACK-BEFORE-DATA")
    source = next(row for row in PACKAGE["sourceRelations"] if row["id"] == "SRC-LUR-WRQ")
    control = PACKAGE["controlBinding"]
    resource = PACKAGE["resourceContract"]
    contract = PACKAGE["objectContract"]
    resource_case = next(row for row in PACKAGE["cases"] if row["id"] == "CASE-RESOURCE-ADMISSION-BLOCK")
    experiment = next(row for row in PACKAGE["experimentRelations"] if row["interfaceId"] == "IF-EXP-TRUTH")
    english_action = section(english, f"### `{action['id']}`")
    chinese_action = section(chinese, f"### `{action['id']}`")
    english_sources = section(english, "## Source-to-model control relations")
    chinese_sources = section(chinese, "## 来源到模型的控制关系")
    english_source_row = record_line(english_sources, source["id"])
    chinese_source_row = record_line(chinese_sources, source["id"])
    assert f"- Eligibility: {action['eligibility']}" in english_action
    assert action["zh"]["eligibility"] in chinese_action
    assert action["zh"]["eligibility"] not in english_action
    assert control["controlCommit"] in english and control["controlCommit"] in chinese
    assert control["rawSha256"] in english and control["rawSha256"] in chinese
    assert source["scenarioRationale"] in english_source_row
    assert source["scenarioRationaleZh"] in chinese_source_row
    assert source["scenarioRationaleZh"] not in english_source_row
    assert action["eligibility"] in english
    assert action["publicStimulus"] in english
    assert action["successorConfirmation"] in english
    assert action["zh"]["eligibility"] in chinese
    assert action["zh"]["historyDisposition"] in chinese
    assert action["possibleOutcomes"][0]["summaryConfirmedWhenZh"] in chinese
    assert source["stateFacts"]["before"] in english
    assert source["sourceLocator"] in english and source["semanticOpcodeClass"] in english and source["fileRole"] in english
    assert source["scenarioRationale"] in english and source["scenarioRationaleZh"] in chinese
    assert PACKAGE["translationsZh"]["actions.ACT-TEST-ACK-BEFORE-DATA.summary"] in chinese
    assert PACKAGE["translationsZh"]["sourceRelations.SRC-LUR-WRQ.summary"] in chinese
    assert PACKAGE["translationsZh"]["resourceContract.summary"] in chinese
    assert "对象与对端合同" in chinese and "状态边界" in chinese and "实验接口交接" in chinese and "A 阶段来源／接口／验收矩阵" in chinese
    assert contract["stateVariables"][0]["invariant"] in english
    assert contract["stateVariables"][0]["meaningZh"] in chinese
    assert contract["guardTransitions"][0]["meaningZh"] in chinese
    assert contract["lifecycleBoundary"]["faultRevocationAction"] in english
    assert contract["implementationIdentityPlan"]["meaningZh"] in chinese
    for field in ("admissionOwner", "accountingOwner", "admissionBoundary", "postDispatchError"):
        assert resource[field] in english
        assert resource[field] in chinese
    for field in ("roundsMeaning", "budgetMeaning", "admissionBoundary", "postDispatchError", "notEvaluated"):
        assert resource["zh"][field] in chinese
    for variant in PACKAGE["lifecycle"]["faultInjection"]["variants"]:
        for field in ("hypothesisId", "installationTarget", "activationObservable", "controllerReadback", "algorithmVisibility"):
            assert variant[field] in english
            assert variant[field] in chinese
    expectation = resource_case["rounds"][0]["resourceExpectation"]
    for value in expectation.values():
        if value is False:
            assert "no" in english.lower() and "否" in chinese
        else:
            assert str(value) in english
            assert str(value) in chinese
    for field in ("publicProjection", "evaluatorProjection", "sharedComponentRisk", "notAdmitted"):
        assert experiment[field] in english
        assert experiment["zh"][field] in chinese

    changed = copy.deepcopy(PACKAGE)
    next(row for row in changed["actionLibrary"] if row["id"] == action["id"])["eligibility"] += " drift"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    changed["translationsZh"]["actions.ACT-TEST-ACK-BEFORE-DATA.summary"] += " 漂移"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    next(row for row in changed["sourceRelations"] if row["id"] == source["id"])["stateFacts"]["before"] = "forged-state"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    next(row for row in changed["sourceRelations"] if row["id"] == source["id"])["stateFacts"]["assertions"][0] = "forged assertion"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    next(row for row in changed["traceabilityMatrix"] if row["id"] == "MAP-LUR-ORDER-TEST")["visibleEvidence"] += " drift"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    changed["resourceContract"]["postDispatchError"] = "ROLL-BACK-ON-ERROR"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    changed["lifecycle"]["faultInjection"]["variants"][0]["controllerReadback"] = "FORGED-READBACK"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    changed["objectContract"]["stateVariables"][0]["invariant"] = "forged invariant"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    next(row for row in changed["actionLibrary"] if row["id"] == action["id"])["zh"]["eligibility"] += " 漂移"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    next(row for row in changed["sourceRelations"] if row["id"] == source["id"])["scenarioRationaleZh"] += " 漂移"
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    next(row for row in changed["cases"] if row["id"] == resource_case["id"])["rounds"][0]["resourceExpectation"]["availableRounds"] = 7
    assert reader.render(changed) != rendered
    changed = copy.deepcopy(PACKAGE)
    next(row for row in changed["experimentRelations"] if row["interfaceId"] == experiment["interfaceId"])["zh"]["sharedComponentRisk"] += " 漂移"
    assert reader.render(changed) != rendered


def test_a10_reader_escapes_tables_and_refuses_invalid_package_without_overwrite(
    isolated_snapshot_repo: tuple[Path, dict],
) -> None:
    root, candidate = isolated_snapshot_repo
    package_path = root / checker.PACKAGE_PATH
    assert reader.sync(root, write=True)[0]
    view = root / reader.VIEW_PATH
    before = view.read_bytes()

    invalid = copy.deepcopy(candidate)
    invalid["translationsZh"]["scope.summary"] = "line one\r\nline two | `literal`"
    package_path.write_text(json.dumps(invalid, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert reader.sync(root, write=True)[0]
    assert reader.sync(root, write=False)[0]
    rendered = view.read_text(encoding="utf-8")
    english, chinese = rendered.split("# 中文版", 1)
    assert r"line one<br>line two \| \`literal\`" in chinese
    assert r"line one<br>line two \| \`literal\`" not in english
    assert "line one\r\nline two" not in rendered

    stale = copy.deepcopy(invalid)
    stale["identity"]["version"] = "0.1.0-candidate-view-drift"
    package_path.write_text(json.dumps(stale, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    current = view.read_bytes()
    ok, message = reader.sync(root, write=False)
    assert not ok and "stale" in message
    assert view.read_bytes() == current

    stale["sourceRelations"][2]["actor"] = "DLA"
    package_path.write_text(json.dumps(stale, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    latest = view.read_bytes()
    ok, message = reader.sync(root, write=True)
    assert not ok and "validation failed" in message
    assert view.read_bytes() == latest
    assert latest != before


def test_a10b_invalid_first_publication_leaves_no_partial_reader_view(
    isolated_snapshot_repo: tuple[Path, dict],
) -> None:
    root, candidate = isolated_snapshot_repo
    view = root / reader.VIEW_PATH
    assert not view.exists()
    candidate["sourceRelations"][2]["actor"] = "DLA"
    (root / checker.PACKAGE_PATH).write_text(
        json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    ok, message = reader.sync(root, write=True)
    assert not ok and "validation failed" in message
    assert not view.exists()


def test_a11_cli_returns_named_failure_and_preserves_reader_on_invalid_package(
    isolated_snapshot_repo: tuple[Path, dict], capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch,
) -> None:
    root, candidate = isolated_snapshot_repo
    assert reader.sync(root, write=True)[0]
    view = root / reader.VIEW_PATH
    before = view.read_bytes()
    candidate["sourceRelations"][1]["eventId"] = "EV_DL_WRQ_LUR"
    (root / checker.PACKAGE_PATH).write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert checker.main(["--root", str(root)]) == 1
    captured = capsys.readouterr()
    assert "SOURCE:" in captured.err
    monkeypatch.setattr(sys, "argv", ["sync_615a_scenarios.py", "--root", str(root), "--write"])
    assert reader.main() == 1
    assert view.read_bytes() == before
