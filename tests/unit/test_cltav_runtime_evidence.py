"""Production-bound tests for the finite runtime evidence/CLI boundary.

The temporary authority repository is intentional: the runtime command must
consume Git objects passed on its command line, rather than fixtures in this
checkout.  The test may construct those inputs, but the production code has no
knowledge of the test directory.
"""

from __future__ import annotations

import copy
from dataclasses import replace
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
import cltav_runtime.evidence as evidence_module
from cltav_runtime.synthetic import SyntheticEnvironment
from cltav_runtime.evidence import (
    EvidenceError,
    _publish_bytes,
    canonical_json_bytes,
    checkpoint_document,
    continue_checkpoint,
    create_checkpoint,
    evidence_document,
    load_checkpoint_bytes,
    load_evidence_bytes,
    load_sources,
    publish_checkpoint,
    publish_run,
    run_scenario,
    validate_checkpoint_bytes,
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
    *,
    producer_mode: str = "CALCULABLE-IDENTITY-MISMATCH",
    resource_mode: str = "ROUNDS",
    resource_remaining: int = 2,
    recover_cost: int = 1,
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
            "recovery": recover_cost,
            "retry": 0,
        },
        "cost": recover_cost,
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
    session.update({
        "resourceMode": resource_mode,
        "resourceRemaining": resource_remaining,
        "retryCap": 2,
        "maximumRounds": 2,
    })
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


def _normal_noncommit_scenario(effect_class: str, *, missing_action: bool = False) -> dict[str, object]:
    """Return a legal normal producer scenario with a non-COMMIT S4 result."""

    scenario = _scenario(maximum_rounds=1)
    environment = scenario["environment"]
    assert isinstance(environment, dict)
    states = environment["states"]
    assert isinstance(states, dict)
    initial = states["private-a0"]
    assert isinstance(initial, dict)
    normal = initial["test-router"]
    assert isinstance(normal, dict)
    if missing_action:
        # Keep an ordinary nonempty environment state while deliberately not
        # defining the action selected by the source model.  The real normal
        # environment must then emit CONFIRMED-NOT-SENT itself.
        initial["unused-normal-action"] = copy.deepcopy(normal)
        del initial["test-router"]
        return scenario
    normal.update({
        "effectClass": effect_class,
        "observable": None,
        "summaryConfirmed": False,
        "postSummary": None,
        "measurementTick": None,
    })
    return scenario


def _response_free_timing_scenario() -> dict[str, object]:
    """A legal normal TEST with insufficient elapsed evidence at deadline."""

    scenario = _timed_observation_scenario()
    environment = scenario["environment"]
    assert isinstance(environment, dict)
    states = environment["states"]
    assert isinstance(states, dict)
    initial = states["private-a0"]
    assert isinstance(initial, dict)
    action = initial["test-router"]
    assert isinstance(action, dict)
    action.update({
        "observable": None,
        "summaryConfirmed": False,
        "postSummary": None,
        "measurementTick": None,
        "observationMaterial": {
            "events": [
                {"id": "req-g3", "sequence": 1, "kind": "REQUEST", "key": "g3-key", "eventType": "REQ", "timestamp": 0},
            ],
            "triggerEventId": "req-g3",
            "responseId": None,
            "measurementInterval": None,
            "observationEndQualified": True,
            "earliestElapsed": 0,
            "clockIdentity": "x",
            "unit": "ticks",
        },
    })
    return scenario


def _authority_arguments(repo: Path, commit: str, *, scenario_path: str = SCENARIO_PATH) -> list[str]:
    return [
        "--authority-repository", str(repo),
        "--authority-commit", commit,
        "--development-path", DEVELOPMENT_PATH,
        "--interface-path", INTERFACE_PATH,
        "--scenario-path", scenario_path,
    ]


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


