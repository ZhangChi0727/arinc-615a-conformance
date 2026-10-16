from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_experiment_design import (  # noqa: E402
    REQUIRED_BINDINGS,
    REQUIRED_METRIC_CONTRACTS,
    _population_sets,
    accounting_summary,
    validate_design,
)
from sync_experiment_design import (  # noqa: E402
    END,
    START,
    reconcile_text,
    render_shared_block,
    sync,
)
import check_experiment_design as checker  # noqa: E402
import sync_experiment_design as generator  # noqa: E402


DESIGN = json.loads((ROOT / "configs/research/cltav_experiment_design.json").read_text(encoding="utf-8"))


def errors_for(mutator) -> list[str]:
    candidate = copy.deepcopy(DESIGN)
    mutator(candidate)
    return validate_design(ROOT, candidate)


def _run_git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


@pytest.fixture()
def isolated_snapshot_repo() -> tuple[Path, dict]:
    with tempfile.TemporaryDirectory(prefix="experiment-snapshot-") as directory:
        root = Path(directory)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Experiment test"], cwd=root, check=True)

        base = DESIGN["identity"]["baseCommit"]
        for relative in REQUIRED_BINDINGS:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            blob = subprocess.check_output(["git", "cat-file", "blob", f"{base}:{relative}"], cwd=ROOT)
            target.write_bytes(blob)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "accepted inputs"], cwd=root, check=True)
        commit = _run_git(root, "rev-parse", "HEAD")

        schema_target = root / "configs/research/cltav_experiment_design.schema.json"
        schema_target.parent.mkdir(parents=True, exist_ok=True)
        schema_target.write_bytes((ROOT / "configs/research/cltav_experiment_design.schema.json").read_bytes())

        candidate = copy.deepcopy(DESIGN)
        candidate["identity"]["baseCommit"] = commit
        for binding in candidate["inputBindings"]:
            relative = binding["path"]
            binding["gitBlobOid"] = _run_git(root, "rev-parse", f"{commit}:{relative}")
            binding["sha256"] = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        yield root, candidate


def test_repository_experiment_design_is_valid_and_reordering_is_semantic_noop() -> None:
    assert validate_design(ROOT) == []
    candidate = copy.deepcopy(DESIGN)
    candidate["inputBindings"].reverse()
    candidate["metrics"].reverse()
    candidate["scenarios"].reverse()
    candidate["dependencies"].reverse()
    assert validate_design(ROOT, candidate) == []


def test_v01_binding_roles_oid_and_sha_are_mandatory() -> None:
    assert errors_for(lambda d: d["inputBindings"].pop(0))
    assert errors_for(lambda d: d["inputBindings"][0].pop("role"))
    assert any("OID" in item or "Git blob" in item for item in errors_for(lambda d: d["inputBindings"][0].update(gitBlobOid="0" * 40)))
    assert any("SHA-256 mismatch" in item for item in errors_for(lambda d: d["inputBindings"][0].update(sha256="0" * 64)))


def test_v02_authority_consumers_use_committed_blobs_only(isolated_snapshot_repo: tuple[Path, dict]) -> None:
    root, candidate = isolated_snapshot_repo
    registry_path = root / "configs/research/cltav_interface_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["experimentInterfaces"][0]["outputs"].append("onlyWorktree")
    registry_path.write_text(json.dumps(registry), encoding="utf-8")

    assert validate_design(root, candidate) == []
    candidate["metrics"][0]["requiredFields"].append("IF-EXP-SCENE.onlyWorktree")
    errors = validate_design(root, candidate)
    assert any("unknown interface output" in item for item in errors)


def test_v03_error_and_nonsingleton_fail_are_not_singleton_decisions() -> None:
    populations = _population_sets(DESIGN)
    assert "ATT-007" not in populations["POP-ANSWERED"]
    assert "ATT-002" not in populations["POP-SINGLETON-DECISION"]
    assert "ATT-003" in populations["POP-SINGLETON-DECISION"]
    assert errors_for(lambda d: d["syntheticWalkthroughs"][6].update(localizationDecisionIssued=True))


def test_v04_zero_answer_and_conditional_error_denominators() -> None:
    candidate = copy.deepcopy(DESIGN)
    for row in candidate["syntheticWalkthroughs"]:
        row["outcome"] = "NOT-ANSWERED"
    summary = accounting_summary(candidate)
    assert summary["answeredCoverage"] == "0/13"
    assert summary["conditionalDetectionError"] == "N/A"

    candidate = copy.deepcopy(DESIGN)
    candidate["syntheticWalkthroughs"][0]["outcome"] = "FAIL"
    assert accounting_summary(candidate)["conditionalDetectionError"] == "1/4"


def test_v05_excluded_unresolved_abstain_and_pairing_remain_visible_without_duplication() -> None:
    populations = _population_sets(DESIGN)
    summary = accounting_summary(DESIGN)
    assert len(populations["POP-ATTEMPTS"]) == 13
    assert summary["equivalentFault"] == 1
    assert summary["unresolvedFault"] == 1
    assert summary["abstain"] == 1
    assert populations["POP-PAIRED-ELIGIBLE"] == {
        "PAIR-01::MET-ANSWERED-COVERAGE",
        "PAIR-01::MET-TRUE-RETAINED",
        "PAIR-01::MET-COST-VECTOR",
    }
    assert populations["POP-ROUNDS"] == {"ATT-001"}
    assert any("duplicate synthetic attempt" in item for item in errors_for(lambda d: d["syntheticWalkthroughs"][1].update(attemptId="ATT-001")))


