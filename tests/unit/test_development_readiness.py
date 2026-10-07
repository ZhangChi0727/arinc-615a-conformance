import copy
import importlib.util
import json
from pathlib import Path
import hashlib
import shutil
import subprocess
import sys
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("development_readiness", ROOT / "scripts" / "check_development_readiness.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
sys.path.insert(0, str(ROOT / "scripts"))
SYNC_SPEC = importlib.util.spec_from_file_location("sync_development_readiness", ROOT / "scripts" / "sync_development_readiness.py")
assert SYNC_SPEC and SYNC_SPEC.loader
SYNC = importlib.util.module_from_spec(SYNC_SPEC)
SYNC_SPEC.loader.exec_module(SYNC)
PACKAGE = json.loads((ROOT / "configs" / "engineering" / "cltav_development_contracts.json").read_text(encoding="utf-8"))


def errors(data):
    return MODULE.package_errors(data)


def run_main(monkeypatch, tmp_path, capsys, data):
    package = tmp_path / "package.json"
    package.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(MODULE, "PACKAGE_PATH", package)
    code = MODULE.main()
    return code, capsys.readouterr()


def test_current_candidate_has_closed_specification_gate():
    assert PACKAGE["reviewBoundary"]["readiness"] == "CANDIDATE"
    assert errors(copy.deepcopy(PACKAGE)) == []


def test_rr85_capture_manifest_rows_enter_capture_and_packet_records() -> None:
    manifest = json.loads((ROOT / "configs/research/cltav_historical_capture_manifest.json").read_text(encoding="utf-8"))
    records = {row["id"]: row for row in PACKAGE["recordContracts"]}
    for row in manifest["captures"]:
        identity = {"captureId": row["captureId"], "relativePath": row["relativePath"], "sha256": row["sha256"], "byteSize": row["byteCount"], "manifestVersion": manifest["manifestVersion"]}
        assert MODULE.validate_record_instance(records["CAPTURE-IDENTITY"], identity) == []
        packet = copy.deepcopy(records["PACKET-REF"]["example"])
        packet["captureId"] = row["captureId"]
        assert MODULE.validate_record_instance(records["PACKET-REF"], packet) == []
    for attack in ("../escape.pcapng", "/absolute.pcapng", "C" + ":/outside.pcapng", "safe\\alias.pcapng"):
        payload = copy.deepcopy(records["CAPTURE-IDENTITY"]["example"])
        payload["relativePath"] = attack
        assert MODULE.validate_record_instance(records["CAPTURE-IDENTITY"], payload)


def test_rr85_empty_history_is_terminal_only_and_never_resurrects() -> None:
    history = next(row for row in PACKAGE["recordContracts"] if row["id"] == "HISTORY-HANDLE")
    terminal = {"H": [], "compatibleStateByHypothesis": {}, "statusByHypothesis": {}, "version": 1}
    assert MODULE.validate_record_instance(history, terminal) == []
    case = next(row for row in PACKAGE["acceptanceCases"] if row["id"] == "AC-SYN-HISTORY")
    assert case["inputFixture"]["values"]["history"]["H"] == ["h0"]
    assert case["expectedOutputFixture"]["values"]["history"]["H"] == []
    assert case["expectedOutputFixture"]["values"]["stop"] == "Stop-Empty"


def test_rr85_kernel_relations_reject_coordinated_mutations() -> None:
    bad = copy.deepcopy(PACKAGE)
    bad["algorithmRefinements"][0]["finiteKernelContract"]["mergeKey"].remove("clockConstraint")
    assert any("merge key" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["algorithmRefinements"][0]["finiteKernelContract"]["limitBehavior"]["pathLength"] = "Stop-Empty"
    assert any("limit behavior" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["algorithmRefinements"][0]["finiteKernelContract"]["totalReturnMapping"].pop()
    assert any("total finite-result" in item or "is too short" in item for item in errors(bad))


def test_rr85_experiment_cases_are_bidirectional_and_concrete() -> None:
    case_by_id = {row["id"]: row for row in PACKAGE["acceptanceCases"]}
    for binding in PACKAGE["experimentInterfaceBindings"]:
        for case_id in binding["acceptanceCaseIds"]:
            case = case_by_id[case_id]
            assert binding["interfaceId"] in case["experimentInterfaceIds"]
            assert case["inputFixture"]["values"] and case["expectedOutputFixture"]["values"]
    bad = copy.deepcopy(PACKAGE)
    binding = bad["experimentInterfaceBindings"][0]
    binding["acceptanceCaseIds"] = ["AC-SYN-TRANSFER"]
    assert any("experiment interface" in item for item in errors(bad))


def test_rr85_dependency_and_activation_gates_reject_joint_forgery() -> None:
    bad = copy.deepcopy(PACKAGE)
    dependency = bad["implementationDependencies"][0]
    removed = dependency["requirementIds"].pop()
    dependency["sourceBindings"] = [row for row in dependency["sourceBindings"] if row["requirementId"] != removed]
    next(row for row in bad["protocolInputDispositions"] if row["inputRequirementId"] == removed)["dependencyIds"] = []
    assert any("required dependency relation" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["implementationDependencies"][0]["sourceBindings"][0]["sourceUnitId"] = "SU-NOT-REAL"
    assert any("forged source binding" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["implementationDependencies"][0]["runtimeStatus"] = "ESTABLISHED"
    assert any("cannot be established" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["reviewBoundary"]["readiness"] = "READY"
    assert any("outside this Draft" in item for item in errors(bad))


def test_finite_kernel_and_experiment_bindings_are_relationally_closed():
    assert len(PACKAGE["experimentInterfaceBindings"]) == 7
    bad = copy.deepcopy(PACKAGE)
    bad["algorithmRefinements"][0]["finiteKernelContract"]["mergeKey"].remove("historyProvenance")
    assert any("whole-history provenance" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["experimentInterfaceBindings"][0]["inputTypes"] = ["fabricated"]
    assert any("experiment I/O differs" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["experimentInterfaceBindings"][0]["failureBehavior"] = "fabricated"
    assert any("failure/resource" in item for item in errors(bad))


def test_integrity_specification_closure_does_not_claim_runtime_capability():
    dependency = PACKAGE["implementationDependencies"][0]
    assert dependency["specificationStatus"] == "CLOSED"
    assert dependency["runtimeStatus"] == "NOT-ESTABLISHED"
    assert dependency["affectsSpecificationReadiness"] is False
    assert len(dependency["requirementIds"]) == 6
    bad = copy.deepcopy(PACKAGE)
    bad["implementationDependencies"][0]["failureBehavior"] = "return PASS"
    assert any("runtime not-evaluated boundary" in item for item in errors(bad))


def test_acceptance_fixtures_cannot_drift_from_controlled_cases():
    bad = copy.deepcopy(PACKAGE)
    bad["acceptanceCases"][0]["inputFixture"]["recordIds"] = ["PACKET-REF"]
    assert any("fixture record identities differ" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["acceptanceCases"][0]["expectedOutputFixture"]["statement"] = "fabricated"
    assert any("expected fixture differs" in item for item in errors(bad))


def test_cross_path_matrix_and_first_batch_scenarios_are_production_checked():
    assert len(PACKAGE["acceptanceMatrix"]) == 14
    assert len(PACKAGE["experimentScenarios"]) == 8
    bad = copy.deepcopy(PACKAGE)
    bad["acceptanceMatrix"][0]["category"] = bad["acceptanceMatrix"][1]["category"]
    assert any("each controlled category exactly once" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["experimentScenarios"][0]["algorithmVisibleFields"].append("truthRecord")
    assert any("leaks evaluator truth" in item for item in errors(bad))


def test_slice_identity_and_edge_rules():
    duplicate_id = copy.deepcopy(PACKAGE)
    duplicate_id["implementationSlices"].append({"id": duplicate_id["implementationSlices"][0]["id"], "scope": "different", "scopeZh": "不同", "requirementIds": ["CRS-M1-00420"]})
    assert any("repeats a slice ID" in item for item in errors(duplicate_id))

    duplicate_edge = copy.deepcopy(PACKAGE)
    duplicate_edge["implementationSlices"][0]["requirementIds"].append(duplicate_edge["implementationSlices"][0]["requirementIds"][0])
    assert any("repeats a requirement use" in item for item in errors(duplicate_edge))

    shared = copy.deepcopy(PACKAGE)
    shared["implementationSlices"].append({"id": "SLICE-SHARED", "scope": "legal shared consumer", "scopeZh": "合法共享消费者", "requirementIds": [shared["implementationSlices"][0]["requirementIds"][0]]})
    assert errors(shared) == []


def test_use_edges_must_resolve_to_m1_and_disposition():
    non_m1 = copy.deepcopy(PACKAGE)
    non_m1["implementationSlices"][0]["requirementIds"].append("CRS-M1-99999")
    assert any("non-M1" in item for item in errors(non_m1))

    required = next(row for row in PACKAGE["protocolInputDispositions"] if row["firstSliceRequired"] and row["disposition"] == "FIRST-SLICE-IMPLEMENTATION")
    downgraded = copy.deepcopy(PACKAGE)
    row = next(item for item in downgraded["protocolInputDispositions"] if item["inputRequirementId"] == required["inputRequirementId"])
    row.update(disposition="NOT-TOOL-OBLIGATION")
    row.pop("moduleId"); row.pop("recordId"); row.pop("acceptanceCaseId")
    assert any("required use has no implementation" in item for item in errors(downgraded))


def test_all_first_slice_references_are_closed_independently():
    row = next(item for item in PACKAGE["protocolInputDispositions"] if item["disposition"] == "FIRST-SLICE-IMPLEMENTATION")
    for field in ("moduleId", "recordId", "acceptanceCaseId"):
        mutated = copy.deepcopy(PACKAGE)
        target = next(item for item in mutated["protocolInputDispositions"] if item["inputRequirementId"] == row["inputRequirementId"])
        target[field] = "MISSING-REFERENCE"
        assert errors(mutated), field


def test_candidate_requires_completion_evidence_and_closed_dependencies():
    for evidence in ([], [""], ["   "]):
        mutated = copy.deepcopy(PACKAGE)
        mutated["reviewBoundary"]["completionEvidence"] = evidence
        assert any("candidate readiness requires" in item for item in errors(mutated))
    mutated = copy.deepcopy(PACKAGE)
    mutated["implementationDependencies"][0]["specificationStatus"] = "OPEN"
    mutated["implementationDependencies"][0]["affectsSpecificationReadiness"] = True
    assert any("READINESS-BLOCKED" in item for item in errors(mutated))


def test_candidate_gate_survives_actual_relation_pruning(monkeypatch, tmp_path, capsys):
    mutated = copy.deepcopy(PACKAGE)
    target = next(row for row in mutated["protocolInputDispositions"] if row["inputRequirementId"] == "CRS-M1-00076")
    target["dependencyIds"] = []
    code, captured = run_main(monkeypatch, tmp_path, capsys, mutated)
    assert code == 1
    assert "dependency" in captured.err


def test_main_returns_exit_codes_for_candidate_and_bad_binding(monkeypatch, tmp_path, capsys):
    code, captured = run_main(monkeypatch, tmp_path, capsys, copy.deepcopy(PACKAGE))
    assert code == 0
    assert "readiness=CANDIDATE" in captured.out
    bad = copy.deepcopy(PACKAGE)
    bad["inputBindings"][0]["sha256"] = "0" * 64
    code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
    assert code == 1
    assert "content identity differs" in captured.err
    bad = copy.deepcopy(PACKAGE)
    bad["recordContracts"][0]["fieldDefinitions"]["byteSize"] = {"type": "banana", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True}
    code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
    assert code == 1
    assert "unsupported type" in captured.err
    bad = copy.deepcopy(PACKAGE)
    bad["recordContracts"][0]["fieldDefinitions"]["relativePath"]["minLength"] = -1
    code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
    assert code == 1
    assert "non-negative integer" in captured.err
    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["recordContracts"] if item["id"] == "HISTORY-HANDLE")["example"]["H"] = [{}]
    code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
    assert code == 1
    assert "example is invalid" in captured.err
    bad = copy.deepcopy(PACKAGE)
    bad["recordContracts"][0]["fieldDefinitions"]["sha256"]["pattern"] = "a{4294967296}"
    code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
    assert code == 1
    assert "valid regular expression" in captured.err
    bad = copy.deepcopy(PACKAGE)
    bad["moduleContracts"][0]["upstreamModuleIds"] = ["MISSING-MODULE"]
    code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
    assert code == 1
    assert "invalid upstream module" in captured.err


def test_invalid_output_record_definition_has_named_diagnostic_not_mapping_exception(monkeypatch, tmp_path, capsys):
    for malformed in (None, "not-a-field-definition"):
        bad = copy.deepcopy(PACKAGE)
        datagram = next(item for item in bad["recordContracts"] if item["id"] == "DATAGRAM-RECORD")
        datagram["fieldDefinitions"]["reassemblyStatus"] = malformed
        code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
        assert code == 1
        assert "DATAGRAM-RECORD.reassemblyStatus field definition must be a nonempty object" in captured.err
        assert "AttributeError" not in captured.err


def test_bounded_algorithm_bindings_parameters_and_acceptance_cases_are_closed():
    candidate = copy.deepcopy(PACKAGE)
    refinement = candidate["algorithmRefinements"][0]
    registry = json.loads((ROOT / "configs" / "research" / "cltav_interface_registry.json").read_text(encoding="utf-8"))
    registry_ids = {row["id"] for row in registry["interfaces"]}
    assert {binding["interfaceId"] for binding in refinement["interfaceBindings"]} == registry_ids
    assert {case["runtimeExecutionStatus"] for case in candidate["acceptanceCases"]} == {"NOT-EXECUTED"}
    assert errors(candidate) == []

    missing = copy.deepcopy(candidate)
    missing["algorithmRefinements"][0]["interfaceBindings"] = missing["algorithmRefinements"][0]["interfaceBindings"][1:]
    assert errors(missing)

    wrong_io = copy.deepcopy(candidate)
    wrong_io["algorithmRefinements"][0]["interfaceBindings"][0]["outputTypes"] = ["fabricated"]
    assert any("output types differ" in item for item in errors(wrong_io))

    bad_case = copy.deepcopy(candidate)
    bad_case["acceptanceCases"][0]["toolRequirementIds"] = []
    assert errors(bad_case)

    detached = copy.deepcopy(candidate)
    detached["acceptanceCases"][0]["toolRequirementIds"].remove("TR-CAPTURE-INTAKE")
    assert any("TR-CAPTURE-INTAKE is absent from its acceptance case" in item for item in errors(detached))

    stale = SYNC.render(candidate)
    for binding in refinement["interfaceBindings"]:
        assert binding["timeContract"] in stale
        assert binding["timeContractZh"] in stale
    for parameter in candidate["runtimeParameterContracts"]:
        assert parameter["exhaustionBehavior"] in stale
        assert parameter["exhaustionBehaviorZh"] in stale


def test_algorithm_acceptance_edges_and_retry_domain_are_not_substitutable():
    assert errors(copy.deepcopy(PACKAGE)) == []
    bad = copy.deepcopy(PACKAGE)
    select = next(item for item in bad["algorithmRefinements"][0]["interfaceBindings"] if item["interfaceId"] == "IF-SELECT-ADMIT")
    select["writeOwnership"] = "Writes SelectSnapshot."
    assert "IF-SELECT-ADMIT must remain read-only; S3-SNAP constructs the final SelectSnapshot" in errors(bad)

    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["runtimeParameterContracts"] if item["id"] == "RP-RETRY-CAP")["domain"] = "NONNEGATIVE-INTEGER"
    assert "RP-RETRY-CAP must retain the existing positive-integer domain" in errors(bad)

    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["acceptanceCases"] if item["id"] == "AC-SYN-HISTORY")["moduleIds"] = ["MOD-CAPTURE"]
    assert "AC-SYN-HISTORY tool TR-HISTORY-COMPATIBILITY omits owner module MOD-OBSERVATION" in errors(bad)

    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["algorithmRefinements"][0]["interfaceBindings"] if item["interfaceId"] == "IF-PRED-OBS")["acceptanceCaseIds"] = ["AC-SYN-RESOURCE-STOP"]
    assert "IF-PRED-OBS acceptance case AC-SYN-RESOURCE-STOP omits that interface" in errors(bad)

    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["runtimeParameterContracts"] if item["id"] == "RP-RETRY-CAP")["acceptanceCaseIds"] = ["AC-SYN-PREDICTION"]
    assert "RP-RETRY-CAP acceptance case AC-SYN-PREDICTION has no parameter consumer" in errors(bad)


def test_bilingual_algorithm_contract_fields_are_rendered_by_section_and_detect_staleness():
    rendered = SYNC.render(copy.deepcopy(PACKAGE))
    english, chinese = rendered.split("# 中文版", 1)
    binding = PACKAGE["algorithmRefinements"][0]["interfaceBindings"][0]
    parameter = PACKAGE["runtimeParameterContracts"][0]
    case = PACKAGE["acceptanceCases"][0]
    assert binding["readOwnership"] in english and binding["writeOwnership"] in english
    assert binding["readOwnershipZh"] in chinese and binding["writeOwnershipZh"] in chinese
    assert parameter["ownerScope"] in english and parameter["ownerScopeZh"] in chinese
    assert case["expectedContractOutput"] in english and case["prohibitedOutput"] in english
    assert case["expectedContractOutputZh"] in chinese and case["prohibitedOutputZh"] in chinese
    for target, field in ((binding, "readOwnershipZh"), (parameter, "ownerScopeZh"), (case, "expectedContractOutputZh"), (case, "prohibitedOutputZh")):
        changed = copy.deepcopy(PACKAGE)
        changed_target = next(item for item in changed["algorithmRefinements"][0]["interfaceBindings"] if item["interfaceId"] == binding["interfaceId"]) if target is binding else next(item for item in changed["runtimeParameterContracts"] if item["id"] == parameter["id"]) if target is parameter else next(item for item in changed["acceptanceCases"] if item["id"] == case["id"])
        changed_target[field] += " drift"
        assert SYNC.render(changed) != rendered


def test_blank_bilingual_algorithm_contract_fields_are_rejected_without_publishing(monkeypatch, tmp_path, capsys):
    mutations = (
        ("interfaceBindings", "readOwnershipZh"),
        ("interfaceBindings", "writeOwnershipZh"),
        ("runtimeParameterContracts", "ownerScopeZh"),
        ("acceptanceCases", "expectedContractOutputZh"),
        ("acceptanceCases", "prohibitedOutputZh"),
    )
    package = tmp_path / "blank-package.json"
    view = tmp_path / "blank-review.md"
    monkeypatch.setattr(SYNC, "PACKAGE", package)
    monkeypatch.setattr(SYNC, "VIEW", view)
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--write"])
    for collection, field in mutations:
        bad = copy.deepcopy(PACKAGE)
        if collection == "interfaceBindings":
            item = bad["algorithmRefinements"][0][collection][0]
        else:
            item = bad[collection][0]
        item[field] = " \t\n "
        assert any(f"blank {field}" in error for error in errors(bad))
        code, captured = run_main(monkeypatch, tmp_path, capsys, bad)
        assert code == 1 and f"blank {field}" in captured.err
        package.write_text(json.dumps(bad), encoding="utf-8")
        view.write_text("preserve-view\n", encoding="utf-8")
        assert SYNC.main() == 1
        assert view.read_text(encoding="utf-8") == "preserve-view\n"


def test_bound_inputs_are_consumed_once_from_git_blobs_not_worktree(monkeypatch):
    bound_paths = {ROOT / item["path"] for item in PACKAGE["inputBindings"]}
    original_read_text = Path.read_text
    original_check_output = MODULE.subprocess.check_output
    reads = []

    def reject_bound_worktree_reads(path, *args, **kwargs):
        if path in bound_paths:
            raise AssertionError("bound input was consumed from the worktree")
        return original_read_text(path, *args, **kwargs)

    def count_blob_reads(command, *args, **kwargs):
        if command[:2] == ["git", "show"]:
            reads.append(command[2])
        return original_check_output(command, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", reject_bound_worktree_reads)
    monkeypatch.setattr(MODULE.subprocess, "check_output", count_blob_reads)
    assert errors(copy.deepcopy(PACKAGE)) == []
    expected = {f"HEAD:{item['path']}" for item in PACKAGE["inputBindings"]}
    assert set(reads) == expected
    assert len(reads) == len(expected)


def test_bound_git_snapshot_survives_bad_worktree_inputs(monkeypatch, tmp_path):
    """The verifier must consume committed bytes, not any worktree read API."""
    repo = tmp_path / "snapshot-repo"
    for relative in (
        "configs/requirements/arinc_615a3_m1_crs.json",
            "configs/research/cltav_interface_registry.json",
            "configs/engineering/cltav_integrity_obligation_baseline.json",
            "configs/engineering/cltav_development_contracts.schema.json",
            "configs/engineering/cltav_development_contracts.json",
            "tests/unit/test_development_readiness.py",
        "docs/control/decisions/DESIGN_DECISIONS.md",
        "docs/control/changes/CR-2026-016.md",
        "docs/research/methodology/RR-2026-001_test_analysis_conformance_methodology.md",
    ):
        source = ROOT / relative
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "snapshot"], cwd=repo, check=True)

    candidate = copy.deepcopy(PACKAGE)
    for binding in candidate["inputBindings"]:
        raw = subprocess.check_output(["git", "show", f"HEAD:{binding['path']}"], cwd=repo)
        binding["sha256"] = hashlib.sha256(raw).hexdigest()

    # Deliberately invalid worktree bytes after the immutable snapshot exists.
    (repo / "configs/requirements/arinc_615a3_m1_crs.json").write_text("{}", encoding="utf-8")
    (repo / "configs/research/cltav_interface_registry.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(MODULE, "ROOT", repo)
    monkeypatch.setattr(MODULE, "SCHEMA_PATH", repo / "configs/engineering/cltav_development_contracts.schema.json")
    monkeypatch.setattr(MODULE, "M1_PATH", repo / "configs/requirements/arinc_615a3_m1_crs.json")
    assert errors(candidate) == []


def test_missing_and_forged_references_report_the_target_contract():
    row = next(item for item in PACKAGE["protocolInputDispositions"] if item["disposition"] == "FIRST-SLICE-IMPLEMENTATION")
    for field, label in (("moduleId", "module"), ("recordId", "record"), ("acceptanceCaseId", "acceptance case")):
        for value in (None, "MISSING-REFERENCE"):
            mutated = copy.deepcopy(PACKAGE)
            target = next(item for item in mutated["protocolInputDispositions"] if item["inputRequirementId"] == row["inputRequirementId"])
            if value is None:
                target.pop(field)
            else:
                target[field] = value
            assert any(label in item for item in errors(mutated))


def test_legal_new_use_then_isolated_downgrade():
    candidate = copy.deepcopy(PACKAGE)
    extra = next(row for row in candidate["protocolInputDispositions"] if not row["firstSliceRequired"])
    candidate["implementationSlices"][0]["requirementIds"].append(extra["inputRequirementId"])
    extra.update(firstSliceRequired=True, disposition="FIRST-SLICE-IMPLEMENTATION", rationale="Synthetic legal first-slice extension.", moduleId="MOD-TRANSFER", recordId="PROTOCOL-EVENT", acceptanceCaseId="AC-SYN-TRANSFER")
    assert errors(candidate) == []
    extra["disposition"] = "NOT-TOOL-OBLIGATION"
    assert any("required use has no implementation" in item for item in errors(candidate))


def test_typed_tool_contracts_have_closed_module_record_case_and_interface_references():
    assert len(PACKAGE["toolRequirements"]) >= 8
    assert errors(copy.deepcopy(PACKAGE)) == []
    for field, value, diagnostic in (
        ("ownerModuleId", "UNKNOWN-MODULE", "owner module"),
        ("acceptanceCaseId", "UNKNOWN-CASE", "acceptance case"),
    ):
        candidate = copy.deepcopy(PACKAGE)
        candidate["toolRequirements"][0][field] = value
        assert any(diagnostic in item for item in errors(candidate))
    candidate = copy.deepcopy(PACKAGE)
    candidate["toolRequirements"][0]["inputRecordIds"] = ["UNKNOWN-RECORD"]
    assert any("record reference" in item for item in errors(candidate))
    candidate = copy.deepcopy(PACKAGE)
    candidate["toolRequirements"][4]["interfaceIds"] = ["UNKNOWN-INTERFACE"]
    assert any("interface reference" in item for item in errors(candidate))
    candidate = copy.deepcopy(PACKAGE)
    candidate["toolRequirements"][2]["protocolRequirementIds"] = ["CRS-M1-99999"]
    assert any("protocol requirement reference" in item for item in errors(candidate))
    history = next(item for item in PACKAGE["toolRequirements"] if item["id"] == "TR-HISTORY-COMPATIBILITY")
    assert history["interfaceIds"] == ["IF-HIST-UPDATE"]


def test_tool_contracts_reject_blank_text_and_unresolved_traceability():
    candidate = copy.deepcopy(PACKAGE)
    candidate["toolRequirements"][0]["triggerZh"] = " \r\n "
    assert any("blank triggerZh" in item for item in errors(candidate))
    candidate = copy.deepcopy(PACKAGE)
    candidate["toolRequirements"][0]["traceability"] = ["DD-999"]
    assert any("unknown DD traceability" in item for item in errors(candidate))
    for reference in ("DD-04", "CR-2026-016 AC-99", "T999", "CRS-M1-99999"):
        candidate = copy.deepcopy(PACKAGE)
        candidate["toolRequirements"][0]["traceability"] = [reference]
        assert errors(candidate), reference
    candidate = copy.deepcopy(PACKAGE)
    protocol = next(item for item in candidate["toolRequirements"] if item["id"] == "TR-TRANSFER-RECONSTRUCTION")
    protocol["protocolRequirementIds"] = []
    assert any("lacks protocol evidence" in item for item in errors(candidate))


def test_module_contracts_close_requirements_records_interfaces_and_dependencies(monkeypatch, tmp_path, capsys):
    modules = {item["id"]: item for item in PACKAGE["moduleContracts"]}
    tools = {item["id"]: item for item in PACKAGE["toolRequirements"]}
    records = {item["id"]: item for item in PACKAGE["recordContracts"]}
    assert set(modules) == {"MOD-CAPTURE", "MOD-REASSEMBLY", "MOD-TRANSFER", "MOD-OWNERSHIP", "MOD-OBSERVATION"}
    for module_id, module in modules.items():
        assert set(module["toolRequirementIds"]) == {tool_id for tool_id, tool in tools.items() if tool["ownerModuleId"] == module_id}
        assert all(records[record_id]["ownerModuleId"] == module_id for record_id in module["outputRecordIds"])
        assert module["steps"] and module["failureOutcomes"] and module["invariants"] and module["invariantsZh"]

    mutations = []
    for field, value in (
        ("inputRecordIds", ["MISSING-RECORD"]),
        ("toolRequirementIds", ["MISSING-TOOL"]),
        ("interfaceIds", ["MISSING-INTERFACE"]),
        ("acceptanceCaseIds", ["MISSING-CASE"]),
        ("runtimeParameterIds", ["MISSING-PARAMETER"]),
        ("upstreamModuleIds", ["MOD-CAPTURE"]),
    ):
        candidate = copy.deepcopy(PACKAGE)
        candidate["moduleContracts"][0][field] = value
        mutations.append(candidate)
    blank = copy.deepcopy(PACKAGE)
    blank["moduleContracts"][0]["responsibility"] = "   "
    mutations.append(blank)
    repeated_step = copy.deepcopy(PACKAGE)
    repeated_step["moduleContracts"][0]["steps"][1]["id"] = repeated_step["moduleContracts"][0]["steps"][0]["id"]
    mutations.append(repeated_step)
    repeated_outcome = copy.deepcopy(PACKAGE)
    repeated_outcome["moduleContracts"][0]["failureOutcomes"].append(copy.deepcopy(repeated_outcome["moduleContracts"][0]["failureOutcomes"][0]))
    mutations.append(repeated_outcome)
    wrong_output_owner = copy.deepcopy(PACKAGE)
    wrong_output_owner["moduleContracts"][0]["outputRecordIds"] = ["DATAGRAM-RECORD"]
    mutations.append(wrong_output_owner)
    missing_owned_input = copy.deepcopy(PACKAGE)
    missing_owned_input["moduleContracts"][0]["inputRecordIds"] = ["INTAKE-METADATA"]
    mutations.append(missing_owned_input)
    missing_owned_tool = copy.deepcopy(PACKAGE)
    missing_owned_tool["moduleContracts"][0]["toolRequirementIds"] = ["TR-DATAGRAM-REASSEMBLY"]
    mutations.append(missing_owned_tool)
    cycle = copy.deepcopy(PACKAGE)
    cycle["moduleContracts"][0]["upstreamModuleIds"] = ["MOD-OBSERVATION"]
    mutations.append(cycle)
    unknown_property = copy.deepcopy(PACKAGE)
    unknown_property["moduleContracts"][0]["unexpected"] = True
    mutations.append(unknown_property)
    for candidate in mutations:
        assert errors(candidate)

    reassembly = modules["MOD-REASSEMBLY"]
    assert reassembly["outputValueMappings"] == [{
        "recordId": "DATAGRAM-RECORD",
        "field": "reassemblyStatus",
        "emittedValues": ["COMPLETE", "GAPPED", "CONFLICT"],
        "meaning": "A coverage gap maps to GAPPED; INCOMPLETE-DATAGRAM is a failure code, not a record-field value.",
        "meaningZh": "覆盖缺口映射为 GAPPED；INCOMPLETE-DATAGRAM 是失败码，不是记录字段值。",
    }]
    datagram = copy.deepcopy(records["DATAGRAM-RECORD"])
    datagram["example"]["reassemblyStatus"] = "GAPPED"
    assert MODULE.validate_record_instance(datagram, datagram["example"]) == []
    datagram["example"]["reassemblyStatus"] = "INCOMPLETE"
    assert any(code == "RC-DATAGRAM-STATUS" for code, _, _ in MODULE.validate_record_instance(datagram, datagram["example"]))
    invalid_mapping = copy.deepcopy(PACKAGE)
    next(item for item in invalid_mapping["moduleContracts"] if item["id"] == "MOD-REASSEMBLY")["outputValueMappings"][0]["emittedValues"] = ["INCOMPLETE"]
    assert any("emits invalid DATAGRAM-RECORD.reassemblyStatus" in item for item in errors(invalid_mapping))
    code, captured = run_main(monkeypatch, tmp_path, capsys, invalid_mapping)
    assert code == 1 and "emits invalid DATAGRAM-RECORD.reassemblyStatus" in captured.err

    missing_producer = copy.deepcopy(PACKAGE)
    next(item for item in missing_producer["moduleContracts"] if item["id"] == "MOD-REASSEMBLY")["upstreamModuleIds"] = []
    assert any("MOD-REASSEMBLY input PACKET-REF lacks producer dependency on MOD-CAPTURE" in item for item in errors(missing_producer))
    code, captured = run_main(monkeypatch, tmp_path, capsys, missing_producer)
    assert code == 1 and "MOD-REASSEMBLY input PACKET-REF lacks producer dependency on MOD-CAPTURE" in captured.err
    reversed_dependency = copy.deepcopy(missing_producer)
    next(item for item in reversed_dependency["moduleContracts"] if item["id"] == "MOD-CAPTURE")["upstreamModuleIds"] = ["MOD-REASSEMBLY"]
    assert any("MOD-REASSEMBLY input PACKET-REF lacks producer dependency on MOD-CAPTURE" in item for item in errors(reversed_dependency))

    unrelated_case = copy.deepcopy(PACKAGE)
    unrelated = copy.deepcopy(unrelated_case["acceptanceCases"][0])
    unrelated["id"] = "AC-SYN-UNRELATED"
    unrelated_case["acceptanceCases"].append(unrelated)
    next(item for item in unrelated_case["moduleContracts"] if item["id"] == "MOD-CAPTURE")["acceptanceCaseIds"] = ["AC-SYN-UNRELATED"]
    diagnostic = "MOD-CAPTURE omits acceptance case AC-SYN-TRANSFER required by ['TR-CAPTURE-INTAKE']"
    assert diagnostic in errors(unrelated_case)
    code, captured = run_main(monkeypatch, tmp_path, capsys, unrelated_case)
    assert code == 1 and diagnostic in captured.err

    legal_extra_case = copy.deepcopy(PACKAGE)
    extra = copy.deepcopy(legal_extra_case["acceptanceCases"][0])
    extra["id"] = "AC-SYN-EXTRA"
    legal_extra_case["acceptanceCases"].append(extra)
    next(item for item in legal_extra_case["moduleContracts"] if item["id"] == "MOD-CAPTURE")["acceptanceCaseIds"].append("AC-SYN-EXTRA")
    assert errors(legal_extra_case) == []
    legal_extra_dependency = copy.deepcopy(PACKAGE)
    next(item for item in legal_extra_dependency["moduleContracts"] if item["id"] == "MOD-OBSERVATION")["upstreamModuleIds"].append("MOD-CAPTURE")
    assert errors(legal_extra_dependency) == []
    reordered = copy.deepcopy(PACKAGE)
    reordered["moduleContracts"] = list(reversed(reordered["moduleContracts"]))
    assert errors(reordered) == []


def test_module_contracts_are_fully_rendered_in_both_languages():
    view = SYNC.render(copy.deepcopy(PACKAGE))
    english = view.split("# 中文版", 1)[0]
    chinese = view.split("# 中文版", 1)[1]
    for module in PACKAGE["moduleContracts"]:
        assert module["title"] in english and module["responsibility"] in english
        assert module["titleZh"] in chinese and module["responsibilityZh"] in chinese
        for step in module["steps"]:
            assert step["action"] in english and step["actionZh"] in chinese
        for outcome in module["failureOutcomes"]:
            assert outcome["condition"] in english and outcome["result"] in english
            assert outcome["conditionZh"] in chinese and outcome["resultZh"] in chinese
        for mapping in module["outputValueMappings"]:
            assert mapping["meaning"] in english and mapping["meaningZh"] in chinese
    assert "every cross-module input producer" in english
    assert "每个跨模块输入的生产者" in chinese
    changed = copy.deepcopy(PACKAGE)
    changed["moduleContracts"][0]["steps"][0]["action"] = "Changed executable module step."
    assert SYNC.render(changed) != view


def test_record_contract_examples_and_history_handle_are_enforced():
    assert errors(copy.deepcopy(PACKAGE)) == []
    candidate = copy.deepcopy(PACKAGE)
    candidate["recordContracts"][0]["invalidExample"] = copy.deepcopy(candidate["recordContracts"][0]["example"])
    assert any("invalid example" in item for item in errors(candidate))
    candidate = copy.deepcopy(PACKAGE)
    candidate["recordContracts"][0]["example"].pop("captureId")
    assert any("example is invalid" in item for item in errors(candidate))
    history = next(item for item in PACKAGE["recordContracts"] if item["id"] == "HISTORY-HANDLE")
    assert history["fields"] == ["H", "compatibleStateByHypothesis", "statusByHypothesis", "version"]
    candidate = copy.deepcopy(PACKAGE)
    next(item for item in candidate["recordContracts"] if item["id"] == "HISTORY-HANDLE")["fields"][0] = "hypotheses"
    assert any("interface HistoryHandle" in item for item in errors(candidate))


def test_all_record_examples_are_typed_and_invalid_diagnostics_are_bound():
    for record in PACKAGE["recordContracts"]:
        assert MODULE.validate_record_instance(record, record["example"]) == [], record["id"]
        violations = MODULE.validate_record_instance(record, record["invalidExample"])
        expected = record["invalidExpected"]
        assert any(code == expected["constraintId"] and list(path) == expected["path"] for code, path, _ in violations), record["id"]
        assert not any(isinstance(value, str) and value.startswith("example-") for value in record["example"].values())
        rendered = SYNC.render(copy.deepcopy(PACKAGE))
        assert json.dumps(record["invalidExpected"], ensure_ascii=False, sort_keys=True) in rendered

    candidate = copy.deepcopy(PACKAGE)
    capture = candidate["recordContracts"][0]
    capture["invalidExpected"] = {"constraintId": "RC-CAPTURE-BYTE-SIZE", "path": ["byteSize"]}
    assert any("does not match invalidExpected" in item for item in errors(candidate))


def test_record_definition_language_is_closed_and_executable():
    mutations = [
        ({"type": "banana", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True}, "unsupported type"),
        ({}, "nonempty object"),
        ({"type": "integer", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": "yes"}, "required must be boolean"),
        ({"type": "integer", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "mysteryLimit": 4}, "unsupported keywords"),
        ({"type": "string", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "minLength": -1}, "non-negative integer"),
        ({"type": "integer", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "minimum": "0"}, "must be a number"),
        ({"type": ["integer"], "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True}, "unsupported type"),
        ({"type": "banana", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "oneOf": [{"type": "integer", "constraintId": "RC-INNER"}]}, "cannot combine"),
        ({"type": "string", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "pattern": "["}, "valid regular expression"),
        ({"type": "string", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "pattern": "a{4294967296}"}, "valid regular expression"),
        ({"type": "array", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "minItems": -1, "maxItems": "x", "uniqueItems": "yes", "items": True}, "items must be"),
        ({"type": "object", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "properties": [], "requiredProperties": "x", "additionalProperties": "yes"}, "properties must be"),
        ({"type": "string", "constraintId": "bad", "required": True, "enum": []}, "constraintId"),
        ({"constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True, "oneOf": []}, "oneOf must be"),
    ]
    for definition, diagnostic in mutations:
        candidate = copy.deepcopy(PACKAGE)
        candidate["recordContracts"][0]["fieldDefinitions"]["byteSize"] = definition
        assert any(diagnostic in item for item in errors(candidate)), definition

    candidate = copy.deepcopy(PACKAGE)
    capture = candidate["recordContracts"][0]
    capture["fields"].append("label")
    capture["fieldDefinitions"]["label"] = {"type": "string", "constraintId": "RC-CAPTURE-LABEL", "required": False, "minLength": 1}
    capture["example"]["label"] = "synthetic"
    assert errors(candidate) == []

    candidate = copy.deepcopy(PACKAGE)
    capture = candidate["recordContracts"][0]
    capture["fields"].append("meta")
    capture["fieldDefinitions"]["meta"] = {"type": "object", "constraintId": "RC-CAPTURE-META", "required": False, "properties": {"byteSize": {"type": "integer", "constraintId": "RC-CAPTURE-META-BYTE-SIZE", "required": True}}, "additionalProperties": False}
    assert any("nested required is unsupported" in item for item in errors(candidate))


def test_nested_diagnostics_resolve_full_paths_and_declared_constraints():
    packet = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "PACKET-REF"))
    packet["example"]["resolution"] = {}
    assert ("RC-PACKET-TICKS-PER-SECOND", ("resolution", "ticksPerSecond")) == MODULE.validate_record_instance(packet, packet["example"])[0][:2]

    candidate = copy.deepcopy(PACKAGE)
    capture = candidate["recordContracts"][0]
    capture["fields"].append("meta")
    capture["fieldDefinitions"]["meta"] = {"type": "object", "constraintId": "RC-CAPTURE-META", "required": True, "properties": {"byteSize": {"type": "integer", "constraintId": "RC-CAPTURE-META-BYTE-SIZE"}}, "requiredProperties": ["byteSize"], "additionalProperties": False}
    capture["example"]["meta"] = {"byteSize": 1}
    capture["invalidExample"] = copy.deepcopy(capture["example"])
    capture["invalidExample"]["meta"] = {}
    capture["invalidExpected"] = {"constraintId": "RC-CAPTURE-META-BYTE-SIZE", "path": ["meta", "byteSize"]}
    assert errors(candidate) == []
    capture["invalidExpected"] = {"constraintId": "RC-CAPTURE-BYTE-SIZE", "path": ["byteSize"]}
    assert any("invalidExpected" in item for item in errors(candidate))

    protocol = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "PROTOCOL-EVENT"))
    protocol["example"]["payload"]["extra"] = True
    assert ("RC-UNKNOWN-FIELD", ("payload", "extra")) == MODULE.validate_record_instance(protocol, protocol["example"])[0][:2]
    datagram = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "DATAGRAM-RECORD"))
    datagram["example"]["fragmentRefs"] = ["bad-ref"]
    assert ("RC-PACKET-REF-ID", ("fragmentRefs", 0)) == MODULE.validate_record_instance(datagram, datagram["example"])[0][:2]

    datagram["example"]["coverage"] = [{}]
    missing = {(code, path) for code, path, _ in MODULE.validate_record_instance(datagram, datagram["example"])}
    assert ("RC-DATAGRAM-RANGE-START", ("coverage", 0, "start")) in missing
    assert ("RC-DATAGRAM-RANGE-END", ("coverage", 0, "endExclusive")) in missing
    for constraint_id, path in (
        ("RC-DATAGRAM-RANGE-START", ["coverage", 0, "start"]),
        ("RC-DATAGRAM-RANGE-END", ["coverage", 0, "endExclusive"]),
    ):
        candidate = copy.deepcopy(PACKAGE)
        target = next(item for item in candidate["recordContracts"] if item["id"] == "DATAGRAM-RECORD")
        target["invalidExample"] = copy.deepcopy(target["example"])
        target["invalidExample"]["coverage"] = [{}]
        target["invalidExpected"] = {"constraintId": constraint_id, "path": path}
        assert errors(candidate) == []

    candidate = copy.deepcopy(PACKAGE)
    transfer = next(item for item in candidate["recordContracts"] if item["id"] == "TRANSFER-RECORD")
    transfer["invalidExample"] = copy.deepcopy(transfer["example"])
    transfer["invalidExample"]["blockMap"] = {"1": "bad-ref"}
    transfer["invalidExpected"] = {"constraintId": "RC-PACKET-REF-ID", "path": ["blockMap", "1"]}
    assert errors(candidate) == []

    candidate = copy.deepcopy(PACKAGE)
    history = next(item for item in candidate["recordContracts"] if item["id"] == "HISTORY-HANDLE")
    history["invalidExample"] = {"H": ["h0.a"], "compatibleStateByHypothesis": {"h0.a": "frontier-syn-0"}, "statusByHypothesis": {"h0.a": "BANANA"}, "version": 0}
    history["invalidExpected"] = {"constraintId": "RC-HISTORY-STATUS-VALUE", "path": ["statusByHypothesis", "h0.a"]}
    assert errors(candidate) == []


def test_oneof_branch_selection_and_leaf_diagnostics_are_order_independent(monkeypatch, tmp_path, capsys):
    branches = [
        {"type": "object", "constraintId": "RC-META-A", "properties": {"a": {"type": "integer", "constraintId": "RC-META-A-VALUE"}}, "requiredProperties": ["a"], "additionalProperties": False},
        {"type": "object", "constraintId": "RC-META-B", "properties": {"b": {"type": "integer", "constraintId": "RC-META-B-VALUE"}}, "requiredProperties": ["b"], "additionalProperties": False},
    ]
    for ordered in (branches, list(reversed(branches))):
        for value in ({"a": 1}, {"b": 1}):
            candidate = copy.deepcopy(PACKAGE)
            capture = candidate["recordContracts"][0]
            capture["fields"].append("meta")
            capture["fieldDefinitions"]["meta"] = {"constraintId": "RC-META", "required": False, "oneOf": copy.deepcopy(ordered)}
            capture["example"]["meta"] = value
            assert MODULE.validate_record_instance(capture, capture["example"]) == []
            assert errors(candidate) == []
            code, captured = run_main(monkeypatch, tmp_path, capsys, candidate)
            assert code == 0
            assert "readiness=CANDIDATE" in captured.out

    record = copy.deepcopy(PACKAGE["recordContracts"][0])
    record["fields"].append("meta")
    record["fieldDefinitions"]["meta"] = {"constraintId": "RC-META", "required": False, "oneOf": copy.deepcopy(branches)}
    record["example"]["meta"] = {"c": 1}
    assert MODULE.validate_record_instance(record, record["example"])
    candidate = copy.deepcopy(PACKAGE)
    candidate["recordContracts"][0] = copy.deepcopy(record)
    code, captured = run_main(monkeypatch, tmp_path, capsys, candidate)
    assert code == 1
    assert "example is invalid" in captured.err
    record["fieldDefinitions"]["meta"] = {"constraintId": "RC-META", "required": False, "oneOf": [
        {"type": "object", "constraintId": "RC-META-OPEN-A", "properties": {}, "additionalProperties": False},
        {"type": "object", "constraintId": "RC-META-OPEN-B", "properties": {}, "additionalProperties": False},
    ]}
    record["example"]["meta"] = {}
    assert MODULE.validate_record_instance(record, record["example"])
    candidate["recordContracts"][0] = copy.deepcopy(record)
    code, captured = run_main(monkeypatch, tmp_path, capsys, candidate)
    assert code == 1
    assert "example is invalid" in captured.err

    for missing_fields in (("lower",), ("upper",), ("lower", "upper")):
        for expected_field, constraint_id in (("lower", "RC-OBS-LOWER"), ("upper", "RC-OBS-UPPER")):
            if expected_field not in missing_fields:
                continue
            candidate = copy.deepcopy(PACKAGE)
            observation = next(item for item in candidate["recordContracts"] if item["id"] == "OBSERVATION-ASSESSMENT")
            observation["invalidExample"] = copy.deepcopy(observation["example"])
            for field in missing_fields:
                observation["invalidExample"]["measurementInterval"].pop(field)
            observation["invalidExpected"] = {"constraintId": constraint_id, "path": ["measurementInterval", expected_field]}
            assert errors(candidate) == []
            wrong = copy.deepcopy(candidate)
            target = next(item for item in wrong["recordContracts"] if item["id"] == "OBSERVATION-ASSESSMENT")
            target["invalidExpected"]["constraintId"] = "RC-OBS-UPPER" if expected_field == "lower" else "RC-OBS-LOWER"
            assert any("invalidExpected" in item for item in errors(wrong))


def test_nested_oneof_uses_complete_schema_semantics_at_every_depth(monkeypatch, tmp_path, capsys):
    def branch(name):
        return {
            "type": "object",
            "constraintId": f"RC-META-{name.upper()}",
            "properties": {name: {"type": "integer", "constraintId": f"RC-META-{name.upper()}-VALUE"}},
            "requiredProperties": [name],
            "additionalProperties": False,
        }

    a, b = branch("a"), branch("b")
    null = {"type": "null", "constraintId": "RC-META-NULL"}

    def assert_schema_and_production_agree(candidate, value):
        record = candidate["recordContracts"][0]
        definition = record["fieldDefinitions"]["meta"]
        schema_accepts = MODULE.Draft202012Validator(MODULE._json_schema(definition)).is_valid(value)
        production_accepts = not MODULE.validate_record_instance(record, record["example"])
        assert production_accepts == schema_accepts

    for outer_order in ("direct-first", "nested-first"):
        for inner in ([b, null], [null, b]):
            nested = {"constraintId": "RC-META-NESTED", "oneOf": copy.deepcopy(inner)}
            outer = [a, nested] if outer_order == "direct-first" else [nested, a]
            for value in ({"a": 1}, {"b": 1}, None):
                candidate = copy.deepcopy(PACKAGE)
                capture = candidate["recordContracts"][0]
                capture["fields"].append("meta")
                capture["fieldDefinitions"]["meta"] = {"constraintId": "RC-META", "required": False, "oneOf": copy.deepcopy(outer)}
                capture["example"]["meta"] = value
                assert_schema_and_production_agree(candidate, value)
                assert MODULE.validate_record_instance(capture, capture["example"]) == []
                assert errors(candidate) == []
                code, captured = run_main(monkeypatch, tmp_path, capsys, candidate)
                assert code == 0
                assert "readiness=CANDIDATE" in captured.out

    wrapped = copy.deepcopy(PACKAGE)
    capture = wrapped["recordContracts"][0]
    capture["fields"].append("meta")
    capture["fieldDefinitions"]["meta"] = {
        "constraintId": "RC-META",
        "required": False,
        "oneOf": [a, {"constraintId": "RC-META-WRAPPER", "oneOf": [{"constraintId": "RC-META-NESTED", "oneOf": [b, null]}]}],
    }
    capture["example"]["meta"] = {"b": 1}
    assert errors(wrapped) == []

    zero = copy.deepcopy(wrapped)
    zero["recordContracts"][0]["example"]["meta"] = {"c": 1}
    assert_schema_and_production_agree(zero, {"c": 1})
    assert errors(zero)
    code, captured = run_main(monkeypatch, tmp_path, capsys, zero)
    assert code == 1
    assert "example is invalid" in captured.err
    duplicate = copy.deepcopy(wrapped)
    duplicate["recordContracts"][0]["fieldDefinitions"]["meta"]["oneOf"] = [a, copy.deepcopy(a)]
    duplicate["recordContracts"][0]["example"]["meta"] = {"a": 1}
    assert_schema_and_production_agree(duplicate, {"a": 1})
    assert errors(duplicate)
    code, captured = run_main(monkeypatch, tmp_path, capsys, duplicate)
    assert code == 1
    assert "example is invalid" in captured.err

    nested_ambiguous_but_outer_unique = copy.deepcopy(wrapped)
    nested_ambiguous_but_outer_unique["recordContracts"][0]["fieldDefinitions"]["meta"]["oneOf"] = [
        a,
        {"constraintId": "RC-META-NESTED", "oneOf": [copy.deepcopy(a), copy.deepcopy(a)]},
    ]
    nested_ambiguous_but_outer_unique["recordContracts"][0]["example"]["meta"] = {"a": 1}
    assert errors(nested_ambiguous_but_outer_unique) == []

    leaf = copy.deepcopy(PACKAGE)
    capture = leaf["recordContracts"][0]
    capture["fields"].append("meta")
    capture["fieldDefinitions"]["meta"] = {
        "constraintId": "RC-META",
        "required": False,
        "oneOf": [null, {"constraintId": "RC-META-NESTED", "oneOf": [b, {"type": "string", "constraintId": "RC-META-STRING", "minLength": 1}]}],
    }
    capture["example"]["meta"] = None
    capture["invalidExample"] = copy.deepcopy(capture["example"])
    capture["invalidExample"]["meta"] = {}
    capture["invalidExpected"] = {"constraintId": "RC-META-B-VALUE", "path": ["meta", "b"]}
    assert errors(leaf) == []
    wrong_leaf = copy.deepcopy(leaf)
    wrong_leaf["recordContracts"][0]["invalidExpected"]["constraintId"] = "RC-META-A-VALUE"
    assert any("invalidExpected" in item for item in errors(wrong_leaf))


def test_record_vocabularies_match_consumers_and_capture_references_are_generic():
    protocol = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "PROTOCOL-EVENT"))
    for layer in ("WIRE", "PARSE-RESULT", "APPLICATION", "ENVIRONMENT"):
        protocol["example"]["eventLayer"] = layer
        assert MODULE.validate_record_instance(protocol, protocol["example"]) == []
    protocol["example"]["eventLayer"] = "TFTP"
    assert MODULE.validate_record_instance(protocol, protocol["example"])

    ownership = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "OWNERSHIP-RESULT"))
    for policy in ("UNIQUE-KEY", "FIFO", "MOST-RECENT"):
        ownership["example"]["policy"] = policy
        assert MODULE.validate_record_instance(ownership, ownership["example"]) == []
    ownership["example"]["policy"] = "REQUEST-CORRELATION"
    assert MODULE.validate_record_instance(ownership, ownership["example"])

    packet = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "PACKET-REF"))
    packet["example"].update(captureId="cap-syn-002", sectionId=0, interfaceId=1, packetNumber=7)
    assert MODULE.validate_record_instance(packet, packet["example"]) == []

    for record_id, field, value in (
        ("DATAGRAM-RECORD", "fragmentRefs", ["cap-syn-002:0:1:7"]),
        ("TRANSFER-RECORD", "blockMap", {"7": "cap-syn-002:0:1:7"}),
        ("PROTOCOL-EVENT", "rawRefs", ["cap-syn-002:0:1:7"]),
    ):
        record = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == record_id))
        record["example"][field] = value
        assert MODULE.validate_record_instance(record, record["example"]) == []
        record["example"][field] = ["bad-ref"] if isinstance(value, list) else {"7": "bad-ref"}
        assert MODULE.validate_record_instance(record, record["example"])


