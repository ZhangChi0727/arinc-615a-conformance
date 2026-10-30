"""Production-bound tests for the finite runtime evidence/CLI boundary.

The temporary authority repository is intentional: the runtime command must
consume Git objects passed on its command line, rather than fixtures in this
checkout.  The test may construct those inputs, but the production code has no
knowledge of the test directory.
"""

from __future__ import annotations

import copy
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import zipfile

import pytest

from cltav_runtime import cli
from cltav_runtime.evidence import (
    EvidenceError,
    _publish_bytes,
    canonical_json_bytes,
    evidence_document,
    load_evidence_bytes,
    load_sources,
    publish_run,
    run_scenario,
    validate_evidence_document,
)


ROOT = Path(__file__).resolve().parents[2]
DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
INTERFACE_PATH = "configs/research/cltav_interface_registry.json"
SCENARIO_PATH = "configs/runtime/g3-synthetic-scenario.json"
PUBLISHED_SCENARIO_PATH = "configs/examples/cltav_runtime_g3_two_round_scenario.json"
FIXTURE = ROOT / "tests" / "fixtures" / "cltav_runtime" / "two_round_scenarios.json"
EXAMPLE_SCENARIO = ROOT / "configs" / "examples" / "cltav_runtime_g3_two_round_scenario.json"


def _scenario(*, producer_mode: str = "SYNTHETIC-NORMAL", maximum_rounds: int = 2) -> dict[str, object]:
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return {
        "artifactType": "CLTAV-FINITE-SYNTHETIC-SCENARIO",
        "schemaVersion": "1.0",
        "purpose": "SYNTHETIC-ENGINEERING-VALIDATION",
        "scenarioId": "g3-two-round-alpha",
        "model": fixture["algorithmModel"],
        "environment": fixture["environments"]["alpha"],
        "interpretationContract": None,
        "session": {
            "sessionId": "g3-session",
            "runId": "g3-run",
            "initialSummary": "q0",
            "resourceMode": "ROUNDS",
            "resourceRemaining": 2,
            "retryCap": 1,
            "maximumRounds": maximum_rounds,
        },
        "producerMode": producer_mode,
    }


def _published_example_scenario() -> dict[str, object]:
    return json.loads(EXAMPLE_SCENARIO.read_text(encoding="utf-8"))


def _recovery_scenario(
    *, producer_mode: str = "CALCULABLE-IDENTITY-MISMATCH",
) -> dict[str, object]:
    """One real G1 identity error followed by an affordable Recover path."""

    scenario = _scenario(producer_mode=producer_mode, maximum_rounds=2)
    model = copy.deepcopy(scenario["model"])
    environment = copy.deepcopy(scenario["environment"])
    assert isinstance(model, dict) and isinstance(environment, dict)
    actions = model["actions"]
    assert isinstance(actions, list)
    router = copy.deepcopy(next(item for item in actions if item["id"] == "test-router"))
    recover = copy.deepcopy(router)
    assert isinstance(recover, dict)
    recover.update({
        "id": "recover-q1",
        "kind": "RECOVER",
        "declaredTarget": "target-q1",
        "recoverWhenUnknown": True,
        "detailCharges": {
            "acquisition": 0,
            "computation": 0,
            "preparation": 0,
            "recovery": 1,
            "retry": 0,
        },
    })
    transition = recover["transition"]
    assert isinstance(transition, dict)
    transition["id"] = "tr-recover-q1"
    model["actions"] = [router, recover]
    limits = model["limits"]
    assert isinstance(limits, dict)
    limits["actions"] = 2
    states = environment["states"]
    assert isinstance(states, dict)
    for state_id in ("private-a0", "private-a1"):
        private_state = states[state_id]
        assert isinstance(private_state, dict)
        private_state["recover-q1"] = {
            "effectClass": "NONE",
            "observable": None,
            "summaryConfirmed": True,
            "postSummary": "q1",
            "measurementTick": None,
            "nextPrivateState": "private-a2",
            "prepRecover": {
                "targetConfirmed": True,
                "summaryConfirmed": True,
                "prepError": False,
                "ineligible": False,
                "declaredTarget": "target-q1",
                "evidence": "synthetic:g3:recover-q1",
                "postSummary": "q1",
            },
        }
    session = scenario["session"]
    assert isinstance(session, dict)
    session.update({"resourceRemaining": 2, "retryCap": 2, "maximumRounds": 2})
    scenario["model"] = model
    scenario["environment"] = environment
    return scenario