def test_open_checkpoint_is_durably_validated_then_continues_without_repeating_prefix(
    tmp_path: Path,
) -> None:
    """EV04 consumes a saved prefix, rather than performing a second full run."""

    sources = _sources(tmp_path)
    prefix = create_checkpoint(sources, prefix_rounds=1)
    prefix_document = checkpoint_document(prefix)
    assert prefix_document["checkpoint"] == {
        "prefixRounds": 1,
        "sourceMaximumRounds": 2,
        "status": "OPEN-PREFIX",
    }
    assert prefix_document["outcome"]["stopReason"] == "Stop-Round-Limit"
    output_parent = tmp_path / "checkpoint-output"
    output_parent.mkdir()
    checkpoint_path = output_parent / "prefix.json"

    # Publication has already staged and independently rebuilt this package.
    # The returned value retains the actual same-session typed prefix.
    same = publish_checkpoint(prefix, output=checkpoint_path)
    assert load_checkpoint_bytes(checkpoint_path.read_bytes()) == prefix_document
    prior_evidence = same.result.state.evidence
    prior_attempts = same.result.state.attempts
    prior_remaining = same.result.state.resources.remaining
    same_continued = continue_checkpoint(same)
    assert same_continued.result.state.evidence[:1] == prior_evidence
    assert same_continued.result.state.attempts == prior_attempts + 1
    assert same_continued.result.state.resources.remaining == prior_remaining - 1
    assert [item.execution.execution_attempt_id for item in same_continued.result.state.evidence] == [
        "g3-run:g3-session:execution:1",
        "g3-run:g3-session:execution:2",
    ]

    # A reread package gets a separate source reconstruction, then formally
    # executes only its post-prefix action.  Its final public result is the
    # same as uninterrupted execution, without trusting JSON as a state.
    fresh = validate_checkpoint_bytes(checkpoint_path.read_bytes(), sources=sources)
    assert fresh._context.session is not same._context.session
    fresh_continued = continue_checkpoint(fresh)
    assert evidence_document(fresh_continued) == evidence_document(same_continued)
    assert evidence_document(fresh_continued) == evidence_document(run_scenario(sources))


@pytest.mark.parametrize(
    ("producer_mode", "first_resolution"),
    [
        ("CALCULABLE-IDENTITY-MISMATCH", "EXECUTION-IDENTITY-ERROR"),
        ("OPAQUE-INVALID-SUCCESSOR", "EXECUTION-RESULT-TYPE-ERROR"),
        ("OPAQUE-TOOL-ERROR", "EXECUTION-TOOL-ERROR"),
    ],
)
def test_checkpoint_rebuilds_each_error_prefix_then_formally_recovers_once(
    tmp_path: Path,
    producer_mode: str,
    first_resolution: str,
) -> None:
    """A reconstructed fault prefix cannot reinject its old first fault."""

    sources = _sources(tmp_path, scenario=_recovery_scenario(producer_mode=producer_mode))
    prefix = create_checkpoint(sources, prefix_rounds=1)
    checkpoint_path = tmp_path / f"{producer_mode.lower()}-prefix.json"
    same = publish_checkpoint(prefix, output=checkpoint_path)
    prefix_evidence = same.result.state.evidence
    assert prefix_evidence[0].resolution_code == first_resolution
    assert same.result.state.resources.mode == "ROUNDS"
    assert same.result.state.resources.remaining == 1

    same_continued = continue_checkpoint(same)
    assert [item.resolution_code for item in same_continued.result.state.evidence] == [
        first_resolution,
        "COMMIT",
    ]
    assert same_continued.result.state.evidence[:1] == prefix_evidence
    assert same_continued.result.state.context.q_status == "KNOWN"
    assert same_continued.result.state.resources.remaining == 0
    assert same_continued.result.state.evidence[1].snapshot.action_id == "recover-q1"

    fresh_continued = continue_checkpoint(
        validate_checkpoint_bytes(checkpoint_path.read_bytes(), sources=sources),
    )
    assert evidence_document(fresh_continued) == evidence_document(same_continued)
    assert evidence_document(fresh_continued) == evidence_document(run_scenario(sources))