def test_numeric_hash_enum_collection_and_interval_boundaries_are_enforced():
    cases = (
        ("CAPTURE-IDENTITY", "byteSize", -1),
        ("CAPTURE-IDENTITY", "sha256", "not-a-hash"),
        ("CAPTURE-IDENTITY", "relativePath", "../../outside.pcap"),
        ("PACKET-REF", "rawTicks", -1),
        ("PACKET-REF", "resolution", {"ticksPerSecond": 0}),
        ("PACKET-REF", "caplen", -5),
        ("PACKET-REF", "decodeStatus", "BANANA"),
        ("DATAGRAM-RECORD", "fragmentRefs", []),
        ("OBSERVATION-ASSESSMENT", "measurementInterval", {"lower": 0, "upper": 1, "lowerClosed": True, "upperClosed": True, "unit": "seconds"}),
    )
    for record_id, field, value in cases:
        record = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == record_id))
        record["example"][field] = value
        assert MODULE.validate_record_instance(record, record["example"]), (record_id, field)

    observation = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "OBSERVATION-ASSESSMENT"))
    observation["example"].update(measurementInterval=None, domain="UNKNOWN", verdict="ERROR", reason="invalid timestamp chain")
    assert MODULE.validate_record_instance(observation, observation["example"]) == []
    for verdict in ("PASS", "FAIL"):
        observation["example"]["verdict"] = verdict
        assert MODULE.validate_record_instance(observation, observation["example"])
    observation["example"].update(measurementInterval={"lower": 100, "upper": 100, "lowerClosed": True, "upperClosed": True, "unit": "us"}, verdict="PASS")
    assert MODULE.validate_record_instance(observation, observation["example"]) == []
    observation["example"]["measurementInterval"]["lowerClosed"] = False
    assert MODULE.validate_record_instance(observation, observation["example"])
    packet = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "PACKET-REF"))
    packet["example"].update(caplen=97, origlen=96)
    assert any(code == "RC-PACKET-CAPLEN" for code, _, _ in MODULE.validate_record_instance(packet, packet["example"]))
    observation["example"].update(measurementInterval={"lower": 5, "upper": 4, "lowerClosed": True, "upperClosed": True, "unit": "us"}, domain="MONOTONIC-CAPTURE", verdict="PASS")
    assert any(code == "RC-OBS-INTERVAL" for code, _, _ in MODULE.validate_record_instance(observation, observation["example"]))
    for lower, upper in ((5.0, 4.0), (5, 4.0), (5.0, 4)):
        observation["example"]["measurementInterval"].update(lower=lower, upper=upper)
        assert any(code == "RC-OBS-INTERVAL" for code, _, _ in MODULE.validate_record_instance(observation, observation["example"]))
    for lower, upper in ((4, 5), (4.0, 5.0), (4, 5.0)):
        observation["example"]["measurementInterval"].update(lower=lower, upper=upper)
        assert MODULE.validate_record_instance(observation, observation["example"]) == []
    observation["example"]["measurementInterval"].update(lower=4.5, upper=5)
    assert MODULE.validate_record_instance(observation, observation["example"])
    observation["example"]["measurementInterval"].update(lower=True, upper=5)
    assert MODULE.validate_record_instance(observation, observation["example"])
    intake = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "INTAKE-METADATA"))
    intake["example"]["clockAccuracy"] = {"state": "UNKNOWN", "boundNs": 0, "source": "not supplied"}
    assert MODULE.validate_record_instance(intake, intake["example"])

    datagram = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "DATAGRAM-RECORD"))
    datagram["example"]["coverage"] = [{"start": 0, "endExclusive": 1}]
    assert MODULE.validate_record_instance(datagram, datagram["example"]) == []
    datagram["example"]["coverage"] = [{"start": 100, "endExclusive": 1}]
    assert MODULE.validate_record_instance(datagram, datagram["example"])
    datagram["example"]["coverage"] = []
    assert MODULE.validate_record_instance(datagram, datagram["example"])

    transfer = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "TRANSFER-RECORD"))
    transfer["example"]["optionState"] = {"mode": "DEFAULTED", "values": {"blksize": 512}}
    assert MODULE.validate_record_instance(transfer, transfer["example"]) == []
    for blksize in (256, 1024):
        transfer["example"]["optionState"] = {"mode": "DEFAULTED", "values": {"blksize": blksize}}
        assert any(code == "RC-OPTION-BLKSIZE" for code, _, _ in MODULE.validate_record_instance(transfer, transfer["example"]))
    transfer["example"]["optionState"] = {"mode": "ACCEPTED", "values": {"blksize": 1024}}
    assert MODULE.validate_record_instance(transfer, transfer["example"]) == []
    transfer["example"]["optionState"] = {"mode": "UNKNOWN", "values": {}}
    assert MODULE.validate_record_instance(transfer, transfer["example"]) == []
    transfer["example"]["optionState"] = {"mode": "UNKNOWN", "values": {"blksize": 512}}
    assert MODULE.validate_record_instance(transfer, transfer["example"])
    transfer["example"]["optionState"] = {"mode": "DEFAULTED", "values": {"blksize": "banana"}}
    assert MODULE.validate_record_instance(transfer, transfer["example"])
    transfer["example"]["optionState"] = {"mode": "UNKNOWN", "values": {}}
    transfer["example"]["blockMap"] = {"banana": "cap-syn-001:0:0:1"}
    assert MODULE.validate_record_instance(transfer, transfer["example"])
    authoritative_transfer = next(item for item in PACKAGE["recordContracts"] if item["id"] == "TRANSFER-RECORD")
    assert authoritative_transfer["sourceRequirementIds"] == ["CRS-M1-00646", "CRS-M1-00647"]
    view = SYNC.render(copy.deepcopy(PACKAGE))
    assert "DEFAULTED blksize" in view and "DEFAULTED 的 blksize" in view
    assert "`CRS-M1-00646`, `CRS-M1-00647`" in view