def _timed_observation_scenario() -> dict[str, object]:
    """A Git-bound METHOD-ONLY ownership/timing projection for evidence export."""

    scenario = _scenario(maximum_rounds=1)
    scenario["interpretationContract"] = {
        "contractId": "g3-method-only-timing",
        "triggerEventType": "REQ",
        "responseEventType": "RESP",
        "key": "g3-key",
        "policy": "UNIQUE-KEY",
        "concurrentSameKey": False,
        "cancellationEventType": "CANCEL",
        "supersessionEventType": "SUPERSEDE",
        "physicalDomain": {
            "lower": {"numerator": -10, "positiveDenominator": 1},
            "upper": {"numerator": 10, "positiveDenominator": 1},
            "lowerClosed": True,
            "upperClosed": True,
        },
        "requirementWindow": {
            "lower": {"numerator": 0, "positiveDenominator": 1},
            "upper": {"numerator": 5, "positiveDenominator": 1},
            "lowerClosed": True,
            "upperClosed": True,
        },
        "clockIdentity": "x",
        "uncertaintyIdentity": "synthetic-u-1",
        "errorBudgetIdentity": "MODEL-UNCERTAINTY-DIGEST",
        "unit": "ticks",
        "clockValid": True,
        "errorBudgetValid": True,
        "deadlineAuthority": "METHOD-ONLY",
        "deadlineIdentity": "g3:method-only:deadline:v1",
        "upperBound": 5,
        "upperClosed": True,
    }
    environment = scenario["environment"]
    assert isinstance(environment, dict)
    states = environment["states"]
    assert isinstance(states, dict)
    initial = states["private-a0"]
    assert isinstance(initial, dict)
    action = initial["test-router"]
    assert isinstance(action, dict)
    action["observationMaterial"] = {
        "events": [
            {"id": "req-g3", "sequence": 1, "kind": "REQUEST", "key": "g3-key", "eventType": "REQ", "timestamp": 0},
            {"id": "resp-g3", "sequence": 2, "kind": "RESPONSE", "key": "g3-key", "eventType": "RESP", "timestamp": 0},
        ],
        "triggerEventId": "req-g3",
        "responseId": "resp-g3",
        "measurementInterval": {"lower": 0, "upper": 0, "lowerClosed": True, "upperClosed": True},
        "observationEndQualified": True,
        "earliestElapsed": 6,
        "clockIdentity": "x",
        "unit": "ticks",
    }
    return scenario