def test_checkpoint_continuation_distinguishes_rounds_from_nonunit_budget_cost(tmp_path: Path) -> None:
    """EV04 retains the original mode and charges the new Recover exactly once."""

    rounds_sources = _sources(
        tmp_path / "rounds",
        scenario=_recovery_scenario(recover_cost=2),
    )
    budget_sources = _sources(
        tmp_path / "budget",
        scenario=_recovery_scenario(
            resource_mode="BUDGET",
            resource_remaining=3,
            recover_cost=2,
        ),
    )
    rounds = continue_checkpoint(publish_checkpoint(
        create_checkpoint(rounds_sources, prefix_rounds=1),
        output=tmp_path / "rounds-prefix.json",
    ))
    budget = continue_checkpoint(publish_checkpoint(
        create_checkpoint(budget_sources, prefix_rounds=1),
        output=tmp_path / "budget-prefix.json",
    ))
    assert rounds.result.state.evidence[0].resource_after.remaining == 1
    assert budget.result.state.evidence[0].resource_after.remaining == 2
    assert rounds.result.state.evidence[1].resource_after.remaining == 0
    assert budget.result.state.evidence[1].resource_after.remaining == 0
    assert rounds.result.state.resources == rounds.result.state.resources.rounds(0)
    assert budget.result.state.resources == budget.result.state.resources.budget(0)
    assert rounds.result.state.evidence[1].detail_charges["recovery"] == 2
    assert budget.result.state.evidence[1].detail_charges["recovery"] == 2