def test_all_manifest_capture_ids_flow_through_the_complete_record_chain():
    manifest = json.loads((ROOT / "configs" / "research" / "cltav_historical_capture_manifest.json").read_text(encoding="utf-8"))
    records = {item["id"]: item for item in PACKAGE["recordContracts"]}
    capture_ids = [item["captureId"] for item in manifest["captures"]]
    assert len(capture_ids) == 23
    for capture_id in capture_ids:
        packet_ref = f"{capture_id}:0:0:1"
        patches = {
            "DATAGRAM-RECORD": {"fragmentRefs": [packet_ref]},
            "TRANSFER-RECORD": {"blockMap": {"1": packet_ref}},
            "PROTOCOL-EVENT": {"rawRefs": [packet_ref]},
            "FINDING-RECORD": {"scope": {**records["FINDING-RECORD"]["example"]["scope"], "captureIds": [capture_id]}},
        }
        for record_id, patch in patches.items():
            record = records[record_id]
            instance = copy.deepcopy(record["example"])
            instance.update(patch)
            assert MODULE.validate_record_instance(record, instance) == [], (record_id, capture_id)


def test_capture_reference_vocabulary_rejects_unsafe_or_malformed_aliases():
    record = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "DATAGRAM-RECORD"))
    absolute_windows_ref = chr(67) + ":/HC-01:0:0:1"
    for bad_ref in ("../HC-01:0:0:1", absolute_windows_ref, "HC-1:0:0:1", "HC-01:0:0:0"):
        instance = copy.deepcopy(record["example"])
        instance["fragmentRefs"] = [bad_ref]
        assert MODULE.validate_record_instance(record, instance)