def test_v06_t5_contains_a_real_interval_overlap_and_rejects_endpoint_or_unit_drift() -> None:
    row = next(row for row in DESIGN["syntheticWalkthroughs"] if row["id"] == "SYN-T5-OVERLAP")
    assert row["observationInterval"] == {"lower": 5.0, "upper": 5.2, "unit": "s"}
    assert any("T5 classification" in item for item in errors_for(lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-T5-OVERLAP")["requirementInterval"].update(upper=4.9)))
    assert any("units" in item for item in errors_for(lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-T5-OVERLAP")["observationInterval"].update(unit="ms")))


def test_v07_stop_priority_is_stage_sensitive() -> None:
    assert any("Stop-Empty" in item for item in errors_for(lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-STOP-EMPTY").update(stage="TERMINAL")))

    def forge_budget_singleton(data: dict) -> None:
        row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-PRE-ACTION")
        row.update(finalHypotheses=["h-normal"], localizationDecisionIssued=True, singletonDecisionIssued=True)

    assert any("masquerade" in item for item in errors_for(forge_budget_singleton))


def test_v08_recovery_projects_to_preparation_once() -> None:
    summary = accounting_summary(DESIGN)
    assert summary["projectedCostTotals"]["preparation"] == 3
    assert summary["reviewSetupEffort"] == 3
    assert errors_for(lambda d: d["costAccounting"]["detailToProjection"].update(recovery="retry"))
    assert any("fair-comparison" in item for item in errors_for(lambda d: d["arms"][1]["costComponents"].append("acquisition")))


def test_v09_scenario_and_acceptance_matrix_references_are_exact() -> None:
    assert DESIGN["scenarios"][4]["crsDisposition"] == "TOOL-OR-EXPERIMENT-N/A"
    assert DESIGN["scenarios"][4]["crsRefs"] == []
    assert any("unknown acceptance-case" in item for item in errors_for(lambda d: d["scenarios"][0]["acceptanceCaseRefs"].append("AC-BOGUS")))
    assert any("bound Git development authority" in item for item in errors_for(lambda d: d["scenarios"][7].update(serviceScope="UPLOAD")))
    assert errors_for(lambda d: d["acceptanceMatrixDispositions"].pop())


def test_v10_runtime_equivalence_is_not_mutation_truth() -> None:
    def conflate(data: dict) -> None:
        dep = next(row for row in data["dependencies"] if row["id"] == "DEP-EQUIV")
        dep["proposalFields"][0]["path"] = "IF-EQUIV.mutationTruth"

    assert any("must not redefine runtime IF-EQUIV" in item for item in errors_for(conflate))


def test_v11_typed_truth_visibility_rejects_algorithm_leakage() -> None:
    def leak(data: dict) -> None:
        data["arms"][0]["visibleInputs"].append({"ref": "IF-EXP-TRUTH.truthRecord", "role": "ALGORITHM-INITIAL"})

    assert any("truth leakage" in item for item in errors_for(leak))
    assert all(row["truthReference"]["visibility"] == "EVALUATOR-ONLY" for row in DESIGN["syntheticWalkthroughs"])


def test_v12_coordinated_deletion_cannot_bypass_closure() -> None:
    def delete_decision_everywhere(data: dict) -> None:
        data["pendingDecisions"] = [row for row in data["pendingDecisions"] if row["id"] != "DEC-CLOCK"]
        data["designAdmission"]["blockingDecisionIds"].remove("DEC-CLOCK")
        for dependency in data["dependencies"]:
            dependency["decisionIds"] = [item for item in dependency["decisionIds"] if item != "DEC-CLOCK"]

    def delete_metric_everywhere(data: dict) -> None:
        data["metrics"] = [row for row in data["metrics"] if row["id"] != "MET-ANSWERED-COVERAGE"]
        for family in data["comparisonFamilies"]:
            family["metricIds"] = [item for item in family["metricIds"] if item != "MET-ANSWERED-COVERAGE"]
        for dependency in data["dependencies"]:
            dependency["consumers"] = [item for item in dependency["consumers"] if item != "MET-ANSWERED-COVERAGE"]
        next(row for row in data["metrics"] if row["id"] == "MET-ABLATION-DELTA")["parentMetricIds"].remove("MET-ANSWERED-COVERAGE")

    assert errors_for(delete_decision_everywhere)
    assert any("metric set must remain complete" in item for item in errors_for(delete_metric_everywhere))
    assert any("dependencies must remain complete" in item for item in errors_for(lambda d: d["dependencies"].pop(0)))


def test_v13_invalid_nested_schema_returns_stable_diagnostics_not_exception() -> None:
    errors = errors_for(lambda d: d["syntheticWalkthroughs"][0].update(chargedCost="not-an-object"))
    assert errors
    assert all(item.startswith("schema ") for item in errors)


def test_v14_generated_bilingual_tables_reject_drift_but_ignore_order_and_line_endings(
    isolated_snapshot_repo: tuple[Path, dict],
) -> None:
    reordered = copy.deepcopy(DESIGN)
    for key in ("scenarios", "acceptanceMatrixDispositions", "metrics", "analysisPlans", "dependencies", "pendingDecisions"):
        reordered[key].reverse()
    assert render_shared_block(reordered) == render_shared_block(DESIGN)

    source = f"head\r\n{START}\r\nstale\r\n{END}\r\ntail\r\n"
    reconciled = reconcile_text(source, render_shared_block(DESIGN))
    assert "stale" not in reconciled
    assert "\r" not in reconciled

    root, candidate = isolated_snapshot_repo
    design_path = root / "configs/research/cltav_experiment_design.json"
    design_path.write_text(json.dumps(candidate), encoding="utf-8")
    spec_path = root / "docs/research/EXPERIMENT_IMPLEMENTATION_SPEC.md"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(f"before\n{START}\nstale\n{END}\nafter\n", encoding="utf-8")
    before = spec_path.read_bytes()
    candidate["inputBindings"][0]["sha256"] = "0" * 64
    design_path.write_text(json.dumps(candidate), encoding="utf-8")
    ok, message = sync(root, write=True)
    assert not ok and "validation failed" in message
    assert spec_path.read_bytes() == before


def test_v15_primary_metrics_have_analysis_decision_and_freeze_gates() -> None:
    primary = [row for row in DESIGN["metrics"] if row["primary"]]
    assert primary
    assert all(row["analysisPlanId"] for row in primary)
    analysis = {row["id"]: row for row in DESIGN["analysisPlans"]}
    assert all(analysis[row["analysisPlanId"]]["freezeDecisionId"] == "DEC-SAMPLE" for row in primary)
    assert any("valid analysis plan" in item for item in errors_for(lambda d: next(row for row in d["metrics"] if row["primary"]).__setitem__("analysisPlanId", "AN-BOGUS")))


def test_repository_spec_is_synchronized() -> None:
    ok, message = sync(ROOT, write=False)
    assert ok, message


def test_w01_error_preserves_history_and_empty_update_is_distinct() -> None:
    assert any("preserve" in item for item in errors_for(lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-INVALID-OBS").update(finalHypotheses=[])))
    empty = next(row for row in DESIGN["syntheticWalkthroughs"] if row["id"] == "SYN-STOP-EMPTY")
    assert empty["compatibleState"] == empty["finalHypotheses"] == []


def test_w02_closed_t5_containment_disjoint_overlap_and_endpoint() -> None:
    def classify(observation: tuple[float, float], requirement: tuple[float, float], outcome: str) -> list[str]:
        def mutate(data: dict) -> None:
            row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-T5-OVERLAP")
            row["observationInterval"].update(lower=observation[0], upper=observation[1])
            row["requirementInterval"].update(lower=requirement[0], upper=requirement[1])
            row["outcome"] = outcome
        return errors_for(mutate)

    assert classify((5.0, 5.2), (4.0, 6.0), "PASS") == []
    assert classify((6.1, 6.2), (4.0, 6.0), "FAIL") == []
    assert classify((5.0, 5.2), (4.0, 5.1), "INCONCLUSIVE") == []
    assert classify((6.0, 6.0), (4.0, 6.0), "PASS") == []


def test_w03_post_update_singleton_cannot_fall_through() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-STOP-645")
        row["compatibleState"] = row["finalHypotheses"] = ["h645"]
    assert any("Stop-Singleton priority" in item for item in errors_for(mutate))


def test_w04_missing_truth_is_unscorable_not_excluded() -> None:
    candidate = copy.deepcopy(DESIGN)
    row = next(row for row in candidate["syntheticWalkthroughs"] if row["id"] == "SYN-TRUE-EXCLUDED")
    row["truthReference"]["truthHypothesis"] = None
    populations = _population_sets(candidate)
    assert "ATT-003" not in populations["POP-TRUE-EXCLUDED"]
    assert "ATT-003" not in populations["POP-SINGLETON-CORRECT"]


def test_w05_pair_requires_scene_arms_reset_and_parent_eligibility() -> None:
    assert _population_sets(DESIGN)["POP-PAIRED-ELIGIBLE"] == {
        "PAIR-01::MET-ANSWERED-COVERAGE",
        "PAIR-01::MET-TRUE-RETAINED",
        "PAIR-01::MET-COST-VECTOR",
    }
    assert any("pairing eligibility" in item for item in errors_for(lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-PAIR-COMPARATOR").update(baseSceneId="OTHER")))
    assert "PAIR-MISMATCH" not in _population_sets(DESIGN)["POP-PAIRED-ELIGIBLE"]


def test_w06_metric_contract_is_single_source_and_reorder_safe() -> None:
    assert any("finite computation contract" in item for item in errors_for(lambda d: next(row for row in d["metrics"] if row["id"] == "MET-ANSWERED-COVERAGE").update(numeratorPopulationId="POP-ATTEMPTS")))
    candidate = copy.deepcopy(DESIGN)
    candidate["metrics"].reverse()
    assert accounting_summary(candidate) == accounting_summary(DESIGN)


def test_w08_w09_safe_projection_and_fixed_roles() -> None:
    assert all(all(item["ref"] != "IF-EXP-SCENE.sceneRecord" for item in arm["visibleInputs"]) for arm in DESIGN["arms"])
    assert any("unknown" in item or "leakage" in item for item in errors_for(lambda d: d["arms"][0]["visibleInputs"].append({"ref":"truthReference.truthHypothesis","role":"ALGORITHM-INITIAL"})))
    assert any("CL-A" in item for item in errors_for(lambda d: d["arms"][1]["visibleInputs"].append({"ref":"IF-EXP-COLLECT.observationLog","role":"ALGORITHM-OWN-ACTION"})))


def test_w10_current_reference_kind_and_required_edges_are_closed() -> None:
    assert any("unknown currentReference kind" in item for item in errors_for(lambda d: d["dependencies"][0]["currentReference"].update(kind="invented-kind")))
    assert errors_for(lambda d: next(row for row in d["dependencies"] if row["id"] == "DEP-TRUTH").update(consumers=[]))


def test_w11_equivalence_is_one_evaluator_only_proposal() -> None:
    fields = [field for dep in DESIGN["dependencies"] for field in dep["proposalFields"] if field["path"] == "truthRecord.equivalenceDisposition"]
    assert fields and all(field["visibility"] == "evaluator-only" for field in fields)
    assert not any(field["path"] == "truthRecord.mutationEquivalence" for dep in DESIGN["dependencies"] for field in dep["proposalFields"])


def test_w13_single_resource_mode_and_separate_retry_cap() -> None:
    decision = next(row for row in DESIGN["pendingDecisions"] if row["id"] == "DEC-RESOURCE")
    assert len(decision["options"]) == 2
    assert "exactly one" in decision["recommendation"]
    assert "retry cap" in decision["recommendation"]


def test_w14_hypothetical_choice_branches_include_wait() -> None:
    choices = {(row["selectedBranch"], row["result"]) for row in DESIGN["analysisChoiceWalkthroughs"]}
    assert ("DETERMINISTIC-EXHAUSTIVE", "CANDIDATE-METHOD") in choices
    assert ("INDEPENDENT-RANDOMIZED", "CANDIDATE-METHOD") in choices
    assert ("PAIRED-OR-CLUSTERED", "CANDIDATE-METHOD") in choices
    assert ("NONE", "WAIT-DEC-SAMPLE") in choices


def test_q01_error_preservation_cannot_be_bypassed_by_relabeling_stop() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-INVALID-OBS")
        row["stopClass"] = "Stop-645"
        row["finalHypotheses"] = []

    assert any("preserve H" in item for item in errors_for(mutate))


def test_q02_empty_and_singleton_update_priorities_precede_other_stops() -> None:
    assert any(
        "Stop-Empty" in item
        for item in errors_for(
            lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-STOP-EMPTY").update(stopClass="Stop-645")
        )
    )
    assert any(
        "Stop-Singleton" in item
        for item in errors_for(
            lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-NORMAL").update(stopClass="Stop-645")
        )
    )


def test_q03_valid_update_is_history_intersection_not_arbitrary_replacement() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-FAIL-NONSINGLETON")
        row["compatibleState"].append("h-extra")
        row["finalHypotheses"].append("h-extra")

    assert any("subset of H" in item for item in errors_for(mutate))


def test_r01_invalid_observation_cannot_be_relabelled_as_valid_update() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-INVALID-OBS")
        row.update(
            updateStatus="VALID-UPDATE",
            compatibleState=["h-normal"],
            finalHypotheses=["h-normal"],
            stopClass="Stop-Singleton",
        )

    assert any("common interpretation/update-source" in item for item in errors_for(mutate))


def test_r02_non_run_attempt_cannot_be_counted_as_pass() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-UNCONFIRMED")
        row.update(validity="VALID", outcome="PASS")

    assert any("non-run record" in item for item in errors_for(mutate))
    candidate = copy.deepcopy(DESIGN)
    row = next(row for row in candidate["syntheticWalkthroughs"] if row["id"] == "SYN-UNCONFIRMED")
    row.update(validity="VALID", outcome="PASS")
    assert row["attemptId"] not in _population_sets(candidate)["POP-ANSWERED"]


def test_q04_missing_truth_keeps_coverage_but_leaves_truth_scored_denominators() -> None:
    candidate = copy.deepcopy(DESIGN)
    row = next(row for row in candidate["syntheticWalkthroughs"] if row["id"] == "SYN-PAIR-COMPARATOR")
    row["truthReference"]["truthHypothesis"] = None
    row["pairParentMetricIds"].remove("MET-TRUE-RETAINED")
    populations = _population_sets(candidate)
    assert "ATT-013" in populations["POP-ANSWERED"]
    assert "ATT-013" in populations["POP-TRUTH-MISSING"]
    assert "ATT-013" not in populations["POP-ANSWERED-TRUTH-SCORABLE"]
    assert "ATT-013" not in populations["POP-LOCALIZATION-TRUTH-SCORABLE"]


def test_q05_pairing_is_derived_independently_for_each_parent_metric() -> None:
    candidate = copy.deepcopy(DESIGN)
    row = next(row for row in candidate["syntheticWalkthroughs"] if row["id"] == "SYN-PAIR-COMPARATOR")
    row["validity"] = "INVALID"
    row["outcome"] = "ERROR"
    row["localizationDecisionIssued"] = False
    row["pairParentMetricIds"] = ["MET-ANSWERED-COVERAGE", "MET-COST-VECTOR"]
    pairs = _population_sets(candidate)["POP-PAIRED-ELIGIBLE"]
    assert "PAIR-01::MET-COST-VECTOR" in pairs
    assert "PAIR-01::MET-TRUE-RETAINED" not in pairs


def test_q06_pairing_requires_registered_construction_identity_and_confirmed_reset() -> None:
    assert errors_for(
        lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-PAIR-COMPARATOR").update(sceneSeed="OTHER")
    )
    assert errors_for(
        lambda d: next(row for row in d["syntheticWalkthroughs"] if row["id"] == "SYN-PAIR-COMPARATOR").update(resetConfirmed=False)
    )


def test_q07_no_response_timeline_is_source_bound_and_not_generic_suppression() -> None:
    assert any(row["outcome"] == "NOT-SCORED" for row in DESIGN["protocolTimelineWalkthroughs"])
    assert errors_for(
        lambda d: next(row for row in d["protocolTimelineWalkthroughs"] if row["id"] == "TL-MISSING-BOTH").update(outcome="PASS")
    )


def test_r03_exception_timer_endpoint_abort_duty_and_finite_horizon_are_closed() -> None:
    at_expiry = next(row for row in DESIGN["protocolTimelineWalkthroughs"] if row["id"] == "TL-STATUS-AT-EXPIRY")
    missing = next(row for row in DESIGN["protocolTimelineWalkthroughs"] if row["id"] == "TL-MISSING-BOTH")
    assert at_expiry["timerExpiryBoundary"] == "UNRESOLVED"
    assert at_expiry["outcome"] == "NOT-SCORED"
    assert missing["abortObligation"] == "REQUIRED-IF-NO-TIMELY-STATUS"
    assert missing["abortCompletionBoundSeconds"] is None
    assert missing["observationEndSeconds"] >= missing["elapsedSeconds"]
    assert missing["outcome"] == "NOT-SCORED"
    assert errors_for(
        lambda d: next(row for row in d["protocolTimelineWalkthroughs"] if row["id"] == "TL-STATUS-AT-EXPIRY").update(
            timerExpiryBoundary="CLOSED", outcome="PASS"
        )
    )
    assert errors_for(
        lambda d: next(row for row in d["protocolTimelineWalkthroughs"] if row["id"] == "TL-MISSING-BOTH").update(
            abortObligation="NOT-APPLICABLE"
        )
    )
    assert errors_for(
        lambda d: next(row for row in d["protocolTimelineWalkthroughs"] if row["id"] == "TL-MISSING-BOTH").update(
            observationEndSeconds=10, outcome="FAIL"
        )
    )


def test_q08_safe_projection_rejects_nested_truth_member_and_denylist_trimming() -> None:
    def leak(data: dict) -> None:
        dep = next(row for row in data["dependencies"] if row["id"] == "DEP-IUT")
        projection = next(field for field in dep["proposalFields"] if field["path"] == "IF-EXP-SCENE.algorithmVisibleFields")
        projection["members"].append({"name": "truthSource", "type": "reference", "role": "ALGORITHM-INITIAL"})

    assert any("safe projection" in item for item in errors_for(leak))


def test_q09_truth_consumers_decisions_and_pilot_milestone_are_not_trimmable() -> None:
    assert errors_for(lambda d: next(row for row in d["dependencies"] if row["id"] == "DEP-TRUTH")["consumers"].remove("MET-TRUE-EXCLUDED"))
    assert errors_for(lambda d: next(row for row in d["dependencies"] if row["id"] == "DEP-TRUTH").update(blockingMilestone="submission"))


def test_q10_controlled_chinese_and_required_fields_are_rendered() -> None:
    rendered = render_shared_block(DESIGN)
    assert DESIGN["translationsZh"]["scenarios.SC-NO-RESPONSE.summary"] in rendered
    assert "truthReference.truthHypothesis" in rendered
    assert any("missing controlled Chinese" in item for item in errors_for(lambda d: d["translationsZh"].pop("metrics.MET-TRUE-EXCLUDED.summary")))


def test_q11_analysis_branch_is_derived_from_independence_evidence() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["analysisChoiceWalkthroughs"] if row["id"] == "CHOICE-INDEPENDENT")
        row["independentUnit"] = "UNKNOWN"

    assert any("independence/pairing inputs" in item for item in errors_for(mutate))


def test_q12_paired_and_clustered_evidence_are_not_interchangeable() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["analysisChoiceWalkthroughs"] if row["id"] == "CHOICE-PAIRED")
        row["pairingEvidence"] = False
        row["clusterEvidence"] = True

    assert any("independence/pairing inputs" in item for item in errors_for(mutate))


def test_q13_statistical_source_locator_must_resolve_to_bound_lines() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["analysisPlans"] if row["id"] == "AN-PROPORTION")
        row["sourceLocators"][0]["path"] = "docs/research/DOES-NOT-EXIST.md"

    assert any("not a bound path" in item for item in errors_for(mutate))


def test_r04_all_metric_population_and_required_field_contracts_are_closed() -> None:
    assert set(REQUIRED_METRIC_CONTRACTS) == {row["id"] for row in DESIGN["metrics"]}
    assert any(
        "finite computation contract" in item
        for item in errors_for(
            lambda d: next(row for row in d["metrics"] if row["id"] == "MET-MISS")["requiredFields"].remove(
                "truthReference.truthHypothesis"
            )
        )
    )


def test_s01_update_relation_is_common_across_scenarios() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["syntheticWalkthroughs"] if row["id"] == "SYN-INVALID-OBS")
        row.update(
            scenarioId="SC-RESOURCE-ERROR",
            updateStatus="VALID-UPDATE",
            compatibleState=["h-normal"],
            finalHypotheses=["h-normal"],
            stopClass="Stop-Singleton",
        )

    errors = errors_for(mutate)
    assert any("common interpretation/update-source" in item for item in errors)
    assert any("preserve preceding H/history" in item for item in errors)


def test_s02_accepted_empty_update_and_rejected_history_cost_both_remain_valid() -> None:
    empty = next(row for row in DESIGN["syntheticWalkthroughs"] if row["id"] == "SYN-STOP-EMPTY")
    rejected = next(row for row in DESIGN["syntheticWalkthroughs"] if row["id"] == "SYN-INVALID-OBS")
    assert empty["updateStatus"] == "VALID-UPDATE" and empty["finalHypotheses"] == []
    assert empty["stopClass"] == "Stop-Empty"
    assert rejected["finalHypotheses"] == rejected["historyBefore"]
    assert sum(rejected["chargedCost"].values()) > 0
    assert not rejected["localizationDecisionIssued"]
    assert validate_design(ROOT) == []


@pytest.mark.parametrize("bound", [0, 1, 10**9])
def test_s03_unreviewed_abort_completion_bounds_are_rejected(bound: int) -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["protocolTimelineWalkthroughs"] if row["id"] == "TL-MISSING-BOTH")
        row.update(abortCompletionBoundSeconds=bound, outcome="FAIL")

    assert any("unreviewed abort completion bound" in item for item in errors_for(mutate))


def test_s04_abort_branch_cannot_ignore_an_invented_completion_bound() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["protocolTimelineWalkthroughs"] if row["id"] == "TL-ABORT-AFTER-DELAY")
        row.update(abortCompletionBoundSeconds=1, elapsedSeconds=100, observationEndSeconds=100)

    assert any("unreviewed abort completion bound" in item for item in errors_for(mutate))


def test_s04b_timeline_boundary_pairing_generic_and_horizon_matrix() -> None:
    assert next(row for row in DESIGN["protocolTimelineWalkthroughs"] if row["id"] == "TL-STATUS-WITHIN-DELAY")["outcome"] == "PASS"
    assert next(row for row in DESIGN["protocolTimelineWalkthroughs"] if row["id"] == "TL-GENERIC-SUPPRESSION")["outcome"] == "NOT-SCORED"
    assert errors_for(
        lambda d: next(row for row in d["protocolTimelineWalkthroughs"] if row["id"] == "TL-STATUS-WITHIN-DELAY").update(
            elapsedSeconds=11, observationEndSeconds=11, outcome="PASS"
        )
    )
    assert errors_for(
        lambda d: next(row for row in d["protocolTimelineWalkthroughs"] if row["id"] == "TL-STATUS-WITHIN-DELAY")["receivedEvent"].update(
            operationKey="OTHER-OP"
        )
    )
    assert any(
        "finite qualified observation endpoint" in item
        for item in errors_for(
            lambda d: next(row for row in d["protocolTimelineWalkthroughs"] if row["id"] == "TL-STATUS-WITHIN-DELAY").update(
                observationEndSeconds=7
            )
        )
    )


def test_s05_metric_field_handoffs_bind_truth_producer_and_closure() -> None:
    def truth_dependency(data: dict) -> dict:
        return next(row for row in data["dependencies"] if row["id"] == "DEP-TRUTH")

    assert any(
        "separate truth identity" in item
        for item in errors_for(
            lambda d: truth_dependency(d).update(
                proposalFields=[field for field in truth_dependency(d)["proposalFields"] if field["path"] != "truthRecord.confirmationRef"]
            )
        )
    )
    assert any(
        "producer/visibility/compatibility/milestone" in item
        for item in errors_for(
            lambda d: next(field for field in truth_dependency(d)["proposalFields"] if field["path"] == "truthRecord.confirmationRef").update(
                producer="algorithm under evaluation"
            )
        )
    )
    assert any(
        "producer/visibility/compatibility/milestone" in item
        for item in errors_for(
            lambda d: next(field for field in truth_dependency(d)["proposalFields"] if field["path"] == "truthRecord.confirmationRef").update(
                closureMilestone="submission"
            )
        )
    )
    assert any(
        "producer/visibility/compatibility/milestone" in item
        for item in errors_for(
            lambda d: next(field for field in truth_dependency(d)["proposalFields"] if field["path"] == "truthRecord.confirmationRef").update(
                backwardCompatibility="replace existing truth field"
            )
        )
    )


def test_s06_shared_proposal_fields_have_one_cross_dependency_meaning() -> None:
    def mutate(data: dict) -> None:
        dep = next(row for row in data["dependencies"] if row["id"] == "DEP-EQUIV")
        dep["proposalFields"][0]["producer"] = "algorithm under evaluation"

    assert any("inconsistent cross-dependency" in item for item in errors_for(mutate))


def test_s07_field_handoff_changes_are_visible_and_reordering_is_stable() -> None:
    candidate = copy.deepcopy(DESIGN)
    row = next(row for row in candidate["metricFieldContracts"] if row["field"] == "attemptId")
    row["backwardCompatibility"] = "versioned additive registration field"
    assert render_shared_block(candidate) != render_shared_block(DESIGN)
    candidate = copy.deepcopy(DESIGN)
    candidate["metricFieldContracts"].reverse()
    candidate["walkthroughInterpretationContracts"].reverse()
    assert validate_design(ROOT, candidate) == []
    assert render_shared_block(candidate) == render_shared_block(DESIGN)


def test_s08_direct_statistical_source_uses_reviewed_proposition_anchor() -> None:
    def mutate(data: dict) -> None:
        locator = next(row for row in data["analysisPlans"] if row["id"] == "AN-PROPORTION")["sourceLocators"][0]
        locator.update(lineStart=1, lineEnd=2)

    assert any("reviewed proposition anchor" in item for item in errors_for(mutate))


@pytest.mark.parametrize("case", ["update", "timing", "handoff", "requirement-source", "truth-source"])
def test_s09_invalid_candidates_fail_real_entrypoints_without_rewriting_view(case: str, monkeypatch, capsys) -> None:
    candidate = copy.deepcopy(DESIGN)
    if case == "update":
        row = next(row for row in candidate["syntheticWalkthroughs"] if row["id"] == "SYN-INVALID-OBS")
        row.update(scenarioId="SC-RESOURCE-ERROR", updateStatus="VALID-UPDATE", compatibleState=["h-normal"], finalHypotheses=["h-normal"], stopClass="Stop-Singleton")
    elif case == "timing":
        row = next(row for row in candidate["protocolTimelineWalkthroughs"] if row["id"] == "TL-MISSING-BOTH")
        row.update(abortCompletionBoundSeconds=1, outcome="FAIL")
    elif case == "handoff":
        dep = next(row for row in candidate["dependencies"] if row["id"] == "DEP-TRUTH")
        dep["proposalFields"][0]["producer"] = "algorithm under evaluation"
    elif case == "requirement-source":
        row = next(row for row in candidate["metricFieldContracts"] if row["field"] == "requirementInterval")
        row.update(
            sourceKind="DIRECT", sourcePath="OBSERVATION-ASSESSMENT.measurementInterval",
            sourceInputPaths=["OBSERVATION-ASSESSMENT.measurementInterval"], proposalFieldPath=None,
        )
    else:
        row = next(row for row in candidate["metricFieldContracts"] if row["field"] == "truthReference.truthHypothesis")
        row.update(sourceKind="DERIVED", sourcePath="finalHypotheses", sourceInputPaths=["finalHypotheses"], proposalFieldPath=None)

    original_read_json = checker._read_json

    def read_candidate(path: Path):
        if path.resolve() == (ROOT / checker.DESIGN_PATH).resolve():
            return candidate
        return original_read_json(path)

    monkeypatch.setattr(checker, "_read_json", read_candidate)
    monkeypatch.setattr(sys, "argv", ["check_experiment_design.py"])
    spec_path = ROOT / generator.SPEC_PATH
    before = spec_path.read_bytes()
    assert checker.main() != 0
    assert generator.sync(ROOT, write=True)[0] is False
    assert spec_path.read_bytes() == before
    assert "failed" in capsys.readouterr().out.lower()


def test_s10_controlled_chinese_covers_645_clock_and_handoffs() -> None:
    translations = DESIGN["translationsZh"]
    assert all(token in translations["dependencies.DEP-645-RUNTIME.summary"] for token in ["645-1", "CRC", "校验值", "命名", "不建立"])
    assert all(token in translations["pendingDecisions.DEC-CLOCK.summary"] for token in ["端点开闭性", "不得改写", "保持为空"])
    rendered = render_shared_block(DESIGN)
    assert "Metric-field handoff / 指标字段交接" in rendered
    assert "Interpretation/update decision relation / 解释与更新决定关系" in rendered
    assert any(
        "finite computation contract" in item
        for item in errors_for(
            lambda d: next(row for row in d["metrics"] if row["id"] == "MET-TRUE-RETAINED").update(
                populationId="POP-ATTEMPTS"
            )
        )
    )


def test_r6_w01_all_metric_fields_classify_value_provenance_and_reorder_stably() -> None:
    contracts = DESIGN["metricFieldContracts"]
    assert len(contracts) == 23
    assert {row["sourceKind"] for row in contracts} == {"DIRECT", "DERIVED", "PROPOSED"}
    assert all(row["sourceInputPaths"] and row["derivationRule"] for row in contracts)
    candidate = copy.deepcopy(DESIGN)
    candidate["metricFieldContracts"].reverse()
    assert validate_design(ROOT, candidate) == []
    assert render_shared_block(candidate) == render_shared_block(DESIGN)


def test_r6_w02_t5_witness_uses_distinct_observation_and_requirement_sources() -> None:
    contracts = {row["field"]: row for row in DESIGN["metricFieldContracts"]}
    assert contracts["observationInterval"]["sourcePath"] == "OBSERVATION-ASSESSMENT.measurementInterval"
    assert contracts["requirementInterval"]["proposalFieldPath"] == "sceneRecord.requirementInterval"
    assert contracts["observationInterval"]["sourcePath"] not in contracts["requirementInterval"]["sourceInputPaths"]
    witness = next(row for row in DESIGN["syntheticWalkthroughs"] if row["id"] == "SYN-T5-OVERLAP")
    assert witness["observationInterval"] == {"lower": 5.0, "upper": 5.2, "unit": "s"}
    assert witness["requirementInterval"] == {"lower": 4.0, "upper": 5.1, "unit": "s"}
    assert witness["outcome"] == "INCONCLUSIVE"


def test_r6_w03_requirement_interval_cannot_alias_measurement_interval() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["metricFieldContracts"] if row["field"] == "requirementInterval")
        row.update(
            sourceKind="DIRECT", sourcePath="OBSERVATION-ASSESSMENT.measurementInterval",
            sourceInputPaths=["OBSERVATION-ASSESSMENT.measurementInterval"], proposalFieldPath=None,
        )

    assert any("requirementInterval violates its reviewed value-source semantics" in item for item in errors_for(mutate))


@pytest.mark.parametrize("source", ["finalHypotheses", "IF-EXP-RUN.traceRef", "IF-EXP-SCENE.algorithmVisibleFields"])
def test_r6_w04_w05_truth_never_comes_from_candidate_or_algorithm_visible_output(source: str) -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["metricFieldContracts"] if row["field"] == "truthReference.truthHypothesis")
        row.update(sourceKind="DERIVED", sourcePath=source, sourceInputPaths=[source], proposalFieldPath=None)

    assert any("truthReference.truthHypothesis violates its reviewed value-source semantics" in item for item in errors_for(mutate))
    truth = next(row for row in DESIGN["metricFieldContracts"] if row["field"] == "truthReference.truthHypothesis")
    assert truth["producerRole"] == "independent evaluator" and truth["visibility"] == "evaluator-only"


@pytest.mark.parametrize("source", ["IF-EXP-SCENE.unconfirmed", "IF-EXP-EVAL.metricCells"])
def test_r6_w06_attempt_outcome_cannot_come_from_unrelated_or_aggregate_output(source: str) -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["metricFieldContracts"] if row["field"] == "outcome")
        row.update(sourceKind="DERIVED", sourcePath=source, sourceInputPaths=[source])

    assert any("outcome violates its reviewed value-source semantics" in item for item in errors_for(mutate))


def test_r6_w07_pair_identity_and_reset_evidence_are_separate() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["metricFieldContracts"] if row["field"] == "pairingId")
        row["proposalFieldPath"] = "sceneRecord.resetEvidenceRef"

    assert any("pairingId" in item and "resetEvidenceRef" in item for item in errors_for(mutate))
    pair = [row for row in DESIGN["syntheticWalkthroughs"] if row.get("pairingId") == "PAIR-01"]
    assert len(pair) == 2 and len({row["resetEvidenceRef"] for row in pair}) == 2


