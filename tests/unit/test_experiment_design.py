from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_experiment_design import accounting_summary, validate_design  # noqa: E402


DESIGN = json.loads((ROOT / "configs/research/cltav_experiment_design.json").read_text(encoding="utf-8"))


def errors_for(mutator) -> list[str]:
    candidate = copy.deepcopy(DESIGN)
    mutator(candidate)
    return validate_design(ROOT, candidate)


def test_repository_experiment_design_is_valid() -> None:
    assert validate_design(ROOT) == []


def test_legal_reordering_does_not_change_validity() -> None:
    candidate = copy.deepcopy(DESIGN)
    candidate["metrics"].reverse()
    candidate["scenarios"].reverse()
    assert validate_design(ROOT, candidate) == []


def test_unknown_and_duplicate_references_are_rejected() -> None:
    assert any("unknown experiment family" in item for item in errors_for(lambda d: d["scenarios"][0]["familyIds"].append("EXP-BOGUS")))
    assert any("duplicate metric id" in item for item in errors_for(lambda d: d["metrics"].append(copy.deepcopy(d["metrics"][0]))))


def test_exact_record_and_interface_members_are_checked() -> None:
    assert any("unknown record field" in item for item in errors_for(lambda d: d["metrics"][0]["requiredFields"].append("CAPTURE-IDENTITY.notAField")))
    assert any("unknown interface output" in item for item in errors_for(lambda d: d["metrics"][0]["requiredFields"].append("IF-EXP-EVAL.notAnOutput")))


def test_bound_git_blob_identity_is_not_replaceable_by_worktree_bytes() -> None:
    def mutate(data: dict) -> None:
        data["inputBindings"][0]["sha256"] = "0" * 64
    assert any("SHA-256 mismatch" in item for item in errors_for(mutate))


def test_metric_denominator_and_zero_denominator_contracts_are_enforced() -> None:
    assert any("lacks a denominator" in item for item in errors_for(lambda d: d["metrics"][0].update(denominator="")))
    assert any("empty denominator as N/A" in item for item in errors_for(lambda d: d["metrics"][0].update(zeroDenominator="0%")))


def test_duplicate_attempt_and_non_attempt_walkthrough_are_rejected() -> None:
    assert any("duplicate synthetic attempt" in item for item in errors_for(lambda d: d["syntheticWalkthroughs"][1].update(attemptId="ATT-001")))
    assert any("missing the all-attempt denominator" in item for item in errors_for(lambda d: d["syntheticWalkthroughs"][0]["denominators"].remove("attempt")))


def test_synthetic_or_historical_inputs_cannot_be_promoted() -> None:
    assert any("not explicitly synthetic" in item for item in errors_for(lambda d: d["syntheticWalkthroughs"][0].update(label="OBSERVED-CONFIRMATORY")))
    assert any("historical captures" in item for item in errors_for(lambda d: d["designAdmission"].update(historicalCaptureUse="CONFIRMATORY-TRUTH")))


def test_truth_leakage_and_non_loop_feedback_are_rejected() -> None:
    assert any("truth leakage" in item for item in errors_for(lambda d: d["arms"][0]["visibleInputs"].append("evaluator truth")))
    assert any("non-loop arm" in item for item in errors_for(lambda d: d["arms"][1].update(feedback=True)))
    assert any("CL-A cannot" in item for item in errors_for(lambda d: d["arms"][1]["visibleInputs"].append("adaptive future record")))


def test_pending_runtime_inputs_cannot_be_declared_ready() -> None:
    assert any("cannot mark confirmatory execution ready" in item for item in errors_for(lambda d: d["designAdmission"].update(confirmatoryRunStatus="READY")))
    assert any("cannot be marked complete" in item for item in errors_for(lambda d: d["pendingDecisions"][0].update(status="APPROVED")))


def test_deleting_dependency_or_closure_evidence_does_not_bypass_gate() -> None:
    assert any("unknown dependency" in item for item in errors_for(lambda d: d["dependencies"].pop(0)))
    assert any("lacks closure evidence" in item for item in errors_for(lambda d: d["dependencies"][0].update(closureTest="")))


def test_unconfirmed_and_equivalent_attempts_cannot_gain_runs() -> None:
    assert any("invents a run" in item for item in errors_for(lambda d: d["syntheticWalkthroughs"][3].update(runId="RUN-FORGED")))
    assert any("pre-run equivalent" in item for item in errors_for(lambda d: d["syntheticWalkthroughs"][7].update(runId="RUN-FORGED")))


def test_budget_and_stop_645_retain_spent_cost() -> None:
    def zero_cost(data: dict) -> None:
        data["syntheticWalkthroughs"][9]["chargedCost"] = {key: 0 for key in data["syntheticWalkthroughs"][9]["chargedCost"]}
    assert any("hides spent cost" in item for item in errors_for(zero_cost))


def test_synthetic_accounting_is_attempt_level_and_reproducible() -> None:
    assert accounting_summary(DESIGN) == {
        "attempts": 12,
        "answered": 3,
        "fails": 2,
        "pass": 1,
        "singletonLocalizationDecisions": 1,
        "abstain": 1,
        "unconfirmedInjection": 1,
        "invalidObservation": 1,
        "equivalentFault": 1,
        "emptyAnsweredRate": "3/12",
    }