def test_rr86_finite_kernel_return_semantics_and_witness_are_not_substitutable():
    mutations = []
    for interface_id, result, output in (
        ("IF-HIST-UPDATE", "UNSUPPORTED-SYNTAX", "Stop-Empty"),
        ("IF-EQUIV", "FEASIBLE", "established"),
        ("IF-RESOURCE-STOP", "EMPTY-HISTORY", "Stop-Budget"),
    ):
        bad = copy.deepcopy(PACKAGE)
        row = next(item for item in bad["algorithmRefinements"][0]["finiteKernelContract"]["totalReturnMapping"] if item["interfaceId"] == interface_id and item["internalResult"] == result)
        row.update(reachable=True, output=output)
        row.pop("rejectionReason", None)
        mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["algorithmRefinements"][0]["finiteKernelContract"]["totalReturnMapping"] if item["interfaceId"] == "IF-HIST-UPDATE" and item["internalResult"] == "LIMIT-REACHED")["historyEffect"] = "EMPTY-PROVEN"
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["algorithmRefinements"][0]["finiteKernelContract"]["witnessVectors"] if item["id"] == "FK-W1-FEASIBLE")["input"].pop("transition")
    mutations.append(bad)
    for bad in mutations:
        assert errors(bad)


def test_rr86_acceptance_inputs_matrix_and_scenarios_are_closed():
    mutations = []
    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["acceptanceCases"] if item["id"] == "AC-EXP-CAUSAL")["inputFixture"]["values"]["arm"] = "CL-TAV"
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["acceptanceCases"] if item["id"] == "AC-SYN-RESOURCE-STOP")["inputFixture"]["values"].pop("lastOutcome")
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    next(item for item in bad["acceptanceCases"] if item["id"] == "AC-EXP-SCENE")["inputFixture"]["values"].pop("resetId")
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    bad["acceptanceMatrix"][0]["caseIds"] = ["AC-NOT-REAL"]
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    bad["experimentScenarios"][0]["serviceScope"] = "DOWNLOAD"
    mutations.append(bad)
    for bad in mutations:
        assert errors(bad)