def test_r6_w08_proposed_value_source_cannot_be_downgraded_to_existing() -> None:
    def mutate(data: dict) -> None:
        row = next(row for row in data["metricFieldContracts"] if row["field"] == "requirementInterval")
        row.update(sourceKind="DIRECT", proposalFieldPath=None)

    errors = errors_for(mutate)
    assert any("requirementInterval" in item and "value-source semantics" in item for item in errors)


def test_r6_w10_legal_source_rule_change_round_trips_after_stale_detection(
    isolated_snapshot_repo: tuple[Path, dict],
) -> None:
    root, candidate = isolated_snapshot_repo
    design_path = root / checker.DESIGN_PATH
    spec_path = root / generator.SPEC_PATH
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(
        f"before\n{render_shared_block(candidate)}\nafter\n",
        encoding="utf-8",
    )
    row = next(row for row in candidate["metricFieldContracts"] if row["field"] == "attemptId")
    row["derivationRule"] += "; preserve the registered text form"
    design_path.parent.mkdir(parents=True, exist_ok=True)
    design_path.write_text(json.dumps(candidate), encoding="utf-8")
    assert validate_design(root, candidate) == []
    refreshed = render_shared_block(candidate)
    assert refreshed != render_shared_block(DESIGN)
    assert sync(root, write=False) == (False, "experiment design spec has generated-table drift; run with --write")
    assert sync(root, write=True)[0] is True
    assert sync(root, write=False)[0] is True