def test_checkpoint_validation_rebuild_and_formal_continue_have_distinct_execution_counts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A verification replay is isolated; formal continuation adds one step."""

    sources = _sources(tmp_path)
    calls: list[str] = []
    original_execute = SyntheticEnvironment.execute

    def counted_execute(self, request):
        calls.append(request.execution_attempt_id)
        return original_execute(self, request)

    monkeypatch.setattr(SyntheticEnvironment, "execute", counted_execute)
    prefix = create_checkpoint(sources, prefix_rounds=1)
    output = tmp_path / "counted-prefix.json"
    same = publish_checkpoint(prefix, output=output)
    assert calls == [
        "g3-run:g3-session:execution:1",  # original prefix
        "g3-run:g3-session:execution:1",  # isolated staged validation
    ]
    continued = continue_checkpoint(same)
    assert calls == [
        "g3-run:g3-session:execution:1",
        "g3-run:g3-session:execution:1",
        "g3-run:g3-session:execution:2",  # only formal new work
    ]
    assert continued.result.state.attempts == 2


def test_checkpoint_publication_is_transactional_for_existing_and_first_targets(tmp_path: Path) -> None:
    sources = _sources(tmp_path)
    prefix = create_checkpoint(sources, prefix_rounds=1)
    output_parent = tmp_path / "checkpoint-publication"
    output_parent.mkdir()
    output = output_parent / "prefix.json"
    publish_checkpoint(prefix, output=output)
    previous = output.read_bytes()

    calls = 0

    def fail_replace(source: Path, target: Path) -> None:
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected checkpoint replacement failure")
        os.replace(source, target)

    with pytest.raises(EvidenceError) as replacement_failure:
        publish_checkpoint(prefix, output=output, replace_fn=fail_replace)
    assert replacement_failure.value.code == "EVIDENCE-PUBLISH-ERROR"
    assert output.read_bytes() == previous
    assert not list(output_parent.glob(".prefix.json.staging-*"))
    assert not list(output_parent.glob(".prefix.json.backup-*"))

    first_target = output_parent / "first-prefix.json"
    with pytest.raises(EvidenceError) as first_failure:
        publish_checkpoint(
            prefix,
            output=first_target,
            replace_fn=lambda _source, _target: (_ for _ in ()).throw(OSError("injected first failure")),
        )
    assert first_failure.value.code == "EVIDENCE-PUBLISH-ERROR"
    assert not first_target.exists()
    assert not list(output_parent.glob(".first-prefix.json.staging-*"))


def test_checkpoint_rejects_terminal_prefix_and_semantic_forgery_before_continuation(
    tmp_path: Path,
) -> None:
    terminal = _scenario(maximum_rounds=2)
    terminal_session = terminal["session"]
    assert isinstance(terminal_session, dict)
    terminal_session["resourceRemaining"] = 1
    with pytest.raises(EvidenceError) as terminal_error:
        create_checkpoint(_sources(tmp_path / "terminal", scenario=terminal), prefix_rounds=1)
    assert terminal_error.value.code == "CHECKPOINT-NOT-OPEN"

    sources = _sources(tmp_path / "forged")
    path = tmp_path / "forged" / "prefix.json"
    path.parent.mkdir(exist_ok=True)
    publish_checkpoint(create_checkpoint(sources, prefix_rounds=1), output=path)
    genuine = path.read_bytes()
    forged = load_checkpoint_bytes(genuine)
    forged["rounds"][0]["selection"]["actionId"] = "forged-after-prefix"
    _refresh_integrity(forged)
    with pytest.raises(EvidenceError) as relation_error:
        validate_checkpoint_bytes(canonical_json_bytes(forged), sources=sources)
    assert relation_error.value.code == "CHECKPOINT-RELATION-MISMATCH"
    assert path.read_bytes() == genuine


def test_continuation_rejects_a_reconstructed_public_checkpoint_object(tmp_path: Path) -> None:
    sources = _sources(tmp_path)
    verified = publish_checkpoint(
        create_checkpoint(sources, prefix_rounds=1),
        output=tmp_path / "trusted-prefix.json",
    )
    with pytest.raises(EvidenceError) as rejected:
        continue_checkpoint(replace(verified, prefix_rounds=0))
    assert rejected.value.code == "CHECKPOINT-PROVENANCE-ERROR"


@pytest.mark.parametrize("mutation", ["raw", "resolution", "history", "producer", "source"])
def test_checkpoint_mutations_are_rejected_before_formal_continuation(
    tmp_path: Path,
    mutation: str,
) -> None:
    sources = _sources(tmp_path)
    checkpoint = checkpoint_document(create_checkpoint(sources, prefix_rounds=1))
    if mutation == "raw":
        checkpoint["rounds"][0]["execution"]["evidenceRef"] = "forged-raw"
    elif mutation == "resolution":
        checkpoint["rounds"][0]["resolutionCode"] = "forged-resolution"
    elif mutation == "history":
        checkpoint["outcome"]["state"]["history"]["version"] = 99
    elif mutation == "producer":
        checkpoint["producerFacts"] = []
    else:
        checkpoint["inputs"]["scenario"]["path"] = "configs/runtime/forged.json"
    _refresh_integrity(checkpoint)
    with pytest.raises(EvidenceError) as rejected:
        validate_checkpoint_bytes(canonical_json_bytes(checkpoint), sources=sources)
    assert rejected.value.code in {"CHECKPOINT-RELATION-MISMATCH", "EVIDENCE-SOURCE-MISMATCH"}


def test_cli_checkpoint_then_continue_consumes_a_genuine_error_prefix_once(
    tmp_path: Path,
) -> None:
    repo, commit = _authority_repo(
        tmp_path,
        scenario=_recovery_scenario(producer_mode="OPAQUE-TOOL-ERROR"),
    )
    outside = tmp_path / "continuation-cli-outside"
    outside.mkdir()
    checkpoint_path = outside / "prefix.json"
    final_path = outside / "continued.json"
    authority = _authority_arguments(repo, commit)

    assert cli.main([
        "checkpoint", *authority, "--prefix-rounds", "1", "--output", str(checkpoint_path),
    ]) == 0
    prefix = load_checkpoint_bytes(checkpoint_path.read_bytes())
    assert prefix["rounds"][0]["resolutionCode"] == "EXECUTION-TOOL-ERROR"
    assert cli.main(["validate", *authority, "--evidence", str(checkpoint_path)]) == 0
    assert cli.main([
        "continue", *authority, "--checkpoint", str(checkpoint_path), "--output", str(final_path),
    ]) == 0
    final = load_evidence_bytes(final_path.read_bytes())
    assert [item["resolutionCode"] for item in final["rounds"]] == [
        "EXECUTION-TOOL-ERROR", "COMMIT",
    ]
    assert final["rounds"][1]["selection"]["actionId"] == "recover-q1"

    forged = copy.deepcopy(prefix)
    forged["rounds"][0]["execution"]["evidenceRef"] = "forged-prefix-raw"
    _refresh_integrity(forged)
    forged_path = outside / "forged-prefix.json"
    forged_path.write_bytes(canonical_json_bytes(forged))
    previous_final = final_path.read_bytes()
    assert cli.main([
        "continue", *authority, "--checkpoint", str(forged_path), "--output", str(final_path),
    ]) == 1
    assert final_path.read_bytes() == previous_final


@pytest.mark.parametrize("invalid_mode", [[], {}, None, 1, True, "UNBOUNDED"])
def test_malformed_resource_mode_has_named_cli_error_without_publication(
    tmp_path: Path,
    invalid_mode: object,
    capsys: pytest.CaptureFixture[str],
) -> None:
    scenario = _scenario()
    session = scenario["session"]
    assert isinstance(session, dict)
    session["resourceMode"] = invalid_mode
    repo, commit = _authority_repo(tmp_path, scenario=scenario)
    output = tmp_path / "bad-mode.json"
    assert cli.main(["run", *_authority_arguments(repo, commit), "--output", str(output)]) == 1
    captured = capsys.readouterr()
    assert "SCENARIO-SHAPE-ERROR" in captured.err
    assert "Traceback" not in captured.err
    assert not output.exists()


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("path", "configs/runtime/other.json"),
        ("commit", "0" * 40),
        ("blobSha256", "0" * 64),
    ],
)
def test_source_identity_is_rejected_before_any_verification_run(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    replacement: str,
) -> None:
    sources = _sources(tmp_path)
    document = evidence_document(run_scenario(sources))
    document["inputs"]["scenario"][field] = replacement
    _refresh_integrity(document)
    calls = 0
    original = evidence_module.run_scenario

    def counted(value):
        nonlocal calls
        calls += 1
        return original(value)

    monkeypatch.setattr(evidence_module, "run_scenario", counted)
    with pytest.raises(EvidenceError) as rejected:
        validate_evidence_document(document, sources=sources)
    assert rejected.value.code == "EVIDENCE-SOURCE-MISMATCH"
    assert calls == 0


def test_checkpoint_source_identity_is_rejected_before_prefix_rebuild(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources = _sources(tmp_path)
    document = checkpoint_document(create_checkpoint(sources, prefix_rounds=1))
    document["inputs"]["scenario"]["path"] = "configs/runtime/other.json"
    _refresh_integrity(document)
    calls = 0
    original = evidence_module.create_checkpoint

    def counted(*args, **kwargs):
        nonlocal calls
        calls += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(evidence_module, "create_checkpoint", counted)
    with pytest.raises(EvidenceError) as rejected:
        evidence_module.validate_checkpoint_document(document, sources=sources)
    assert rejected.value.code == "EVIDENCE-SOURCE-MISMATCH"
    assert calls == 0


def test_relation_diagnostics_name_the_semantic_field_and_preserve_exact_types(tmp_path: Path) -> None:
    sources = _sources(tmp_path)
    changed_action = evidence_document(run_scenario(sources))
    changed_action["rounds"][0]["selection"]["actionId"] = "forged-action"
    _refresh_integrity(changed_action)
    with pytest.raises(EvidenceError) as action_error:
        validate_evidence_document(changed_action, sources=sources)
    assert action_error.value.code == "EVIDENCE-RELATION-MISMATCH"
    assert "$.rounds[0].selection.actionId" in str(action_error.value)

    changed_boolean = evidence_document(run_scenario(sources))
    changed_boolean["rounds"][0]["chargedOnce"] = 1
    _refresh_integrity(changed_boolean)
    with pytest.raises(EvidenceError) as type_error:
        validate_evidence_document(changed_boolean, sources=sources)
    assert type_error.value.code == "EVIDENCE-RELATION-MISMATCH"
    assert "$.rounds[0].chargedOnce" in str(type_error.value)


@pytest.mark.parametrize(
    ("scenario", "resolution", "fact"),
    [
        (_normal_noncommit_scenario("CONFIRMED-NOT-SENT"), "CONFIRMED-NOT-SENT", "TYPED-CONFIRMED-NOT-SENT"),
        (_normal_noncommit_scenario("UNKNOWN-EFFECT"), "UNKNOWN-EFFECT", "TYPED-UNKNOWN-EFFECT"),
        (_normal_noncommit_scenario("NONE", missing_action=True), "CONFIRMED-NOT-SENT", "TYPED-CONFIRMED-NOT-SENT"),
    ],
)
def test_normal_noncommit_producer_facts_publish_and_rebuild(
    tmp_path: Path,
    scenario: dict[str, object],
    resolution: str,
    fact: str,
) -> None:
    sources = _sources(tmp_path, scenario=scenario)
    document = evidence_document(run_scenario(sources))
    assert document["rounds"][0]["resolutionCode"] == resolution
    assert document["producerFacts"][0]["fact"] == fact
    assert validate_evidence_document(document, sources=sources) == document
    repo = sources.repository
    output = tmp_path / "normal-noncommit.json"
    assert cli.main(["run", *_authority_arguments(repo, sources.scenario.commit), "--output", str(output)]) == 0
    assert load_evidence_bytes(output.read_bytes())["producerFacts"][0]["fact"] == fact


def test_normal_response_free_pending_deadline_material_can_publish_without_commit(
    tmp_path: Path,
) -> None:
    sources = _sources(tmp_path, scenario=_response_free_timing_scenario())
    document = evidence_document(run_scenario(sources))
    assert document["rounds"][0]["resolutionCode"] == "OBSERVATION-NO-RESPONSE"
    assert document["rounds"][0]["observationAssessment"]["verdict"] == "INCONCLUSIVE"
    assert document["producerFacts"][0]["fact"] == "TYPED-NO-RESPONSE-MATERIAL"
    assert validate_evidence_document(document, sources=sources) == document
    output = tmp_path / "response-free.json"
    assert cli.main([
        "run", *_authority_arguments(sources.repository, sources.scenario.commit), "--output", str(output),
    ]) == 0
    assert load_evidence_bytes(output.read_bytes())["producerFacts"][0]["fact"] == "TYPED-NO-RESPONSE-MATERIAL"


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

    # The same non-editable installed command must also consume a durable
    # error prefix and execute only the post-prefix Recover action.
    recovery_repo, recovery_commit = _authority_repo(
        tmp_path / "wheel-recovery-authority",
        scenario=_recovery_scenario(producer_mode="OPAQUE-INVALID-SUCCESSOR"),
    )
    recovery_authority = _authority_arguments(recovery_repo, recovery_commit)
    checkpoint_path = outside / "wheel-prefix.json"
    continued_path = outside / "wheel-continued.json"
    checkpoint = subprocess.run(
        [str(entrypoint), "checkpoint", *recovery_authority, "--prefix-rounds", "1", "--output", str(checkpoint_path)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=runtime_environment,
    )
    assert checkpoint.returncode == 0, checkpoint.stderr
    checkpoint_validation = subprocess.run(
        [str(entrypoint), "validate", *recovery_authority, "--evidence", str(checkpoint_path)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=runtime_environment,
    )
    assert checkpoint_validation.returncode == 0, checkpoint_validation.stderr
    continuation = subprocess.run(
        [str(entrypoint), "continue", *recovery_authority, "--checkpoint", str(checkpoint_path), "--output", str(continued_path)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=runtime_environment,
    )
    assert continuation.returncode == 0, continuation.stderr
    continued = load_evidence_bytes(continued_path.read_bytes())
    assert [item["resolutionCode"] for item in continued["rounds"]] == [
        "EXECUTION-RESULT-TYPE-ERROR", "COMMIT",
    ]

    forged_checkpoint = load_checkpoint_bytes(checkpoint_path.read_bytes())
    forged_checkpoint["producerFacts"] = []
    _refresh_integrity(forged_checkpoint)
    forged_checkpoint_path = outside / "wheel-forged-prefix.json"
    forged_checkpoint_path.write_bytes(canonical_json_bytes(forged_checkpoint))
    forged_continuation = subprocess.run(
        [str(entrypoint), "continue", *recovery_authority, "--checkpoint", str(forged_checkpoint_path), "--output", str(continued_path)],
        cwd=outside,
        text=True,
        capture_output=True,
        env=runtime_environment,
    )
    assert forged_continuation.returncode == 1
    assert "CHECKPOINT-RELATION-MISMATCH" in forged_continuation.stderr