def _authority_repo(
    tmp_path: Path,
    *,
    scenario: dict[str, object] | None = None,
    scenario_path: str = SCENARIO_PATH,
) -> tuple[Path, str]:
    repo = tmp_path / "authority"
    (repo / "configs" / "engineering").mkdir(parents=True)
    (repo / "configs" / "research").mkdir(parents=True)
    shutil.copyfile(ROOT / DEVELOPMENT_PATH, repo / DEVELOPMENT_PATH)
    shutil.copyfile(ROOT / INTERFACE_PATH, repo / INTERFACE_PATH)
    target_scenario = repo / scenario_path
    target_scenario.parent.mkdir(parents=True, exist_ok=True)
    target_scenario.write_bytes(canonical_json_bytes(scenario or _scenario()))
    for command in (
        ["git", "init", "-q"],
        ["git", "config", "user.email", "g3@example.invalid"],
        ["git", "config", "user.name", "G3 test"],
        ["git", "add", "configs"],
        ["git", "commit", "-q", "-m", "authority"],
    ):
        subprocess.run(command, cwd=repo, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()
    return repo, commit


def _sources(
    tmp_path: Path,
    *,
    scenario: dict[str, object] | None = None,
    scenario_path: str = SCENARIO_PATH,
):
    repo, commit = _authority_repo(tmp_path, scenario=scenario, scenario_path=scenario_path)
    return load_sources(
        repository=repo,
        commit=commit,
        development_path=DEVELOPMENT_PATH,
        interface_path=INTERFACE_PATH,
        scenario_path=scenario_path,
    )


def _refresh_integrity(document: dict[str, object]) -> None:
    payload = {key: value for key, value in document.items() if key != "integrity"}
    document["integrity"] = {"canonicalPayloadSha256": sha256(canonical_json_bytes(payload)).hexdigest()}


def test_git_bound_two_round_evidence_round_trips_exact_rationals(tmp_path: Path) -> None:
    sources = _sources(tmp_path)
    run = run_scenario(sources)
    document = evidence_document(run)

    assert len(document["rounds"]) == 2
    assert document["rounds"][0]["selection"]["actionId"] == "test-router"
    assert document["rounds"][1]["selection"]["actionId"] == "test-left"
    interval = document["rounds"][0]["selection"]["prediction"]["classes"][0]["measurementWindows"]["h0"]
    assert interval["lower"] == {"numerator": 0, "positiveDenominator": 1}
    assert interval["lowerClosed"] is True
    assert document["inputs"]["scenario"]["path"] == SCENARIO_PATH
    raw = canonical_json_bytes(document)
    decoded = load_evidence_bytes(raw)
    assert validate_evidence_document(decoded, sources=sources) == document


def test_published_example_is_a_closed_git_bound_two_round_scenario(tmp_path: Path) -> None:
    sources = _sources(
        tmp_path,
        scenario=_published_example_scenario(),
        scenario_path=PUBLISHED_SCENARIO_PATH,
    )
    document = evidence_document(run_scenario(sources))

    assert document["run"]["scenarioId"] == "cltav-g3-two-round-example"
    assert [item["selection"]["actionId"] for item in document["rounds"]] == [
        "test-route", "test-follow",
    ]
    assert document["inputs"]["scenario"]["path"] == PUBLISHED_SCENARIO_PATH
    assert [item["chargedOnce"] for item in document["rounds"]] == [True, True]
    assert document["outcome"]["stopReason"] == "Stop-Singleton"
    assert validate_evidence_document(document, sources=sources) == document


def test_git_bound_timing_material_exports_raw_order_ownership_and_assessment(tmp_path: Path) -> None:
    sources = _sources(tmp_path, scenario=_timed_observation_scenario())
    document = evidence_document(run_scenario(sources))

    round_ = document["rounds"][0]
    material = round_["execution"]["observationInput"]
    assert [event["id"] for event in material["events"]] == ["req-g3", "resp-g3"]
    assert material["measurementInterval"] == {
        "lower": {"numerator": 0, "positiveDenominator": 1},
        "upper": {"numerator": 0, "positiveDenominator": 1},
        "lowerClosed": True,
        "upperClosed": True,
    }
    assessment = round_["observationAssessment"]
    assert assessment["ownership"]["ownerRequestId"] == "req-g3"
    assert assessment["replay"]["responseResolutions"]["resp-g3"]["status"] == "UNIQUE"
    assert document["outcome"]["state"]["eventIdentityRefs"]["req-g3"]["kind"] == "REQUEST"
    assert validate_evidence_document(document, sources=sources) == document


def test_evidence_round_trip_preserves_exact_rational_open_closed_timing_bounds(tmp_path: Path) -> None:
    """The public package never widens an exact timing witness to a float."""

    scenario = _timed_observation_scenario()
    contract = scenario["interpretationContract"]
    environment = scenario["environment"]
    assert isinstance(contract, dict) and isinstance(environment, dict)
    contract["physicalDomain"] = {
        "lower": {"numerator": -1, "positiveDenominator": 2},
        "upper": {"numerator": 5, "positiveDenominator": 6},
        "lowerClosed": False,
        "upperClosed": True,
    }
    contract["requirementWindow"] = {
        "lower": {"numerator": 0, "positiveDenominator": 1},
        "upper": {"numerator": 2, "positiveDenominator": 3},
        "lowerClosed": True,
        "upperClosed": False,
    }
    contract["upperBound"] = {"numerator": 2, "positiveDenominator": 3}
    contract["upperClosed"] = False
    model = scenario["model"]
    assert isinstance(model, dict)
    uncertainty = model["uncertainty"]
    assert isinstance(uncertainty, dict)
    uncertainty["maximumErrorTicks"] = {"numerator": 1, "positiveDenominator": 2}
    states = environment["states"]
    assert isinstance(states, dict)
    initial = states["private-a0"]
    assert isinstance(initial, dict)
    action = initial["test-router"]
    assert isinstance(action, dict)
    material = action["observationMaterial"]
    assert isinstance(material, dict)
    material["measurementInterval"] = {
        "lower": {"numerator": -1, "positiveDenominator": 2},
        "upper": {"numerator": 1, "positiveDenominator": 2},
        "lowerClosed": True,
        "upperClosed": True,
    }

    sources = _sources(tmp_path, scenario=scenario)
    document = evidence_document(run_scenario(sources))
    exported = document["rounds"][0]["execution"]["observationInput"]["measurementInterval"]
    assert exported == material["measurementInterval"]
    assessment = document["rounds"][0]["observationAssessment"]
    assert assessment["physicalInterval"] == {
        "lower": {"numerator": -1, "positiveDenominator": 2},
        "upper": {"numerator": 1, "positiveDenominator": 2},
        "lowerClosed": False,
        "upperClosed": True,
    }
    assert assessment["requirementWindow"] == contract["requirementWindow"]
    assert validate_evidence_document(load_evidence_bytes(canonical_json_bytes(document)), sources=sources) == document


def test_synthetic_scenario_cannot_claim_a_reviewed_protocol_deadline(tmp_path: Path) -> None:
    scenario = _timed_observation_scenario()
    contract = scenario["interpretationContract"]
    assert isinstance(contract, dict)
    contract["deadlineAuthority"] = "REVIEWED"
    sources = _sources(tmp_path, scenario=scenario)
    with pytest.raises(EvidenceError) as rejected:
        run_scenario(sources)
    assert rejected.value.code == "SCENARIO-CONTRACT-ERROR"


@pytest.mark.parametrize("mutation", ["delete-raw", "relabel-and-refresh"])
def test_causal_validation_rejects_raw_delete_and_coordinated_relabel(tmp_path: Path, mutation: str) -> None:
    sources = _sources(
        tmp_path,
        scenario=_scenario(producer_mode="CALCULABLE-IDENTITY-MISMATCH", maximum_rounds=1),
    )
    document = evidence_document(run_scenario(sources))
    assert document["rounds"][0]["resolutionCode"] == "EXECUTION-IDENTITY-ERROR"
    assert document["rounds"][0]["rejectedResponse"] is not None
    altered = copy.deepcopy(document)
    if mutation == "delete-raw":
        altered["rounds"][0]["rejectedResponse"] = None
    else:
        # Model the old coordinated-edit weakness: relabel the retained error,
        # rewrite each visible history string, then refresh the self hash.
        altered["rounds"][0]["resolutionCode"] = "EXECUTION-TOOL-ERROR"
        altered["outcome"]["state"]["errorHistory"] = [
            value.replace("EXECUTION-IDENTITY-ERROR", "EXECUTION-TOOL-ERROR")
            for value in altered["outcome"]["state"]["errorHistory"]
        ]
    _refresh_integrity(altered)
    with pytest.raises(EvidenceError) as rejected:
        validate_evidence_document(altered, sources=sources)
    assert rejected.value.code == "EVIDENCE-RELATION-MISMATCH"


def test_qualified_validation_rejects_external_downgrade_and_self_rebound_source(
    tmp_path: Path,
) -> None:
    """A package cannot choose a weaker source class or its own authority."""

    sources = _sources(tmp_path)
    document = evidence_document(run_scenario(sources))

    downgraded = copy.deepcopy(document)
    downgraded["run"]["producerMode"] = "EXTERNAL-OPAQUE-UNVERIFIED"
    downgraded["producerFacts"] = []
    _refresh_integrity(downgraded)
    with pytest.raises(EvidenceError) as downgraded_error:
        validate_evidence_document(downgraded, sources=sources)
    assert downgraded_error.value.code == "EVIDENCE-RELATION-MISMATCH"

    rebound = copy.deepcopy(document)
    rebound["inputs"]["scenario"]["path"] = "configs/runtime/attacker-selected.json"
    _refresh_integrity(rebound)
    with pytest.raises(EvidenceError) as rebound_error:
        validate_evidence_document(rebound, sources=sources)
    assert rebound_error.value.code == "EVIDENCE-SOURCE-MISMATCH"


def test_finite_opaque_driver_uses_real_s4_s7_chain_and_is_rebuilt(tmp_path: Path) -> None:
    sources = _sources(
        tmp_path,
        scenario=_scenario(producer_mode="OPAQUE-INVALID-SUCCESSOR", maximum_rounds=1),
    )
    document = evidence_document(run_scenario(sources))

    assert document["rounds"][0]["resolutionCode"] == "EXECUTION-RESULT-TYPE-ERROR"
    assert document["rounds"][0]["chargedOnce"] is True
    assert document["producerFacts"] == [{
        "producerId": "cltav-runtime-finite-fault-driver",
        "producerProtocol": "CLTAV-FINITE-PRODUCER/1.0",
        "runtimeDistribution": "a615a-sim",
        "runtimeVersion": "0.0.1",
        "runId": "g3-run",
        "sessionId": "g3-session",
        "attemptId": "g3-run:g3-session:execution:1",
        "issuedActionId": "test-router",
        "actionKind": "TEST",
        "stage": "S4-EXECUTE-RETURN",
        "fact": "INVALID-SUCCESSOR-TYPE",
    }]
    assert validate_evidence_document(document, sources=sources) == document


def test_finite_tool_error_uses_the_real_execute_boundary_and_is_rebuilt(tmp_path: Path) -> None:
    sources = _sources(
        tmp_path,
        scenario=_scenario(producer_mode="OPAQUE-TOOL-ERROR", maximum_rounds=1),
    )
    document = evidence_document(run_scenario(sources))

    assert document["rounds"][0]["resolutionCode"] == "EXECUTION-TOOL-ERROR"
    assert document["rounds"][0]["rejectedResponse"] is None
    assert document["rounds"][0]["chargedOnce"] is True
    assert document["producerFacts"] == [{
        "producerId": "cltav-runtime-finite-fault-driver",
        "producerProtocol": "CLTAV-FINITE-PRODUCER/1.0",
        "runtimeDistribution": "a615a-sim",
        "runtimeVersion": "0.0.1",
        "runId": "g3-run",
        "sessionId": "g3-session",
        "attemptId": "g3-run:g3-session:execution:1",
        "issuedActionId": "test-router",
        "actionKind": "TEST",
        "stage": "S4-EXECUTE-CALL",
        "fact": "FINITE-TOOL-EXCEPTION",
    }]
    assert validate_evidence_document(document, sources=sources) == document


def test_calculable_error_retains_raw_and_real_same_fresh_recover_continuation(tmp_path: Path) -> None:
    sources = _sources(tmp_path, scenario=_recovery_scenario())
    first = evidence_document(run_scenario(sources))
    fresh = evidence_document(run_scenario(sources))

    assert first == fresh
    assert [round_['selection']['actionId'] for round_ in first['rounds']] == ['test-router', 'recover-q1']
    assert first['rounds'][0]['resolutionCode'] == 'EXECUTION-IDENTITY-ERROR'
    assert first['rounds'][0]['rejectedResponse']['actionId'] == 'forged:test-router'
    assert first['rounds'][1]['resolutionCode'] == 'COMMIT'
    assert first['outcome']['state']['summary'] == 'q1'
    assert first['producerFacts'][0]['fact'] == 'CALCULABLE-IDENTITY-MISMATCH'
    assert first['producerFacts'][1]['fact'] == 'TYPED-VISIBLE-RECORD'
    assert validate_evidence_document(first, sources=sources) == first


@pytest.mark.parametrize(
    ("producer_mode", "first_resolution"),
    [
        ("OPAQUE-INVALID-SUCCESSOR", "EXECUTION-RESULT-TYPE-ERROR"),
        ("OPAQUE-TOOL-ERROR", "EXECUTION-TOOL-ERROR"),
    ],
)
def test_finite_fault_driver_does_not_reinject_an_opaque_fault_into_recover(
    tmp_path: Path,
    producer_mode: str,
    first_resolution: str,
) -> None:
    """A finite fault is one issued attempt, not a retry-cap shortcut."""

    sources = _sources(tmp_path, scenario=_recovery_scenario(producer_mode=producer_mode))
    document = evidence_document(run_scenario(sources))

    assert [round_["resolutionCode"] for round_ in document["rounds"]] == [first_resolution, "COMMIT"]
    assert document["rounds"][1]["selection"]["actionId"] == "recover-q1"
    assert document["outcome"]["state"]["summary"] == "q1"
    assert document["producerFacts"][1]["producerId"] == "cltav-runtime-synthetic-environment"
    assert validate_evidence_document(document, sources=sources) == document


def test_external_opaque_mode_cannot_be_downgraded_into_qualified_replay(tmp_path: Path) -> None:
    sources = _sources(tmp_path, scenario=_scenario(producer_mode="EXTERNAL-OPAQUE-UNVERIFIED"))
    with pytest.raises(EvidenceError) as rejected:
        run_scenario(sources)
    assert rejected.value.code == "EXTERNAL-OPAQUE-SOURCE-UNSUPPORTED"


def test_scenario_rejects_evaluator_truth_and_does_not_read_adjacent_truth_files(tmp_path: Path) -> None:
    """Truth labels have no route into finite prediction, selection or update."""

    truth_injected = _scenario()
    truth_injected["truth"] = {"expectedAction": "test-expensive-optimal"}
    injected_sources = _sources(tmp_path / "injected", scenario=truth_injected)
    with pytest.raises(EvidenceError) as injected_error:
        run_scenario(injected_sources)
    assert injected_error.value.code == "SCENARIO-SHAPE-ERROR"

    repo, commit = _authority_repo(tmp_path / "isolated")
    private_truth = repo / "evaluation-answer.json"
    private_truth.write_text('{"label":"first"}\n', encoding="utf-8")
    sources = load_sources(
        repository=repo,
        commit=commit,
        development_path=DEVELOPMENT_PATH,
        interface_path=INTERFACE_PATH,
        scenario_path=SCENARIO_PATH,
    )
    first = evidence_document(run_scenario(sources))
    private_truth.write_text('{"label":"second","answer":"test-expensive-optimal"}\n', encoding="utf-8")
    second = evidence_document(run_scenario(sources))
    assert second == first


def test_real_publication_success_rollback_and_first_failure_are_byte_safe(tmp_path: Path) -> None:
    sources = _sources(tmp_path)
    run = run_scenario(sources)
    output_parent = tmp_path / "published"
    output_parent.mkdir()
    output = output_parent / "evidence.json"

    published = publish_run(run, output=output)
    previous = output.read_bytes()
    assert load_evidence_bytes(previous) == published

    calls = 0

    def fail_replace(source: Path, target: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected replacement failure")
        os.replace(source, target)

    with pytest.raises(EvidenceError) as replacement_failure:
        publish_run(run, output=output, replace_fn=fail_replace)
    assert replacement_failure.value.code == "EVIDENCE-PUBLISH-ERROR"
    assert output.read_bytes() == previous
    assert not list(output_parent.glob(".evidence.json.staging-*"))
    assert not list(output_parent.glob(".evidence.json.backup-*"))

    first_failure = output_parent / "first.json"
    with pytest.raises(EvidenceError) as first_failure_error:
        publish_run(run, output=first_failure, replace_fn=lambda _source, _target: (_ for _ in ()).throw(OSError("injected first failure")))
    assert first_failure_error.value.code == "EVIDENCE-PUBLISH-ERROR"
    assert not first_failure.exists()
    assert not list(output_parent.glob(".first.json.staging-*"))


def test_staging_relation_failure_cannot_replace_an_existing_valid_package(tmp_path: Path) -> None:
    """The staged bytes are semantically checked before the first target move."""

    sources = _sources(tmp_path)
    run = run_scenario(sources)
    output_parent = tmp_path / "staging-protected"
    output_parent.mkdir()
    output = output_parent / "evidence.json"
    publish_run(run, output=output)
    previous = output.read_bytes()

    forged = evidence_document(run)
    forged["rounds"][0]["selection"]["actionId"] = "forged-after-staging"
    _refresh_integrity(forged)

    with pytest.raises(EvidenceError) as failure:
        _publish_bytes(
            canonical_json_bytes(forged),
            output=output,
            sources=sources,
            validator=lambda raw: validate_evidence_document(load_evidence_bytes(raw), sources=sources),
        )
    assert failure.value.code == "EVIDENCE-RELATION-MISMATCH"
    assert output.read_bytes() == previous
    assert not list(output_parent.glob(".evidence.json.staging-*"))
    assert not list(output_parent.glob(".evidence.json.backup-*"))


def test_publication_refuses_to_replace_unowned_user_material(tmp_path: Path) -> None:
    sources = _sources(tmp_path)
    output_parent = tmp_path / "user-material"
    output_parent.mkdir()
    target = output_parent / "notes.json"
    target.write_bytes(b"user-owned bytes\n")

    with pytest.raises(EvidenceError) as rejected:
        publish_run(run_scenario(sources), output=target)
    assert rejected.value.code == "UNSAFE-OUTPUT-PATH"
    assert target.read_bytes() == b"user-owned bytes\n"
    assert not list(output_parent.glob(".notes.json.staging-*"))
    assert not list(output_parent.glob(".notes.json.backup-*"))


def test_publication_refuses_to_write_inside_the_authority_repository(tmp_path: Path) -> None:
    """Authority inputs and persistent evidence must remain separate trees."""

    sources = _sources(tmp_path)
    target = sources.repository / "g3-evidence.json"
    with pytest.raises(EvidenceError) as rejected:
        publish_run(run_scenario(sources), output=target)
    assert rejected.value.code == "UNSAFE-OUTPUT-PATH"
    assert not target.exists()


def test_publication_rejects_a_leaf_symlink_before_any_target_move(tmp_path: Path) -> None:
    sources = _sources(tmp_path)
    output_parent = tmp_path / "symlink-output"
    output_parent.mkdir()
    owned = output_parent / "owned-evidence.json"
    publish_run(run_scenario(sources), output=owned)
    previous = owned.read_bytes()
    link = output_parent / "linked-evidence.json"
    try:
        os.symlink(owned.name, link)
    except OSError as exc:
        pytest.skip(f"symbolic links are unavailable in this environment: {exc}")

    with pytest.raises(EvidenceError) as rejected:
        publish_run(run_scenario(sources), output=link)
    assert rejected.value.code == "UNSAFE-OUTPUT-PATH"
    assert owned.read_bytes() == previous
    assert link.is_symlink()


def test_publication_rejects_a_dangling_leaf_symlink_before_staging(tmp_path: Path) -> None:
    """A broken link is still a link, even where ``Path.exists`` is false."""

    sources = _sources(tmp_path)
    output_parent = tmp_path / "dangling-symlink-output"
    output_parent.mkdir()
    link = output_parent / "dangling-evidence.json"
    try:
        os.symlink("missing-target.json", link)
    except OSError as exc:
        pytest.skip(f"symbolic links are unavailable in this environment: {exc}")

    with pytest.raises(EvidenceError) as rejected:
        publish_run(run_scenario(sources), output=link)
    assert rejected.value.code == "UNSAFE-OUTPUT-PATH"
    assert link.is_symlink()
    assert not list(output_parent.glob(".dangling-evidence.json.staging-*"))


def test_cli_uses_explicit_git_inputs_from_an_outside_directory_without_network(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo, commit = _authority_repo(
        tmp_path,
        scenario=_published_example_scenario(),
        scenario_path=PUBLISHED_SCENARIO_PATH,
    )
    # The command must consume the named Git object, not this dirty worktree
    # replacement.  This also keeps the test's fixture construction outside
    # every production lookup path.
    for path in (DEVELOPMENT_PATH, INTERFACE_PATH, PUBLISHED_SCENARIO_PATH):
        (repo / path).write_text('{"attacker":"worktree-only"}\n', encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    output = outside / "runtime-evidence.json"
    base = [
        "--authority-repository", str(repo),
        "--authority-commit", commit,
        "--development-path", DEVELOPMENT_PATH,
        "--interface-path", INTERFACE_PATH,
        "--scenario-path", PUBLISHED_SCENARIO_PATH,
    ]

    def no_network(*_args, **_kwargs):
        raise AssertionError("runtime CLI must not open a network connection")

    monkeypatch.setattr(socket, "create_connection", no_network)
    monkeypatch.setattr(socket.socket, "connect", no_network)
    monkeypatch.chdir(outside)
    assert cli.main(["run", *base, "--output", str(output)]) == 0
    assert cli.main(["validate", *base, "--evidence", str(output)]) == 0
    assert cli.main(["replay", *base, "--evidence", str(output)]) == 0
    assert output.is_file()
    produced = load_evidence_bytes(output.read_bytes())
    assert [item["selection"]["actionId"] for item in produced["rounds"]] == [
        "test-route", "test-follow",
    ]
    assert [item["chargedOnce"] for item in produced["rounds"]] == [True, True]

    forged = load_evidence_bytes(output.read_bytes())
    forged["producerFacts"] = []
    _refresh_integrity(forged)
    forged_path = outside / "forged-runtime-evidence.json"
    forged_path.write_bytes(canonical_json_bytes(forged))
    assert cli.main(["validate", *base, "--evidence", str(forged_path)]) == 1


def test_cli_rebuilds_a_genuine_error_then_recover_trace_from_the_same_git_inputs(
    tmp_path: Path,
) -> None:
    repo, commit = _authority_repo(tmp_path, scenario=_recovery_scenario())
    outside = tmp_path / "recovery-cli-outside"
    outside.mkdir()
    output = outside / "genuine-recovery.json"
    authority = [
        "--authority-repository", str(repo),
        "--authority-commit", commit,
        "--development-path", DEVELOPMENT_PATH,
        "--interface-path", INTERFACE_PATH,
        "--scenario-path", SCENARIO_PATH,
    ]

    assert cli.main(["run", *authority, "--output", str(output)]) == 0
    genuine = output.read_bytes()
    document = load_evidence_bytes(genuine)
    assert [item["resolutionCode"] for item in document["rounds"]] == [
        "EXECUTION-IDENTITY-ERROR", "COMMIT",
    ]
    assert cli.main(["validate", *authority, "--evidence", str(output)]) == 0
    assert cli.main(["replay", *authority, "--evidence", str(output)]) == 0

    forged = copy.deepcopy(document)
    forged["rounds"][0]["rejectedResponse"] = None
    _refresh_integrity(forged)
    forged_path = outside / "forged-recovery.json"
    forged_path.write_bytes(canonical_json_bytes(forged))
    assert cli.main(["validate", *authority, "--evidence", str(forged_path)]) == 1
    assert output.read_bytes() == genuine


def test_cli_publishes_a_named_resource_terminal_without_extra_dispatch(tmp_path: Path) -> None:
    """The installed command publishes an actual bounded resource stop, not a fixture label."""

    scenario = _scenario(maximum_rounds=2)
    session = scenario["session"]
    assert isinstance(session, dict)
    session["resourceRemaining"] = 1
    repo, commit = _authority_repo(tmp_path, scenario=scenario)
    outside = tmp_path / "resource-cli-outside"
    outside.mkdir()
    output = outside / "resource-terminal.json"
    authority = [
        "--authority-repository", str(repo),
        "--authority-commit", commit,
        "--development-path", DEVELOPMENT_PATH,
        "--interface-path", INTERFACE_PATH,
        "--scenario-path", SCENARIO_PATH,
    ]

    assert cli.main(["run", *authority, "--output", str(output)]) == 0
    document = load_evidence_bytes(output.read_bytes())
    assert document["outcome"]["stopReason"] == "Stop-Budget"
    assert [item["selection"]["actionId"] for item in document["rounds"]] == ["test-router"]
    assert document["outcome"]["state"]["resource"] == {"mode": "ROUNDS", "remaining": 0}
    assert cli.main(["validate", *authority, "--evidence", str(output)]) == 0


def test_noneditable_wheel_runs_the_real_finite_cli_from_an_unrelated_directory(tmp_path: Path) -> None:
    """The installed entry point has declared dependencies, no source leak or socket path."""

    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    build = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "--wheel-dir",
            str(wheel_dir),
            str(ROOT),
        ],
        text=True,
        capture_output=True,
    )
    assert build.returncode == 0, build.stderr
    wheel = next(wheel_dir.glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        assert "cltav_runtime/evidence.py" in archive.namelist()
        assert "cltav_runtime/cli.py" in archive.namelist()

    venv = tmp_path / "clean-wheel-venv"
    create = subprocess.run(
        [sys.executable, "-m", "venv", str(venv)],
        text=True,
        capture_output=True,
    )
    assert create.returncode == 0, create.stderr
    binary_dir = venv / ("Scripts" if os.name == "nt" else "bin")
    python = binary_dir / ("python.exe" if os.name == "nt" else "python")
    entrypoint = binary_dir / ("cltav-runtime.exe" if os.name == "nt" else "cltav-runtime")
    clean_environment = {
        key: value
        for key, value in os.environ.items()
        if key not in {"PYTHONHOME", "PYTHONPATH"}
    }
    clean_environment["PYTHONNOUSERSITE"] = "1"
    clean_environment["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    install = subprocess.run(
        [str(python), "-m", "pip", "install", "--no-input", str(wheel)],
        text=True,
        capture_output=True,
        env=clean_environment,
    )
    assert install.returncode == 0, install.stderr
    dependency_check = subprocess.run(
        [str(python), "-m", "pip", "check"],
        text=True,
        capture_output=True,
        env=clean_environment,
    )
    assert dependency_check.returncode == 0, dependency_check.stdout + dependency_check.stderr
    loaded = subprocess.run(
        [str(python), "-c", "import cltav_runtime; print(cltav_runtime.__file__)"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        env=clean_environment,
    )
    loaded_path = loaded.stdout.replace("\\", "/").strip()
    assert loaded.returncode == 0, loaded.stderr
    assert "/site-packages/cltav_runtime/" in loaded_path
    assert str(ROOT).replace("\\", "/").lower() not in loaded_path.lower()
    assert entrypoint.is_file()

    repo, commit = _authority_repo(
        tmp_path,
        scenario=_published_example_scenario(),
        scenario_path=PUBLISHED_SCENARIO_PATH,
    )
    outside = tmp_path / "unrelated-wheel-cwd"
    outside.mkdir()
    output = outside / "wheel-runtime-evidence.json"
    socket_guard = tmp_path / "socket-guard"
    socket_guard.mkdir()
    marker = socket_guard / "loaded.txt"
    (socket_guard / "sitecustomize.py").write_text(
        "import os\n"
        "from pathlib import Path\n"
        "import socket\n"
        "Path(os.environ['G3_SOCKET_GUARD_MARKER']).write_text('loaded', encoding='utf-8')\n"
        "def _blocked(*args, **kwargs):\n"
        "    raise AssertionError('G3 finite runtime must not create a network socket')\n"
        "socket.create_connection = _blocked\n"
        "class _BlockedSocket(socket.socket):\n"
        "    def connect(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "    def connect_ex(self, *args, **kwargs):\n"
        "        return _blocked(*args, **kwargs)\n"
        "socket.socket = _BlockedSocket\n",
        encoding="utf-8",
    )
    runtime_environment = dict(clean_environment)
    runtime_environment["PYTHONPATH"] = str(socket_guard)
    runtime_environment["G3_SOCKET_GUARD_MARKER"] = str(marker)
    authority = [
        "--authority-repository", str(repo),
        "--authority-commit", commit,
        "--development-path", DEVELOPMENT_PATH,
        "--interface-path", INTERFACE_PATH,
        "--scenario-path", PUBLISHED_SCENARIO_PATH,
    ]
    completed = subprocess.run(
        [str(entrypoint), "run", *authority, "--output", str(output)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=runtime_environment,
    )
    assert completed.returncode == 0, completed.stderr
    assert marker.read_text(encoding="utf-8") == "loaded"
    assert output.is_file()
    produced = load_evidence_bytes(output.read_bytes())
    assert [item["selection"]["actionId"] for item in produced["rounds"]] == [
        "test-route", "test-follow",
    ]
    validation = subprocess.run(
        [str(entrypoint), "validate", *authority, "--evidence", str(output)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=runtime_environment,
    )
    assert validation.returncode == 0, validation.stderr
    replay = subprocess.run(
        [str(entrypoint), "replay", *authority, "--evidence", str(output)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=runtime_environment,
    )
    assert replay.returncode == 0, replay.stderr

    forged = load_evidence_bytes(output.read_bytes())
    forged["producerFacts"] = []
    _refresh_integrity(forged)
    forged_path = outside / "wheel-forged-runtime-evidence.json"
    forged_path.write_bytes(canonical_json_bytes(forged))
    rejected = subprocess.run(
        [str(entrypoint), "validate", *authority, "--evidence", str(forged_path)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=runtime_environment,
    )
    assert rejected.returncode == 1
    assert "EVIDENCE-RELATION-MISMATCH" in rejected.stderr
