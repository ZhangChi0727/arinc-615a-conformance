"""Public Git-snapshot tests for B/C-2C finite applicability routing.

The runtime must not infer a named ARINC 645 residual from a caller-supplied
scenario, service label, or mutable worktree file.  These tests therefore
assemble a small real Git repository and enter only through the public
``RuntimeAuthorityBinding.from_git_objects`` and ``ReferenceSession`` APIs.
They do not call private applicability helpers or hand-construct a residual.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
from typing import Any, Callable, Mapping

import pytest

from cltav_runtime.bindings import RuntimeAuthorityBinding
from cltav_runtime.kernel import ContractSnapshot, ModelContext
from cltav_runtime.model import FiniteSessionModel
from cltav_runtime.session import ReferenceSession, ResourceState


ROOT = Path(__file__).resolve().parents[2]
DEVELOPMENT_PATH = "configs/engineering/cltav_development_contracts.json"
INTERFACE_PATH = "configs/research/cltav_interface_registry.json"
INTEGRITY_BASELINE_PATH = "configs/engineering/cltav_integrity_obligation_baseline.json"
APPLICABILITY_SCHEMA_PATH = "configs/engineering/cltav_runtime_applicability.schema.json"
APPLICABILITY_MANIFEST_PATH = "configs/engineering/cltav_runtime_applicability.json"
APPLICABILITY_FIXTURE_PATH = "configs/engineering/cltav_runtime_applicability_fixture.json"


_SIX_CONTEXTS = (
    (
        "CTX-645-00076",
        "CRS-M1-00076",
        "DEP-INTEGRITY-RUNTIME",
        "SU-ARINC-615A-3-5-4-2-P047-PROSE-SENTENCE-025-3CF28DC21423",
        "INT-INFORMATION-RECEIVER-SUPPORT",
    ),
    (
        "CTX-645-00082",
        "CRS-M1-00082",
        "DEP-INTEGRITY-RUNTIME",
        "SU-ARINC-615A-3-5-4-3-P048-PROSE-SENTENCE-026-F38D018C4499",
        "INT-UPLOAD-RECEIVER-SUPPORT",
    ),
    (
        "CTX-645-00085",
        "CRS-M1-00085",
        "DEP-INTEGRITY-RUNTIME",
        "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-007-F209ABE1376B",
        "INT-FINAL-IMAGE-LSP-VALUE",
    ),
    (
        "CTX-645-00086",
        "CRS-M1-00086",
        "DEP-INTEGRITY-RUNTIME",
        "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-008-CDA43D6568CC",
        "INT-OPTIONAL-OLD-NEW-COMPARE",
    ),
    (
        "CTX-645-00087",
        "CRS-M1-00087",
        "DEP-INTEGRITY-RUNTIME",
        "SU-ARINC-615A-3-5-4-3-1-P049-PROSE-SENTENCE-010-F4624AC8DCB4",
        "INT-SAME-PART-NUMBER-CRC-EQUALITY",
    ),
    (
        "CTX-645-00109",
        "CRS-M1-00109",
        "DEP-INTEGRITY-RUNTIME",
        "SU-ARINC-615A-3-6-3-2-P068-PROSE-SENTENCE-042-4C1D759A6B9A",
        "INT-POST-DATA-STATUS-CONTINUATION",
    ),
)


class _NoDispatch:
    """An S4 probe which makes premature dispatch observable."""

    def __init__(self) -> None:
        self.calls = 0

    def execute(self, request: object) -> object:  # pragma: no cover - must not run
        self.calls += 1
        raise AssertionError(f"unexpected S4 dispatch: {request}")


def _run_git(repository: Path, *arguments: str, capture: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    return completed.stdout if capture else ""


def _root_git_bytes(relative_path: str) -> bytes:
    """Read a controlled authority from the actual HEAD blob, not CRLF checkout bytes."""

    output = _run_git(ROOT, "show", f"HEAD:{relative_path}", capture=True)
    assert isinstance(output, bytes)
    return output


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _json_at(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _commit(repository: Path, message: str) -> str:
    _run_git(repository, "add", ".")
    _run_git(
        repository,
        "-c",
        "user.name=CLTAV applicability test",
        "-c",
        "user.email=applicability@example.invalid",
        "commit",
        "-qm",
        message,
    )
    output = _run_git(repository, "rev-parse", "HEAD", capture=True)
    assert isinstance(output, bytes)
    return output.decode("ascii").strip()


def _temporary_authority_repo(
    tmp_path: Path,
    *,
    mutate_manifest: Callable[[dict[str, Any]], None] | None = None,
    mutate_fixture: Callable[[dict[str, Any]], None] | None = None,
) -> tuple[Path, str]:
    """Create a Git-exact authority snapshot with the controlled six sources.

    The development contract and integrity baseline are deliberately copied
    from ``git show HEAD:<path>``.  On Windows their checkout bytes can be
    CRLF-normalized, whereas the manifest binds their Git blob bytes.
    """

    repository = tmp_path / "authority-repository"
    repository.mkdir(parents=True)
    payloads = {
        DEVELOPMENT_PATH: _root_git_bytes(DEVELOPMENT_PATH),
        INTERFACE_PATH: _root_git_bytes(INTERFACE_PATH),
        INTEGRITY_BASELINE_PATH: _root_git_bytes(INTEGRITY_BASELINE_PATH),
        APPLICABILITY_SCHEMA_PATH: (ROOT / APPLICABILITY_SCHEMA_PATH).read_bytes(),
        APPLICABILITY_MANIFEST_PATH: (ROOT / APPLICABILITY_MANIFEST_PATH).read_bytes(),
        APPLICABILITY_FIXTURE_PATH: (ROOT / APPLICABILITY_FIXTURE_PATH).read_bytes(),
    }
    for relative_path, payload in payloads.items():
        destination = repository / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)

    manifest_path = repository / APPLICABILITY_MANIFEST_PATH
    fixture_path = repository / APPLICABILITY_FIXTURE_PATH
    if mutate_fixture is not None:
        fixture = _json_at(fixture_path)
        mutate_fixture(fixture)
        _write_json(fixture_path, fixture)
    if mutate_manifest is not None:
        manifest = _json_at(manifest_path)
        mutate_manifest(manifest)
        _write_json(manifest_path, manifest)

    # A fixture mutation is a legitimate new raw Git source for a negative
    # test.  Rebind its declared source identity before testing its semantic
    # validation; other source identities remain the controlled blob bytes.
    if mutate_fixture is not None:
        manifest = _json_at(manifest_path)
        bindings = manifest["sourceBindings"]
        assert isinstance(bindings, dict)
        fixture_binding = bindings["fixture"]
        assert isinstance(fixture_binding, dict)
        fixture_binding["blobSha256"] = sha256(fixture_path.read_bytes()).hexdigest()
        _write_json(manifest_path, manifest)

    _run_git(repository, "init", "-q")
    _run_git(repository, "config", "core.autocrlf", "false")
    return repository, _commit(repository, "controlled applicability sources")


def _binding(
    repository: Path,
    *,
    authority_commit: str,
    manifest_commit: str | None = None,
) -> RuntimeAuthorityBinding:
    return RuntimeAuthorityBinding.from_git_objects(
        repository=repository,
        development_commit=authority_commit,
        development_path=DEVELOPMENT_PATH,
        interface_commit=authority_commit,
        interface_path=INTERFACE_PATH,
        applicability_schema_commit=authority_commit,
        applicability_schema_path=APPLICABILITY_SCHEMA_PATH,
        applicability_manifest_commit=manifest_commit or authority_commit,
        applicability_manifest_path=APPLICABILITY_MANIFEST_PATH,
        applicability_fixture_commit=authority_commit,
        applicability_fixture_path=APPLICABILITY_FIXTURE_PATH,
        integrity_baseline_commit=authority_commit,
        integrity_baseline_path=INTEGRITY_BASELINE_PATH,
    )


def _git_json(repository: Path, commit: str, relative_path: str) -> dict[str, Any]:
    output = _run_git(repository, "show", f"{commit}:{relative_path}", capture=True)
    assert isinstance(output, bytes)
    value = json.loads(output.decode("utf-8"))
    assert isinstance(value, dict)
    return value


def _model(repository: Path, commit: str, model_id: str) -> FiniteSessionModel:
    fixture = _git_json(repository, commit, APPLICABILITY_FIXTURE_PATH)
    models = fixture["models"]
    assert isinstance(models, list)
    row = next(item for item in models if item["id"] == model_id)
    assert isinstance(row, dict)
    algorithm = row["algorithmModel"]
    assert isinstance(algorithm, dict)
    public_model = algorithm["model"]
    assert isinstance(public_model, dict)
    typed_domains = public_model["typedDomains"]
    assert isinstance(typed_domains, dict)
    snapshot = ContractSnapshot.from_git_object(
        repository=repository,
        contract_commit=commit,
        contract_path=DEVELOPMENT_PATH,
    )
    context = ModelContext.build(
        snapshot=snapshot,
        model={
            "stateIds": set(public_model["stateIds"]),
            "clockIds": set(public_model["clockIds"]),
            "typedDomains": {
                name: set(domain)
                for name, domain in typed_domains.items()
            },
        },
        projection_clock="x",
    )
    return FiniteSessionModel.from_mapping(context=context, value=algorithm)


def _session(
    binding: RuntimeAuthorityBinding,
    model: FiniteSessionModel,
    *,
    context_id: str,
    session_id: str = "applicability-session",
    named_645_residuals: object | None = None,
    scenario_id: object | None = None,
) -> ReferenceSession:
    return ReferenceSession(
        binding=binding,
        model=model,
        session_id=session_id,
        run_id=f"run-{session_id}",
        initial_summary="q0",
        resources=ResourceState.rounds(0),
        retry_cap=1,
        applicability_context_id=context_id,
        named_645_residuals=named_645_residuals,
        scenario_id=scenario_id,
    )


def _source_tuple_from_development(
    repository: Path,
    commit: str,
    requirement_id: str,
) -> tuple[str, str, str, str]:
    development = _git_json(repository, commit, DEVELOPMENT_PATH)
    dependencies = development["implementationDependencies"]
    assert isinstance(dependencies, list)
    dependency = next(item for item in dependencies if item["id"] == "DEP-INTEGRITY-RUNTIME")
    assert isinstance(dependency, dict)
    rows = dependency["sourceBindings"]
    assert isinstance(rows, list)
    row = next(item for item in rows if item["requirementId"] == requirement_id)
    assert isinstance(row, dict)
    return (
        requirement_id,
        "DEP-INTEGRITY-RUNTIME",
        row["sourceUnitId"],
        row["contractId"],
    )


@pytest.mark.parametrize("context_id, requirement_id, dependency_id, source_unit_id, contract_id", _SIX_CONTEXTS)
def test_each_exact_integrity_context_routes_multi_h_zero_resource_to_stop_645(
    tmp_path: Path,
    context_id: str,
    requirement_id: str,
    dependency_id: str,
    source_unit_id: str,
    contract_id: str,
) -> None:
    """Each source-bound finite context wins P3 before P5 without dispatch."""

    repository, commit = _temporary_authority_repo(tmp_path)
    binding = _binding(repository, authority_commit=commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")
    session = _session(binding, model, context_id=context_id, session_id=f"p3-{requirement_id}")
    no_dispatch = _NoDispatch()

    result = session.step(session.initial_state, no_dispatch)  # type: ignore[arg-type]

    expected = (requirement_id, dependency_id, source_unit_id, contract_id)
    assert expected == _source_tuple_from_development(repository, commit, requirement_id)
    assert result.stop_reason == "Stop-645"
    assert result.state == session.initial_state
    assert no_dispatch.calls == 0
    assert result.stop_trace is not None
    assert result.stop_trace.phase == "ENTRY"
    assert result.stop_trace.applicability_status == "P3-ACTIVE"
    assert result.stop_trace.final_hypotheses == ("h0", "h1")
    assert [
        (item.requirement_id, item.dependency_id, item.source_unit_id, item.contract_id)
        for item in result.stop_trace.active_named_645_residuals
    ] == [expected]
    assert result.stop_trace.applicability_context_id == context_id
    assert result.stop_trace.applicability_input_identity


def test_explicit_method_only_context_has_no_p3_residual_and_reaches_budget_stop(tmp_path: Path) -> None:
    """A controlled non-integrity model cannot acquire a global Stop-645."""

    repository, commit = _temporary_authority_repo(tmp_path)
    binding = _binding(repository, authority_commit=commit)
    model = _model(repository, commit, "MODEL-METHOD-ONLY")
    session = _session(binding, model, context_id="CTX-METHOD-ONLY", session_id="method-only")
    no_dispatch = _NoDispatch()

    result = session.step(session.initial_state, no_dispatch)  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Budget"
    assert no_dispatch.calls == 0
    assert result.stop_trace is not None
    assert result.stop_trace.active_named_645_residuals == ()
    assert result.stop_trace.applicability_context_id == "CTX-METHOD-ONLY"
    assert result.stop_trace.applicability_status == "P3-METHOD-ONLY"


def _legacy_binding(repository: Path, commit: str) -> RuntimeAuthorityBinding:
    return RuntimeAuthorityBinding.from_git_objects(
        repository=repository,
        development_commit=commit,
        development_path=DEVELOPMENT_PATH,
        interface_commit=commit,
        interface_path=INTERFACE_PATH,
    )


def test_legacy_double_input_binding_remains_explicitly_p3_unavailable(tmp_path: Path) -> None:
    """The preserved generic runtime path is not a METHOD-ONLY substitute."""

    repository, commit = _temporary_authority_repo(tmp_path)
    binding = _legacy_binding(repository, commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="legacy-unavailable",
        run_id="run-legacy-unavailable",
        initial_summary="q0",
        resources=ResourceState.rounds(0),
        retry_cap=1,
    )

    result = session.step(session.initial_state, _NoDispatch())  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Budget"
    assert result.stop_trace is not None
    assert result.stop_trace.applicability_status == "P3-UNAVAILABLE"
    assert result.stop_trace.applicability_context_id is None
    assert result.stop_trace.active_named_645_residuals == ()


def test_package_requires_context_and_legacy_rejects_one_before_dispatch(tmp_path: Path) -> None:
    """Neither an absent package nor an absent context may silently switch modes."""

    repository, commit = _temporary_authority_repo(tmp_path)
    package_binding = _binding(repository, authority_commit=commit)
    legacy_binding = _legacy_binding(repository, commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")

    with pytest.raises(ValueError, match="APPLICABILITY-INPUT-ERROR"):
        ReferenceSession(
            binding=package_binding,
            model=model,
            session_id="missing-context",
            run_id="run-missing-context",
            initial_summary="q0",
            resources=ResourceState.rounds(0),
            retry_cap=1,
        )
    with pytest.raises(ValueError, match="APPLICABILITY-INPUT-ERROR"):
        _session(legacy_binding, model, context_id="CTX-645-00076")


def test_p3_checkpoint_cannot_resume_under_a_legacy_binding(tmp_path: Path) -> None:
    """S0 freezes the evaluated applicability domain across fresh replay."""

    repository, commit = _temporary_authority_repo(tmp_path)
    package_binding = _binding(repository, authority_commit=commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")
    source = _session(package_binding, model, context_id="CTX-645-00076", session_id="p3-to-legacy")
    first = source.step(source.initial_state, _NoDispatch())  # type: ignore[arg-type]
    assert first.stop_reason == "Stop-645"
    legacy = ReferenceSession(
        binding=_legacy_binding(repository, commit),
        model=model,
        session_id="p3-to-legacy",
        run_id="run-p3-to-legacy",
        initial_summary="q0",
        resources=ResourceState.rounds(0),
        retry_cap=1,
    )
    no_dispatch = _NoDispatch()

    replay = legacy.step(first.state, no_dispatch)  # type: ignore[arg-type]

    assert replay.stop_reason == "Stop-Error"
    assert replay.diagnostics[0].code == "SESSION-AUTHORITY-MISMATCH"
    assert no_dispatch.calls == 0


def test_fresh_same_package_replays_the_same_p3_context_and_residual_identity(tmp_path: Path) -> None:
    """A fresh verified package preserves P3 rather than reinterpreting S0."""

    repository, commit = _temporary_authority_repo(tmp_path)
    source = _session(
        _binding(repository, authority_commit=commit),
        _model(repository, commit, "MODEL-INTEGRITY-STOP"),
        context_id="CTX-645-00076",
        session_id="p3-fresh-same-package",
    )
    first = source.step(source.initial_state, _NoDispatch())  # type: ignore[arg-type]
    fresh = _session(
        _binding(repository, authority_commit=commit),
        _model(repository, commit, "MODEL-INTEGRITY-STOP"),
        context_id="CTX-645-00076",
        session_id="p3-fresh-same-package",
    )
    no_dispatch = _NoDispatch()

    replay = fresh.step(first.state, no_dispatch)  # type: ignore[arg-type]

    assert first.stop_reason == replay.stop_reason == "Stop-645"
    assert first.stop_trace is not None and replay.stop_trace is not None
    assert first.stop_trace.applicability_status == replay.stop_trace.applicability_status == "P3-ACTIVE"
    assert first.stop_trace.applicability_context_id == replay.stop_trace.applicability_context_id == "CTX-645-00076"
    assert first.stop_trace.applicability_input_identity == replay.stop_trace.applicability_input_identity
    assert first.stop_trace.active_named_645_residuals == replay.stop_trace.active_named_645_residuals
    assert no_dispatch.calls == 0


def _one_integrity_hypothesis(fixture: dict[str, Any]) -> None:
    models = fixture["models"]
    assert isinstance(models, list) and isinstance(models[0], dict)
    algorithm = models[0]["algorithmModel"]
    assert isinstance(algorithm, dict)
    hypotheses = algorithm["hypotheses"]
    assert isinstance(hypotheses, list)
    algorithm["hypotheses"] = [hypotheses[0]]
    actions = algorithm["actions"]
    assert isinstance(actions, list) and isinstance(actions[0], dict)
    action = actions[0]
    observable = action["observableByHypothesis"]
    ticks = action["measurementTicksByHypothesis"]
    assert isinstance(observable, dict) and isinstance(ticks, dict)
    observable.pop("h1")
    ticks.pop("h1")


def test_p2_singleton_precedes_an_active_bound_p3_residual(tmp_path: Path) -> None:
    """P2 remains prior to P3 even in a valid integrity applicability context."""

    repository, commit = _temporary_authority_repo(tmp_path, mutate_fixture=_one_integrity_hypothesis)
    binding = _binding(repository, authority_commit=commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")
    session = ReferenceSession(
        binding=binding,
        model=model,
        session_id="p2-before-p3",
        run_id="run-p2-before-p3",
        initial_summary="q0",
        resources=ResourceState.rounds(0),
        retry_cap=1,
        applicability_context_id="CTX-645-00076",
    )

    result = session.step(session.initial_state, _NoDispatch())  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Singleton"
    assert result.stop_trace is not None
    assert result.stop_trace.active_named_645_residuals[0].requirement_id == "CRS-M1-00076"


def _inactive_information_option(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[0], dict)
    public_inputs = tasks[0]["publicInputs"]
    assert isinstance(public_inputs, dict)
    public_inputs["optionSelected"] = False


def _information_not_selected(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    declarations = references["optionSelections"]
    assert isinstance(declarations, list) and isinstance(declarations[0], dict)
    assert declarations[0]["id"] == "selection-information-a"
    declarations[0]["selected"] = False


def _inactive_comparison(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[3], dict)
    public_inputs = tasks[3]["publicInputs"]
    assert isinstance(public_inputs, dict)
    public_inputs["comparisonSelected"] = False
    public_inputs["comparisonDeclarationId"] = "comparison-not-selected-a"
    reason_refs = tasks[3]["reasonRefs"]
    assert isinstance(reason_refs, list)
    tasks[3]["reasonRefs"] = [
        "comparison-not-selected-a" if item == "comparison-selected-a" else item
        for item in reason_refs
    ]


def _comparison_not_selected(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    declarations = references["comparisonDeclarations"]
    assert isinstance(declarations, list) and isinstance(declarations[1], dict)
    assert declarations[1]["id"] == "comparison-not-selected-a"
    declarations[1]["selected"] = False


@pytest.mark.parametrize(
    ("manifest_mutation", "fixture_mutation", "context_id"),
    [
        (_inactive_information_option, _information_not_selected, "CTX-645-00076"),
        (_inactive_comparison, _comparison_not_selected, "CTX-645-00086"),
    ],
)
def test_explicit_inactive_controls_are_valid_but_do_not_create_a_p3_residual(
    tmp_path: Path,
    manifest_mutation: Callable[[dict[str, Any]], None],
    fixture_mutation: Callable[[dict[str, Any]], None] | None,
    context_id: str,
) -> None:
    """A typed false control differs from missing/unknown applicability input."""

    repository, commit = _temporary_authority_repo(
        tmp_path,
        mutate_manifest=manifest_mutation,
        mutate_fixture=fixture_mutation,
    )
    binding = _binding(repository, authority_commit=commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")
    session = _session(binding, model, context_id=context_id)
    result = session.step(session.initial_state, _NoDispatch())  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-Budget"
    assert result.stop_trace is not None
    assert result.stop_trace.applicability_status == "P3-EXPLICIT-INACTIVE"
    assert result.stop_trace.active_named_645_residuals == ()


def test_same_part_task_remains_active_when_optional_comparison_is_explicitly_inactive(tmp_path: Path) -> None:
    """00087 owns its inputs and cannot be suppressed by 00086's control."""

    repository, commit = _temporary_authority_repo(
        tmp_path,
        mutate_manifest=_inactive_comparison,
        mutate_fixture=_comparison_not_selected,
    )
    binding = _binding(repository, authority_commit=commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")
    session = _session(binding, model, context_id="CTX-645-00087", session_id="independent-00087")

    result = session.step(session.initial_state, _NoDispatch())  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-645"
    assert result.stop_trace is not None
    assert result.stop_trace.active_named_645_residuals[0].requirement_id == "CRS-M1-00087"


@pytest.mark.parametrize("legacy_value", [(), [], [{"requirementId": "CRS-M1-00076"}]])
def test_caller_cannot_supply_legacy_residuals_or_a_scenario_selector(
    tmp_path: Path,
    legacy_value: object,
) -> None:
    """The public constructor rejects both pre-addendum P3 bypass channels."""

    repository, commit = _temporary_authority_repo(tmp_path)
    binding = _binding(repository, authority_commit=commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")

    with pytest.raises(ValueError, match="APPLICABILITY-INPUT-ERROR.*caller-supplied"):
        _session(
            binding,
            model,
            context_id="CTX-645-00076",
            named_645_residuals=legacy_value,
        )
    with pytest.raises(ValueError, match="APPLICABILITY-INPUT-ERROR.*scenario identifiers"):
        _session(
            binding,
            model,
            context_id="CTX-645-00076",
            scenario_id="DISPLAY-FORGED-STOP-ROUTE",
        )


def _omit_a_source_tuple(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list)
    tasks.pop()


def _swap_source_units(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list)
    first, second = tasks[0], tasks[1]
    assert isinstance(first, dict) and isinstance(second, dict)
    first["sourceUnitId"], second["sourceUnitId"] = second["sourceUnitId"], first["sourceUnitId"]


def _wrong_dependency(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[0], dict)
    tasks[0]["dependencyId"] = "DEP-FORGED-RUNTIME"


@pytest.mark.parametrize(
    ("mutation", "label"),
    [
        (_omit_a_source_tuple, "omitted source tuple"),
        (_swap_source_units, "swapped source tuples"),
        (_wrong_dependency, "wrong dependency"),
    ],
)
def test_manifest_rejects_any_missing_or_repaired_source_tuple_before_dispatch(
    tmp_path: Path,
    mutation: Callable[[dict[str, Any]], None],
    label: str,
) -> None:
    """P3 accepts the exact six-row authority relation, not merely valid IDs."""

    repository, commit = _temporary_authority_repo(tmp_path, mutate_manifest=mutation)
    no_dispatch = _NoDispatch()

    with pytest.raises(ValueError, match="APPLICABILITY-INPUT-ERROR"):
        _binding(repository, authority_commit=commit)
    assert no_dispatch.calls == 0, label


def _support_false(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    declarations = references["supportDeclarations"]
    assert isinstance(declarations, list) and isinstance(declarations[0], dict)
    declarations[0]["declaredSupport"] = False


def _support_null(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    declarations = references["supportDeclarations"]
    assert isinstance(declarations, list) and isinstance(declarations[0], dict)
    declarations[0]["declaredSupport"] = None


def _bad_protected_bytes_reference(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[0], dict)
    values = tasks[0]["publicInputs"]
    assert isinstance(values, dict)
    values["protectedBytesId"] = "missing-protected-bytes"


def _unknown_option_selection(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[0], dict)
    values = tasks[0]["publicInputs"]
    assert isinstance(values, dict)
    values["optionSelected"] = None


def _bad_selection_reference(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[0], dict)
    values = tasks[0]["publicInputs"]
    assert isinstance(values, dict)
    values["selectionDeclarationId"] = "missing-selection-declaration"


def _wrong_receiver_role(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    receivers = references["receivers"]
    assert isinstance(receivers, list) and isinstance(receivers[0], dict)
    receivers[0]["role"] = "SENDER"


def _unrelated_reason_reference(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[0], dict)
    tasks[0]["reasonRefs"] = ["file-a"]


def _bad_status_order(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    events = references["events"]
    assert isinstance(events, list) and isinstance(events[0], dict)
    assert events[0]["id"] == "event-final-data-a"
    events[0]["at"] = 100


def _wrong_integrity_file_service(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    bytes_rows = references["byteBindings"]
    assert isinstance(bytes_rows, list) and isinstance(bytes_rows[2], dict)
    assert bytes_rows[2]["id"] == "bytes-image-a"
    bytes_rows[2]["service"] = "INFORMATION"


def _comparison_declares_different_files(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    declarations = references["comparisonDeclarations"]
    assert isinstance(declarations, list) and isinstance(declarations[0], dict)
    declarations[0]["oldFileId"] = "file-a"


def _check_value_uses_another_configuration(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    check_values = references["checkValues"]
    assert isinstance(check_values, list) and isinstance(check_values[0], dict)
    check_values[0]["algorithmConfigurationId"] = "other-configuration"


def _comparison_check_value_uses_missing_configuration(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    check_values = references["checkValues"]
    assert isinstance(check_values, list) and isinstance(check_values[2], dict)
    assert check_values[2]["id"] == "check-old-a"
    check_values[2]["algorithmConfigurationId"] = "missing-configuration"


def _comparison_check_values_use_blank_configuration_fields(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    configurations = references["algorithmConfigurations"]
    check_values = references["checkValues"]
    assert isinstance(configurations, list) and isinstance(configurations[0], dict)
    assert isinstance(check_values, list)
    configuration = dict(configurations[0])
    configuration.update(
        {
            "id": "algorithm-config-comparison-only",
            "algorithmId": "   ",
            "configurationId": "   ",
        },
    )
    configurations.append(configuration)
    for index in (2, 3):
        assert isinstance(check_values[index], dict)
        check_values[index]["algorithmConfigurationId"] = configuration["id"]


def _same_part_blank_configuration_manifest(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list)
    task = next(item for item in tasks if item.get("requirementId") == "CRS-M1-00087")
    assert isinstance(task, dict)
    public_inputs = task["publicInputs"]
    reason_refs = task["reasonRefs"]
    assert isinstance(public_inputs, dict) and isinstance(reason_refs, list)
    public_inputs["algorithmConfigurationId"] = "algorithm-config-same-part-only"
    task["reasonRefs"] = [
        "algorithm-config-same-part-only" if value == "algorithm-config-a" else value
        for value in reason_refs
    ]


def _same_part_check_values_use_blank_configuration_fields(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    configurations = references["algorithmConfigurations"]
    check_values = references["checkValues"]
    assert isinstance(configurations, list) and isinstance(configurations[0], dict)
    assert isinstance(check_values, list)
    configuration = dict(configurations[0])
    configuration.update(
        {
            "id": "algorithm-config-same-part-only",
            "algorithmId": "   ",
            "configurationId": "   ",
        },
    )
    configurations.append(configuration)
    for index in (4, 5):
        assert isinstance(check_values[index], dict)
        check_values[index]["algorithmConfigurationId"] = configuration["id"]


def _same_part_check_value_has_blank_source(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    check_values = references["checkValues"]
    assert isinstance(check_values, list) and isinstance(check_values[4], dict)
    assert check_values[4]["id"] == "check-file-a"
    check_values[4]["source"] = "   "


def _blank_same_part_number(fixture: dict[str, Any]) -> None:
    references = fixture["references"]
    assert isinstance(references, dict)
    files = references["files"]
    assert isinstance(files, list) and isinstance(files[5], dict)
    assert files[5]["id"] == "file-b"
    files[5]["partNumber"] = "   "


def _method_only_reuses_integrity_action(manifest: dict[str, Any]) -> None:
    contexts = manifest["methodOnlyContexts"]
    assert isinstance(contexts, list) and isinstance(contexts[0], dict)
    contexts[0]["modelId"] = "MODEL-INTEGRITY-STOP"
    contexts[0]["actionIds"] = ["integrity-observe"]


def _malformed_fixture_model(fixture: dict[str, Any]) -> None:
    models = fixture["models"]
    assert isinstance(models, list) and isinstance(models[0], dict)
    algorithm = models[0]["algorithmModel"]
    assert isinstance(algorithm, dict)
    algorithm["model"] = {}


@pytest.mark.parametrize(
    ("manifest_mutation", "fixture_mutation", "label"),
    [
        (None, _support_false, "false receiver support"),
        (None, _support_null, "unknown receiver support"),
        (_bad_protected_bytes_reference, None, "unresolved protected bytes"),
        (_unknown_option_selection, None, "unknown option selection"),
        (_inactive_information_option, None, "unbound false option selection"),
        (_bad_selection_reference, None, "unresolved option selection declaration"),
        (None, _wrong_receiver_role, "wrong receiver role"),
        (_unrelated_reason_reference, None, "unrelated reason reference"),
        (None, _bad_status_order, "status evidence before FINAL-DATA"),
        (None, _wrong_integrity_file_service, "non-upload integrity file bytes"),
        (None, _comparison_declares_different_files, "unbound comparison declaration"),
        (None, _check_value_uses_another_configuration, "unbound check-value configuration"),
        (None, _comparison_check_value_uses_missing_configuration, "unresolved comparison check-value configuration"),
        (None, _comparison_check_values_use_blank_configuration_fields, "blank comparison check-value configuration fields"),
        (_same_part_blank_configuration_manifest, _same_part_check_values_use_blank_configuration_fields, "blank same-part check-value configuration fields"),
        (None, _same_part_check_value_has_blank_source, "blank same-part check-value source"),
        (None, _blank_same_part_number, "blank same-part-number identity"),
        (_method_only_reuses_integrity_action, None, "method-only integrity-action reuse"),
        (None, _malformed_fixture_model, "malformed finite fixture model"),
    ],
)
def test_invalid_applicability_prerequisites_fail_before_a_session_can_dispatch(
    tmp_path: Path,
    manifest_mutation: Callable[[dict[str, Any]], None] | None,
    fixture_mutation: Callable[[dict[str, Any]], None] | None,
    label: str,
) -> None:
    """Missing public inputs are named authority errors, never non-applicability."""

    repository, commit = _temporary_authority_repo(
        tmp_path,
        mutate_manifest=manifest_mutation,
        mutate_fixture=fixture_mutation,
    )
    no_dispatch = _NoDispatch()

    with pytest.raises(ValueError, match="APPLICABILITY-INPUT-ERROR"):
        _binding(repository, authority_commit=commit)
    assert no_dispatch.calls == 0, label


def _retag_display_metadata(manifest: dict[str, Any]) -> None:
    tasks = manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[0], dict)
    tasks[0]["displayScenarioId"] = "DISPLAY-RETAGGED-ONLY"
    tasks[0]["displayService"] = "RETAGGED-METADATA-ONLY"


def _terminal_tuple(
    repository: Path,
    commit: str,
    *,
    manifest_commit: str | None = None,
) -> tuple[tuple[str, str, str, str], str]:
    binding = _binding(repository, authority_commit=commit, manifest_commit=manifest_commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")
    session = _session(binding, model, context_id="CTX-645-00076", session_id="retag")
    result = session.step(session.initial_state, _NoDispatch())  # type: ignore[arg-type]
    assert result.stop_reason == "Stop-645" and result.stop_trace is not None
    residual = result.stop_trace.active_named_645_residuals
    assert len(residual) == 1
    item = residual[0]
    return (
        (item.requirement_id, item.dependency_id, item.source_unit_id, item.contract_id),
        result.stop_trace.applicability_input_identity or "",
    )


def test_display_retag_changes_manifest_identity_but_not_source_tuple_semantics(tmp_path: Path) -> None:
    """Display metadata is not a P3 selector or substitute for public facts."""

    baseline_repo, baseline_commit = _temporary_authority_repo(tmp_path / "baseline")
    retagged_repo, retagged_commit = _temporary_authority_repo(
        tmp_path / "retagged",
        mutate_manifest=_retag_display_metadata,
    )

    baseline_tuple, baseline_input = _terminal_tuple(baseline_repo, baseline_commit)
    retagged_tuple, retagged_input = _terminal_tuple(retagged_repo, retagged_commit)

    assert baseline_tuple == retagged_tuple == _SIX_CONTEXTS[0][1:]
    assert baseline_input != retagged_input


def test_worktree_drift_after_git_binding_cannot_rewrite_the_frozen_p3_input(tmp_path: Path) -> None:
    """The session consumes Git source bytes, even if the checkout is later altered."""

    repository, commit = _temporary_authority_repo(tmp_path)
    binding = _binding(repository, authority_commit=commit)
    model = _model(repository, commit, "MODEL-INTEGRITY-STOP")

    manifest_path = repository / APPLICABILITY_MANIFEST_PATH
    drifted_manifest = _json_at(manifest_path)
    tasks = drifted_manifest["tasks"]
    assert isinstance(tasks, list) and isinstance(tasks[0], dict)
    values = tasks[0]["publicInputs"]
    assert isinstance(values, dict)
    values["protectedBytesId"] = "worktree-forged-missing-bytes"
    _write_json(manifest_path, drifted_manifest)
    assert _run_git(repository, "status", "--short", capture=True)

    session = _session(binding, model, context_id="CTX-645-00076", session_id="worktree-drift")
    no_dispatch = _NoDispatch()
    result = session.step(session.initial_state, no_dispatch)  # type: ignore[arg-type]

    assert result.stop_reason == "Stop-645"
    assert no_dispatch.calls == 0
    assert result.stop_trace is not None
    assert result.stop_trace.active_named_645_residuals[0].requirement_id == "CRS-M1-00076"


def _alternate_manifest(manifest: dict[str, Any]) -> None:
    artifact = manifest["artifact"]
    assert isinstance(artifact, dict)
    artifact["version"] = "1.0-alternate-manifest-identity"


def test_retained_state_cannot_replay_under_an_alternate_git_bound_manifest(tmp_path: Path) -> None:
    """S0/state authority includes the exact manifest snapshot, not its labels alone."""

    repository, initial_commit = _temporary_authority_repo(tmp_path)
    binding = _binding(repository, authority_commit=initial_commit)
    model = _model(repository, initial_commit, "MODEL-INTEGRITY-STOP")
    source = _session(binding, model, context_id="CTX-645-00076", session_id="alternate-manifest")
    first = source.step(source.initial_state, _NoDispatch())  # type: ignore[arg-type]
    assert first.stop_reason == "Stop-645"

    manifest_path = repository / APPLICABILITY_MANIFEST_PATH
    alternate = _json_at(manifest_path)
    _alternate_manifest(alternate)
    _write_json(manifest_path, alternate)
    alternate_manifest_commit = _commit(repository, "alternate manifest identity")

    alternate_binding = _binding(
        repository,
        authority_commit=initial_commit,
        manifest_commit=alternate_manifest_commit,
    )
    assert alternate_binding.identities()["development"]["commit"] == initial_commit
    assert alternate_binding.identities()["applicabilityManifest"]["commit"] == alternate_manifest_commit
    target = _session(
        alternate_binding,
        model,
        context_id="CTX-645-00076",
        session_id="alternate-manifest",
    )
    no_dispatch = _NoDispatch()

    replay = target.step(first.state, no_dispatch)  # type: ignore[arg-type]

    assert replay.stop_reason == "Stop-Error"
    assert replay.diagnostics[0].code == "SESSION-AUTHORITY-MISMATCH"
    assert no_dispatch.calls == 0