def test_rr86_integrity_obligations_come_from_independent_bound_baseline():
    dependency = PACKAGE["implementationDependencies"][0]
    assert len({row["contractId"] for row in dependency["sourceBindings"]}) == 6
    bad = copy.deepcopy(PACKAGE)
    bad["implementationDependencies"][0]["requirementIds"].pop()
    bad["implementationDependencies"][0]["sourceBindings"].pop()
    assert any("independent obligation baseline" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["implementationDependencies"][0]["sourceBindings"][1] = copy.deepcopy(bad["implementationDependencies"][0]["sourceBindings"][0])
    assert any("exactly cover" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["implementationDependencies"][0]["closureEvidence"] = ["README.md", "project-status.json"]
    assert any("content-bound and relevant" in item for item in errors(bad))


def test_rr87_kernel_uses_canonical_rationals_complete_returns_and_separate_histories():
    bad = copy.deepcopy(PACKAGE)
    witness = next(row for row in bad["algorithmRefinements"][0]["finiteKernelContract"]["witnessVectors"] if row["id"] == "FK-W1-FEASIBLE")
    witness["input"]["guard"]["lower"] = {"numerator": 3, "positiveDenominator": 1}
    assert any("reversed interval" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    witness = next(row for row in bad["algorithmRefinements"][0]["finiteKernelContract"]["witnessVectors"] if row["id"] == "FK-W5-CLOCK")
    witness["expected"]["merge"] = True
    assert any("clock-correlation witness" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    row = next(row for row in bad["algorithmRefinements"][0]["finiteKernelContract"]["totalReturnMapping"] if row["interfaceId"] == "IF-PRED-OBS" and row["internalResult"] == "COMPUTATION-UNKNOWN")
    row["returnContract"]["requiredFields"].remove("historyVersionUsed")
    assert any("return contract is incomplete" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    row = next(row for row in bad["algorithmRefinements"][0]["finiteKernelContract"]["totalReturnMapping"] if row["interfaceId"] == "IF-SELECT-ADMIT" and row["internalResult"] == "LIMIT-REACHED")
    row["returnContract"]["adapter"] = "reject every action"
    assert any("TEST-scoped GAP" in item for item in errors(bad))


def test_rr87_acceptance_relations_reject_semantic_drift():
    mutations = []
    bad = copy.deepcopy(PACKAGE)
    next(x for x in bad["acceptanceCases"] if x["id"] == "AC-SYN-OBSERVATION")["expectedOutputFixture"]["values"]["verdict"] = "PASS"
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    case = next(x for x in bad["acceptanceCases"] if x["id"] == "AC-SYN-HISTORY")
    case["expectedOutputFixture"]["values"]["history"] = copy.deepcopy(case["inputFixture"]["values"]["history"])
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    next(x for x in bad["acceptanceCases"] if x["id"] == "AC-SYN-PREP-RECOVER")["inputFixture"]["values"]["summaryConfirmed"] = False
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    next(x for x in bad["acceptanceCases"] if x["id"] == "AC-EXP-TRUTH")["inputFixture"]["values"]["algorithmVisible"] = True
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    next(x for x in bad["acceptanceCases"] if x["id"] == "AC-SYN-SELECT")["inputFixture"]["values"]["resource"]["remaining"] = 0
    mutations.append(bad)
    bad = copy.deepcopy(PACKAGE)
    bad["experimentScenarios"][0]["dependencyIds"] = ["NO-SUCH-DEPENDENCY"]
    mutations.append(bad)
    for bad in mutations:
        assert errors(bad)


def test_rr87_registered_negative_variants_execute_and_hit_the_named_relation():
    for case in PACKAGE["acceptanceCases"]:
        for variant in case["negativeVariants"]:
            mutated = MODULE._apply_acceptance_variant(case, variant)
            assert variant["expectedRejection"] in MODULE._acceptance_relation_errors(mutated)
    bad = copy.deepcopy(PACKAGE)
    variant = next(x for x in bad["acceptanceCases"] if x["id"] == "AC-SYN-HISTORY")["negativeVariants"][0]
    variant["path"] = ["expectedOutputFixture", "values", "NO-SUCH-FIELD"]
    assert any("does not hit its named relation" in item for item in errors(bad))


def test_rr87_matrix_scenarios_and_integrity_witnesses_are_not_labels_only():
    bad = copy.deepcopy(PACKAGE)
    next(x for x in bad["acceptanceMatrix"] if x["category"] == "corpus identity")["coverageAxes"] = ["armId", "truth", "cost"]
    assert any("category-specific coverage axes" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    bad["experimentScenarios"][1]["scenarioValues"]["eventSequence"] = ["WAIT"]
    assert errors(bad)
    bad = copy.deepcopy(PACKAGE)
    dep = bad["implementationDependencies"][0]
    dep["id"] = "DEP-INTEGRITY-RENAMED"
    removed = "CRS-M1-00109"
    dep["requirementIds"].remove(removed)
    dep["sourceBindings"] = [x for x in dep["sourceBindings"] if x["requirementId"] != removed]
    dep["obligationWitnesses"] = [x for x in dep["obligationWitnesses"] if x["requirementId"] != removed]
    dep["closureEvidence"] = ["README.md", "project-status.json"]
    for row in bad["protocolInputDispositions"]:
        row["dependencyIds"] = ["DEP-INTEGRITY-RENAMED" if x == "DEP-INTEGRITY-RUNTIME" else x for x in row.get("dependencyIds", []) if row["inputRequirementId"] != removed]
    bad["requiredDependencyRelations"][0]["dependencyId"] = "DEP-INTEGRITY-RENAMED"
    bad["requiredDependencyRelations"][0]["requirementIds"].remove(removed)
    assert any("independently bound integrity obligations" in item or "independent obligation baseline" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    witness = next(x for x in bad["implementationDependencies"][0]["obligationWitnesses"] if x["requirementId"] == "CRS-M1-00087")
    witness["inputs"]["crcB"] = "0x9999"
    assert any("same-part-number files" in item for item in errors(bad))


def test_rr87_schema_is_standard_valid_and_invalid_schema_is_fail_closed(monkeypatch, tmp_path):
    schema = json.loads(MODULE.SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(PACKAGE)
    broken = copy.deepcopy(schema)
    broken["properties"]["acceptanceMatrix"]["items"]["required"].append("caseIds")
    path = tmp_path / "broken.schema.json"
    path.write_text(json.dumps(broken), encoding="utf-8")
    monkeypatch.setattr(MODULE, "SCHEMA_PATH", path)
    assert any("schema is invalid" in item for item in errors(copy.deepcopy(PACKAGE)))


def test_history_handle_reuses_bound_status_vocabulary_and_scope():
    history = copy.deepcopy(next(item for item in PACKAGE["recordContracts"] if item["id"] == "HISTORY-HANDLE"))
    initialized = copy.deepcopy(history["example"])
    initialized.pop("statusByHypothesis")
    assert MODULE.validate_record_instance(history, initialized) == []
    for status in ("KNOWN", "CONSERVATIVE-UNKNOWN"):
        instance = copy.deepcopy(initialized)
        instance["statusByHypothesis"] = {"h0": status}
        assert MODULE.validate_record_instance(history, instance) == []
    bad = copy.deepcopy(PACKAGE)
    target = next(item for item in bad["recordContracts"] if item["id"] == "HISTORY-HANDLE")
    target["example"]["statusByHypothesis"] = {"h0": "BANANA"}
    assert any("example is invalid" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    target = next(item for item in bad["recordContracts"] if item["id"] == "HISTORY-HANDLE")
    target["example"]["statusByHypothesis"] = {"h9": "KNOWN"}
    assert any("outside H" in item for item in errors(bad))
    bad = copy.deepcopy(PACKAGE)
    target = next(item for item in bad["recordContracts"] if item["id"] == "HISTORY-HANDLE")
    target["fieldDefinitions"]["statusByHypothesis"]["additionalProperties"]["enum"] = ["KNOWN", "BANANA"]
    assert any("statuses differ" in item for item in errors(bad))
    malformed = copy.deepcopy(history["example"])
    malformed["H"] = [{}]
    assert MODULE.validate_record_instance(history, malformed)


def test_review_view_renders_every_disposition_and_bilingual_authority_fields():
    view = SYNC.render(copy.deepcopy(PACKAGE))
    assert "## All requirement dispositions" in view
    assert "## 全部需求处置" in view
    assert "## Slice membership relations" in view
    assert "## 切片成员关系" in view
    english_inputs = view.split("## Inputs\n", 1)[1].split("## Slices and dependencies", 1)[0]
    chinese_inputs = view.split("## 输入身份\n", 1)[1].split("## 切片与依赖", 1)[0]
    chinese_control = view.split("# CL-TAV 开发就绪评审视图", 1)[1].split("## 输入身份", 1)[0]
    assert f"Control: `{PACKAGE['control']['changeRequest']}`" in view
    assert f"控制：`{PACKAGE['control']['changeRequest']}`" in chinese_control
    for decision in PACKAGE["control"]["decisions"]:
        assert f"`{decision}`" in chinese_control
    for binding in PACKAGE["inputBindings"]:
        assert binding["purpose"] in english_inputs
        assert binding["purposeZh"] not in english_inputs
        assert binding["purposeZh"] in chinese_inputs
        assert binding["purpose"] not in chinese_inputs
    for row in PACKAGE["protocolInputDispositions"]:
        assert row["inputRequirementId"] in view
        assert row["rationale"] in view
        assert row["rationaleZh"] in view
    for slice_ in PACKAGE["implementationSlices"]:
        assert slice_["scope"] in view
        assert slice_["scopeZh"] in view
        for requirement_id in slice_["requirementIds"]:
            assert f"| `{slice_['id']}` | `{requirement_id}` |" in view
    tool = PACKAGE["toolRequirements"][2]
    english_tool = view.split(f"### `{tool['id']}` — {tool['title']}", 1)[1].split("# 中文版", 1)[0]
    assert tool["trigger"] in english_tool
    assert tool["action"] in english_tool
    assert tool["errorUnknown"] in english_tool
    chinese_tool = view.split(f"### `{tool['id']}` — {tool['titleZh']}", 1)[1]
    assert tool["triggerZh"] in chinese_tool
    assert tool["actionZh"] in chinese_tool
    assert tool["errorUnknownZh"] in chinese_tool


def test_review_view_escapes_table_rationales_without_losing_row_structure():
    candidate = copy.deepcopy(PACKAGE)
    row = candidate["protocolInputDispositions"][0]
    row["rationale"] = "English left | right\nnext line"
    row["rationaleZh"] = "中文左侧 | 右侧\n下一行"
    view = SYNC.render(candidate)
    english = view.split("## All requirement dispositions\n", 1)[1].split("# 中文版", 1)[0]
    chinese = view.split("## 全部需求处置\n", 1)[1]
    english_row = next(line for line in english.splitlines() if f"`{row['inputRequirementId']}`" in line)
    chinese_row = next(line for line in chinese.splitlines() if f"`{row['inputRequirementId']}`" in line)
    assert english_row.endswith("English left \\| right<br>next line Dependencies: none |")
    assert chinese_row.endswith("中文左侧 \\| 右侧<br>下一行 依赖：无 |")
    assert sum(char == "|" and (index == 0 or english_row[index - 1] != "\\") for index, char in enumerate(english_row)) == 8
    assert sum(char == "|" and (index == 0 or chinese_row[index - 1] != "\\") for index, char in enumerate(chinese_row)) == 8


def test_review_generator_normalizes_free_text_before_write_check_round_trip(monkeypatch, tmp_path):
    candidate = copy.deepcopy(PACKAGE)
    candidate["inputBindings"][0]["purpose"] = "English purpose\r\n# not a heading"
    candidate["inputBindings"][0]["purposeZh"] = "中文用途\r\n# 不是标题"
    candidate["implementationSlices"][0]["scope"] = "English scope\r\n# not a heading"
    candidate["implementationSlices"][0]["scopeZh"] = "中文范围\r\n# 不是标题"
    view = SYNC.render(candidate)
    assert "English purpose<br># not a heading" in view
    assert "中文用途<br># 不是标题" in view
    assert "English scope<br># not a heading" in view
    assert "中文范围<br># 不是标题" in view
    assert "\n# not a heading" not in view
    assert "\n# 不是标题" not in view

    package = tmp_path / "package.json"
    review = tmp_path / "review.md"
    package.write_text(json.dumps(candidate), encoding="utf-8")
    monkeypatch.setattr(SYNC, "PACKAGE", package)
    monkeypatch.setattr(SYNC, "VIEW", review)
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--write"])
    assert SYNC.main() == 0
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--check"])
    assert SYNC.main() == 0


def test_review_view_detects_nonfirst_disposition_and_slice_relation_changes():
    baseline = SYNC.render(copy.deepcopy(PACKAGE))
    candidate = copy.deepcopy(PACKAGE)
    nonfirst = next(row for row in candidate["protocolInputDispositions"] if not row["firstSliceRequired"])
    nonfirst["rationale"] = "Changed non-first-slice rationale."
    nonfirst["rationaleZh"] = "已变更的非首轮理由。"
    assert SYNC.render(candidate) != baseline

    candidate = copy.deepcopy(PACKAGE)
    first_ids = candidate["implementationSlices"][0]["requirementIds"]
    moved, retained = first_ids[0], first_ids[1]
    candidate["implementationSlices"][0]["requirementIds"].remove(moved)
    candidate["implementationSlices"].append({"id": "SLICE-SECOND", "scope": "legal partition", "scopeZh": "合法分区", "requirementIds": [moved]})
    assert errors(candidate) == []
    partitioned = SYNC.render(candidate)
    candidate["implementationSlices"][0]["requirementIds"].remove(retained)
    candidate["implementationSlices"][0]["requirementIds"].append(moved)
    candidate["implementationSlices"][1]["requirementIds"] = [retained]
    assert errors(candidate) == []
    assert SYNC.render(candidate) != partitioned


def test_review_generator_refuses_invalid_authority_and_detects_stale_view(monkeypatch, tmp_path, capsys):
    package = tmp_path / "package.json"
    view = tmp_path / "review.md"
    package.write_text(json.dumps(PACKAGE), encoding="utf-8")
    view.write_text("preserve this failed-publication marker\n", encoding="utf-8")
    monkeypatch.setattr(SYNC, "PACKAGE", package)
    monkeypatch.setattr(SYNC, "VIEW", view)
    invalid = copy.deepcopy(PACKAGE)
    invalid["protocolInputDispositions"][0].pop("rationaleZh")
    package.write_text(json.dumps(invalid), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--write"])
    assert SYNC.main() == 1
    assert view.read_text(encoding="utf-8") == "preserve this failed-publication marker\n"

    invalid = copy.deepcopy(PACKAGE)
    invalid["recordContracts"][0]["fieldDefinitions"]["byteSize"] = {"type": "banana", "constraintId": "RC-CAPTURE-BYTE-SIZE", "required": True}
    package.write_text(json.dumps(invalid), encoding="utf-8")
    assert SYNC.main() == 1
    assert view.read_text(encoding="utf-8") == "preserve this failed-publication marker\n"

    invalid = copy.deepcopy(PACKAGE)
    invalid["recordContracts"][0]["fieldDefinitions"]["relativePath"]["minLength"] = -1
    package.write_text(json.dumps(invalid), encoding="utf-8")
    assert SYNC.main() == 1
    assert view.read_text(encoding="utf-8") == "preserve this failed-publication marker\n"

    invalid = copy.deepcopy(PACKAGE)
    invalid["recordContracts"][0]["fieldDefinitions"]["sha256"]["pattern"] = "a{4294967296}"
    package.write_text(json.dumps(invalid), encoding="utf-8")
    assert SYNC.main() == 1
    assert view.read_text(encoding="utf-8") == "preserve this failed-publication marker\n"

    invalid_modules = []
    invalid = copy.deepcopy(PACKAGE)
    next(item for item in invalid["moduleContracts"] if item["id"] == "MOD-REASSEMBLY")["outputValueMappings"][0]["emittedValues"] = ["INCOMPLETE"]
    invalid_modules.append(invalid)
    invalid = copy.deepcopy(PACKAGE)
    next(item for item in invalid["moduleContracts"] if item["id"] == "MOD-REASSEMBLY")["upstreamModuleIds"] = []
    invalid_modules.append(invalid)
    invalid = copy.deepcopy(PACKAGE)
    invalid["acceptanceCases"].append({"id": "AC-SYN-UNRELATED", "kind": "SYNTHETIC-NONTRUTH"})
    next(item for item in invalid["moduleContracts"] if item["id"] == "MOD-CAPTURE")["acceptanceCaseIds"] = ["AC-SYN-UNRELATED"]
    invalid_modules.append(invalid)
    for invalid in invalid_modules:
        package.write_text(json.dumps(invalid), encoding="utf-8")
        for mode in ("--write", "--check"):
            monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", mode])
            assert SYNC.main() == 1
            assert view.read_text(encoding="utf-8") == "preserve this failed-publication marker\n"

    a = {"type": "object", "constraintId": "RC-META-A", "properties": {"a": {"type": "integer", "constraintId": "RC-META-A-VALUE"}}, "requiredProperties": ["a"], "additionalProperties": False}
    b = {"type": "object", "constraintId": "RC-META-B", "properties": {"b": {"type": "integer", "constraintId": "RC-META-B-VALUE"}}, "requiredProperties": ["b"], "additionalProperties": False}
    nested = {"constraintId": "RC-META-NESTED", "oneOf": [b, {"type": "null", "constraintId": "RC-META-NULL"}]}
    invalid = copy.deepcopy(PACKAGE)
    capture = invalid["recordContracts"][0]
    capture["fields"].append("meta")
    capture["fieldDefinitions"]["meta"] = {"constraintId": "RC-META", "required": False, "oneOf": [a, nested]}
    capture["example"]["meta"] = {"c": 1}
    package.write_text(json.dumps(invalid), encoding="utf-8")
    for mode in ("--write", "--check"):
        monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", mode])
        assert SYNC.main() == 1
        assert view.read_text(encoding="utf-8") == "preserve this failed-publication marker\n"

    for ordered in ([a, nested], [nested, a]):
        legal = copy.deepcopy(PACKAGE)
        capture = legal["recordContracts"][0]
        capture["fields"].append("meta")
        capture["fieldDefinitions"]["meta"] = {"constraintId": "RC-META", "required": False, "oneOf": copy.deepcopy(ordered)}
        capture["example"]["meta"] = {"b": 1}
        package.write_text(json.dumps(legal), encoding="utf-8")
        monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--write"])
        assert SYNC.main() == 0
        monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--check"])
        assert SYNC.main() == 0

    changed = copy.deepcopy(legal)
    changed["recordContracts"][0]["fieldDefinitions"]["meta"]["oneOf"][0]["oneOf"][0]["properties"]["b"]["minimum"] = 0
    package.write_text(json.dumps(changed), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--check"])
    assert SYNC.main() == 1
    assert "stale" in capsys.readouterr().err

    package.write_text(json.dumps(PACKAGE), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--write"])
    assert SYNC.main() == 0
    changed = copy.deepcopy(PACKAGE)
    changed["moduleContracts"][0]["steps"][0]["action"] = "Changed executable module step."
    package.write_text(json.dumps(changed), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["sync_development_readiness.py", "--check"])
    assert SYNC.main() == 1
    assert "stale" in capsys.readouterr().err
