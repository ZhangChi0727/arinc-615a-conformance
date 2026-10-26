"""Immutable authority bindings for the bounded CL-TAV runtime.

The runtime is deliberately a *consumer* of controlled engineering and
research contracts.  This module reads declared Git objects directly and
retains their raw-byte identity; it does not use a convenient worktree copy as
an authority and does not construct a second requirements catalogue.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import subprocess
from types import MappingProxyType
from typing import Any, Mapping

from .applicability import (
    ApplicabilityInputError,
    RuntimeApplicabilityProjection,
    build_runtime_applicability_projection,
)
from .kernel import ContractSnapshot, ModelContext
from .model import FiniteSessionModel, verified_finite_session_model
from .stopping import Named645Residual, StopInputs


_SOURCE_SNAPSHOT_TOKEN = object()
_BINDING_TOKEN = object()
_RUNTIME_INTERFACE_IDS = frozenset(
    {
        "IF-PRED-OBS",
        "IF-SELECT-ADMIT",
        "IF-EXECUTE-RECORD",
        "IF-OBS-INTERPRET",
        "IF-PREP-RECOVER",
        "IF-HIST-UPDATE",
        "IF-EQUIV",
        "IF-RESOURCE-STOP",
    }
)
_REQUIRED_RECORD_IDS = frozenset({"HISTORY-HANDLE", "OBSERVATION-ASSESSMENT"})
_REQUIRED_PARAMETER_IDS = frozenset(
    {
        "RP-HYPOTHESIS-COUNT",
        "RP-PATH-LENGTH",
        "RP-FRONTIER-STATE-COUNT",
        "RP-ACTION-COUNT",
        "RP-OBSERVATION-CLASS-COUNT",
        "RP-RETRY-CAP",
        "RP-RESOURCE-MODE",
    }
)
_EXPECTED_INTERFACE_OUTPUTS = {
    "IF-PRED-OBS": ("currentlyValidNonemptyClasses", "PredictionGapError"),
    "IF-SELECT-ADMIT": ("kind", "tStar", "S", "admitA2A5"),
    "IF-EXECUTE-RECORD": ("record", "effectClass", "correlationId"),
    "IF-OBS-INTERPRET": (
        "Iz", "effectClass", "summaryConfirmed", "postSummary", "ownershipResult", "measurementInterval",
    ),
    "IF-PREP-RECOVER": (
        "targetConfirmed", "summaryConfirmed", "prepError", "ineligible", "declaredTarget", "evidence", "postSummary",
    ),
    "IF-HIST-UPDATE": ("HistoryHandlePrime", "Hprime", "Stop-Empty"),
    "IF-EQUIV": ("established", "notEstablished", "unknown"),
    "IF-RESOURCE-STOP": ("stopClass", "finalH", "trace"),
}
# This is intentionally a named, closed adapter map.  It records presentation
# aliases without relying on either the registry's array position or a TeX
# presentation order (notably ALG-05's ``k,S,t*,admit`` rendering).
NAMED_INTERFACE_ADAPTERS: Mapping[str, Mapping[str, str]] = MappingProxyType(
    {
        "IF-PRED-OBS": MappingProxyType({
            "currentlyValidNonemptyClasses": "prediction.classes",
            "PredictionGapError": "prediction.gapDiagnostic",
        }),
        "IF-SELECT-ADMIT": MappingProxyType({
            "kind": "selection.kind",
            "tStar": "selection.actionId",
            "S": "selection.classes",
            "admitA2A5": "selection.admission",
        }),
        "IF-EXECUTE-RECORD": MappingProxyType({
            "record": "execution.visibleRecord",
            "effectClass": "execution.effectClass",
            "correlationId": "execution.executionAttemptId",
        }),
        "IF-OBS-INTERPRET": MappingProxyType({
            "Iz": "interpretation.observationClass",
            "effectClass": "interpretation.effectClass",
            "summaryConfirmed": "interpretation.summaryConfirmed",
            "postSummary": "interpretation.postSummary",
            "ownershipResult": "interpretation.ownershipResult",
            "measurementInterval": "interpretation.measurementInterval",
        }),
        "IF-PREP-RECOVER": MappingProxyType({
            "targetConfirmed": "recovery.targetConfirmed",
            "summaryConfirmed": "recovery.summaryConfirmed",
            "prepError": "recovery.prepError",
            "ineligible": "recovery.ineligible",
            "declaredTarget": "recovery.declaredTarget",
            "evidence": "recovery.evidence",
            "postSummary": "recovery.postSummary",
        }),
        "IF-HIST-UPDATE": MappingProxyType({
            "HistoryHandlePrime": "history.after",
            "Hprime": "history.after.hypotheses",
            "Stop-Empty": "stop.empty",
        }),
        "IF-EQUIV": MappingProxyType({
            "established": "equivalence.established",
            "notEstablished": "equivalence.notEstablished",
            "unknown": "equivalence.unknown",
        }),
        "IF-RESOURCE-STOP": MappingProxyType({
            "stopClass": "stop.reason",
            "finalH": "stop.finalHypotheses",
            "trace": "stop.trace",
        }),
    },
)


def _safe_repository_path(value: str) -> str:
    """Return a portable repository-relative path or reject it."""

    if type(value) is not str or not value or "\\" in value:
        raise ValueError("controlled source path must be a nonempty POSIX path")
    if PureWindowsPath(value).is_absolute() or PurePosixPath(value).is_absolute():
        raise ValueError("controlled source path must be repository-relative")
    path = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("controlled source path contains an unsafe component")
    return path.as_posix()


def _validate_commit(value: str) -> str:
    if (
        type(value) is not str
        or len(value) != 40
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError("controlled source commit identity is invalid")
    return value


@dataclass(frozen=True)
class SourceSnapshot:
    """A verified raw Git object used by one authority consumer."""

    commit: str
    path: str
    blob_sha256: str
    _content: bytes = field(default=b"", init=False, compare=False, repr=False)
    _binding_sha256: str = field(default="", init=False, compare=False, repr=False)
    _verification_token: object | None = field(
        default=None, init=False, compare=False, repr=False,
    )

    @classmethod
    def from_git_object(
        cls, *, repository: Path | str, commit: str, path: str,
    ) -> "SourceSnapshot":
        commit = _validate_commit(commit)
        path = _safe_repository_path(path)
        repository_path = Path(repository).resolve()
        if not repository_path.is_dir():
            raise ValueError("controlled source repository is not an existing directory")
        try:
            resolved = subprocess.run(
                ["git", "-C", str(repository_path), "rev-parse", "--verify", f"{commit}^{{commit}}"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            ).stdout.strip()
            if resolved != commit:
                raise ValueError("controlled source commit does not resolve to declared identity")
            content = subprocess.run(
                ["git", "-C", str(repository_path), "show", f"{resolved}:{path}"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).stdout
        except subprocess.CalledProcessError as exc:
            raise ValueError("controlled source Git object cannot be loaded") from exc
        snapshot = cls(commit=resolved, path=path, blob_sha256=sha256(content).hexdigest())
        object.__setattr__(snapshot, "_content", content)
        object.__setattr__(snapshot, "_binding_sha256", _source_snapshot_binding_digest(snapshot))
        object.__setattr__(snapshot, "_verification_token", _SOURCE_SNAPSHOT_TOKEN)
        return snapshot

    def json_object(self) -> Mapping[str, Any]:
        if not _verified_source_snapshot(self):
            raise ValueError("controlled source snapshot is not verified")
        try:
            value = json.loads(self._content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("controlled source object must be UTF-8 JSON") from exc
        if not isinstance(value, Mapping):
            raise ValueError("controlled source root must be an object")
        return value

    def identity(self) -> Mapping[str, str]:
        if not _verified_source_snapshot(self):
            raise ValueError("controlled source snapshot is not verified")
        return MappingProxyType(
            {"commit": self.commit, "path": self.path, "blobSha256": self.blob_sha256},
        )


@dataclass(frozen=True)
class RuntimeAuthorityBinding:
    """Verified projection of the authorities consumed by the runtime.

    The projection only names the finite interfaces and record/parameter IDs
    required by the reference session.  The controlled JSON files remain the
    authorities for their full contents.
    """

    development: ContractSnapshot
    interfaces: SourceSnapshot
    development_artifact_id: str
    development_version: str
    finite_refinement_id: str
    interface_ids: frozenset[str]
    record_ids: frozenset[str]
    runtime_parameter_ids: frozenset[str]
    applicability_schema: SourceSnapshot | None = None
    applicability_manifest: SourceSnapshot | None = None
    applicability_fixture: SourceSnapshot | None = None
    integrity_baseline: SourceSnapshot | None = None
    applicability: RuntimeApplicabilityProjection | None = None
    _verification_token: object | None = field(
        default=None, init=False, compare=False, repr=False,
    )

    @classmethod
    def from_git_objects(
        cls,
        *,
        repository: Path | str,
        development_commit: str,
        development_path: str,
        interface_commit: str,
        interface_path: str,
        applicability_schema_commit: str | None = None,
        applicability_schema_path: str | None = None,
        applicability_manifest_commit: str | None = None,
        applicability_manifest_path: str | None = None,
        applicability_fixture_commit: str | None = None,
        applicability_fixture_path: str | None = None,
        integrity_baseline_commit: str | None = None,
        integrity_baseline_path: str | None = None,
    ) -> "RuntimeAuthorityBinding":
        development = ContractSnapshot.from_git_object(
            repository=repository,
            contract_commit=development_commit,
            contract_path=development_path,
        )
        interfaces = SourceSnapshot.from_git_object(
            repository=repository,
            commit=interface_commit,
            path=interface_path,
        )
        applicability_values = (
            applicability_schema_commit,
            applicability_schema_path,
            applicability_manifest_commit,
            applicability_manifest_path,
            applicability_fixture_commit,
            applicability_fixture_path,
            integrity_baseline_commit,
            integrity_baseline_path,
        )
        if any(value is not None for value in applicability_values) and any(
            value is None for value in applicability_values
        ):
            raise ValueError("runtime applicability source binding is incomplete")
        if not any(value is not None for value in applicability_values):
            return cls._from_verified_snapshots(development=development, interfaces=interfaces)
        assert all(isinstance(value, str) for value in applicability_values)
        schema = SourceSnapshot.from_git_object(
            repository=repository,
            commit=applicability_schema_commit,
            path=applicability_schema_path,
        )
        manifest = SourceSnapshot.from_git_object(
            repository=repository,
            commit=applicability_manifest_commit,
            path=applicability_manifest_path,
        )
        fixture = SourceSnapshot.from_git_object(
            repository=repository,
            commit=applicability_fixture_commit,
            path=applicability_fixture_path,
        )
        baseline = SourceSnapshot.from_git_object(
            repository=repository,
            commit=integrity_baseline_commit,
            path=integrity_baseline_path,
        )
        return cls._from_verified_snapshots(
            development=development,
            interfaces=interfaces,
            applicability_schema=schema,
            applicability_manifest=manifest,
            applicability_fixture=fixture,
            integrity_baseline=baseline,
        )

    @classmethod
    def _from_verified_snapshots(
        cls,
        *,
        development: ContractSnapshot,
        interfaces: SourceSnapshot,
        applicability_schema: SourceSnapshot | None = None,
        applicability_manifest: SourceSnapshot | None = None,
        applicability_fixture: SourceSnapshot | None = None,
        integrity_baseline: SourceSnapshot | None = None,
    ) -> "RuntimeAuthorityBinding":
        development_object = development._parsed_contract()
        interface_object = interfaces.json_object()
        identity = development_object.get("identity")
        refinements = development_object.get("algorithmRefinements")
        record_contracts = development_object.get("recordContracts")
        parameters = development_object.get("runtimeParameterContracts")
        registry_interfaces = interface_object.get("interfaces")
        if not isinstance(identity, Mapping):
            raise ValueError("development contract identity is invalid")
        artifact_id = identity.get("artifactId")
        version = identity.get("version")
        if not isinstance(artifact_id, str) or not artifact_id or not isinstance(version, str) or not version:
            raise ValueError("development contract identity is incomplete")
        if not isinstance(refinements, list) or not isinstance(record_contracts, list) or not isinstance(parameters, list):
            raise ValueError("development runtime projection is incomplete")
        if not isinstance(registry_interfaces, list):
            raise ValueError("interface registry has no interface list")
        refinement = next(
            (
                item for item in refinements
                if isinstance(item, Mapping) and item.get("id") == "AR-FINITE"
            ),
            None,
        )
        if not isinstance(refinement, Mapping):
            raise ValueError("development contract does not contain AR-FINITE")
        bindings = refinement.get("interfaceBindings")
        if not isinstance(bindings, list):
            raise ValueError("AR-FINITE interface bindings are invalid")
        bound_ids = _unique_string_ids(bindings, "interfaceId", "AR-FINITE interface bindings")
        registry_ids = _unique_string_ids(registry_interfaces, "id", "interface registry")
        record_ids = _unique_string_ids(record_contracts, "id", "record contracts")
        parameter_ids = _unique_string_ids(parameters, "id", "runtime parameters")
        if bound_ids != _RUNTIME_INTERFACE_IDS:
            raise ValueError("AR-FINITE does not bind the complete runtime interface set")
        if not _RUNTIME_INTERFACE_IDS <= registry_ids:
            raise ValueError("interface registry does not provide each runtime interface")
        for interface in registry_interfaces:
            if interface["id"] not in _RUNTIME_INTERFACE_IDS:
                continue
            outputs = interface.get("outputs")
            if not isinstance(outputs, list) or tuple(outputs) != _EXPECTED_INTERFACE_OUTPUTS[interface["id"]]:
                raise ValueError("interface registry output contract differs from named runtime binding")
        if not _REQUIRED_RECORD_IDS <= record_ids:
            raise ValueError("development record contracts do not provide runtime records")
        if not _REQUIRED_PARAMETER_IDS <= parameter_ids:
            raise ValueError("development runtime parameters are incomplete")
        applicability_snapshots = (
            applicability_schema,
            applicability_manifest,
            applicability_fixture,
            integrity_baseline,
        )
        if any(item is None for item in applicability_snapshots) and any(
            item is not None for item in applicability_snapshots
        ):
            raise ValueError("runtime applicability source binding is incomplete")
        applicability: RuntimeApplicabilityProjection | None = None
        if all(item is not None for item in applicability_snapshots):
            assert applicability_schema is not None
            assert applicability_manifest is not None
            assert applicability_fixture is not None
            assert integrity_baseline is not None
            if not all(_verified_source_snapshot(item) for item in applicability_snapshots):
                raise ValueError("runtime applicability source snapshot is not verified")
            development_identity = MappingProxyType(
                {
                    "commit": development.contract_commit,
                    "path": development.contract_path,
                    "blobSha256": development.contract_blob_sha256,
                },
            )
            try:
                applicability = build_runtime_applicability_projection(
                    schema_bytes=applicability_schema._content,
                    manifest_bytes=applicability_manifest._content,
                    fixture_bytes=applicability_fixture._content,
                    development=development_object,
                    integrity_baseline_bytes=integrity_baseline._content,
                    source_identities={
                        "schema": applicability_schema.identity(),
                        "manifest": applicability_manifest.identity(),
                        "fixture": applicability_fixture.identity(),
                        "development": development_identity,
                        "integrityBaseline": integrity_baseline.identity(),
                    },
                )
                _validate_applicability_fixture_models(
                    development=development,
                    fixture=applicability_fixture,
                    projection=applicability,
                )
            except (ApplicabilityInputError, AttributeError, TypeError, ValueError) as exc:
                raise ValueError(str(exc) or "APPLICABILITY-INPUT-ERROR") from exc
        result = cls(
            development=development,
            interfaces=interfaces,
            development_artifact_id=artifact_id,
            development_version=version,
            finite_refinement_id="AR-FINITE",
            interface_ids=frozenset(bound_ids),
            record_ids=frozenset(record_ids),
            runtime_parameter_ids=frozenset(parameter_ids),
            applicability_schema=applicability_schema,
            applicability_manifest=applicability_manifest,
            applicability_fixture=applicability_fixture,
            integrity_baseline=integrity_baseline,
            applicability=applicability,
        )
        object.__setattr__(result, "_verification_token", _BINDING_TOKEN)
        return result

    def identities(self) -> Mapping[str, Mapping[str, str]]:
        """Return raw-Git identities only after revalidating their snapshots.

        ``RuntimeAuthorityBinding`` is a frozen dataclass, but an adapter can
        still retain an alias and use ``object.__setattr__``.  A binding token
        alone therefore cannot establish the S0 authority boundary: the
        development and registry snapshots, plus the finite projection derived
        from them, are checked again immediately before their identity leaves
        this module.
        """

        self._require_verified_projection()
        return self._raw_identities()

    def _raw_identities(self) -> Mapping[str, Mapping[str, str]]:
        identities: dict[str, Mapping[str, str]] = {
            "development": MappingProxyType(
                {
                    "commit": self.development.contract_commit,
                    "path": self.development.contract_path,
                    "blobSha256": self.development.contract_blob_sha256,
                },
            ),
            "interfaceRegistry": self.interfaces.identity(),
        }
        if self.applicability is not None:
            if (
                self.applicability_schema is None
                or self.applicability_manifest is None
                or self.applicability_fixture is None
                or self.integrity_baseline is None
            ):
                raise ValueError("runtime applicability identities are incomplete")
            identities.update(
                {
                    "applicabilitySchema": self.applicability_schema.identity(),
                    "applicabilityManifest": self.applicability_manifest.identity(),
                    "applicabilityFixture": self.applicability_fixture.identity(),
                    "integrityBaseline": self.integrity_baseline.identity(),
                },
            )
        return MappingProxyType(identities)

    def _require_verified_projection(self) -> None:
        """Reject fabricated or caller-mutated runtime authority bindings."""

        if type(self) is not RuntimeAuthorityBinding or self._verification_token is not _BINDING_TOKEN:
            raise ValueError("runtime authority binding is not verified")
        # The raw-byte/token checks deliberately happen before the finite
        # projection is reconstructed.  That prevents a token-bearing object
        # whose public identity fields were altered after factory construction
        # from being treated as a new authority.
        if type(self.development) is not ContractSnapshot:
            raise ValueError("runtime authority development snapshot is not verified")
        try:
            self.development._parsed_contract()
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError("runtime authority development snapshot is not verified") from exc
        if not _verified_source_snapshot(self.interfaces):
            raise ValueError("runtime authority interface snapshot is not verified")
        try:
            expected = RuntimeAuthorityBinding._from_verified_snapshots(
                development=self.development,
                interfaces=self.interfaces,
                applicability_schema=self.applicability_schema,
                applicability_manifest=self.applicability_manifest,
                applicability_fixture=self.applicability_fixture,
                integrity_baseline=self.integrity_baseline,
            )
        except (AttributeError, TypeError, ValueError) as exc:
            raise ValueError("runtime authority projection is not verified") from exc
        if not _same_projection(self, expected):
            raise ValueError("runtime authority projection differs from its verified snapshots")

    def named_interface_adapters(self) -> Mapping[str, Mapping[str, str]]:
        """Return the closed source-to-runtime aliases for all eight interfaces."""

        self._require_verified_projection()
        return NAMED_INTERFACE_ADAPTERS

    def validated_stop_inputs(
        self,
        *,
        applicability_context_id: str | None,
        legacy_named_645_residuals: object | None,
        model: FiniteSessionModel,
    ) -> StopInputs:
        """Derive immutable P3 inputs from a Git-bound runtime context.

        ``legacy_named_645_residuals`` exists only to reject the pre-addendum
        caller-supplied API explicitly.  No caller collection, empty or not,
        can erase a residual selected by the controlled manifest.
        """

        self._require_verified_projection()
        if legacy_named_645_residuals is not None:
            raise ValueError("APPLICABILITY-INPUT-ERROR: caller-supplied named residuals are forbidden")
        if self.applicability is None:
            if applicability_context_id is not None:
                raise ValueError("APPLICABILITY-INPUT-ERROR: no Git-bound runtime applicability manifest is present")
            return StopInputs(
                applicability_status="P3-UNAVAILABLE",
                context_id=None,
                applicability_input_identity=None,
                named_645_residuals=(),
            )
        if not verified_finite_session_model(model):
            raise ValueError("APPLICABILITY-INPUT-ERROR: runtime model is not a verified finite model")
        try:
            resolution = self.applicability.resolve(
                context_id=applicability_context_id,
                model_source_json=model._source_json,
                action_ids=tuple(sorted(model.actions)),
            )
        except (ApplicabilityInputError, AttributeError, TypeError, ValueError) as exc:
            raise ValueError(str(exc) or "APPLICABILITY-INPUT-ERROR") from exc
        return StopInputs(
            applicability_status=resolution.status,
            context_id=resolution.context_id,
            applicability_input_identity=resolution.input_identity,
            named_645_residuals=tuple(
                Named645Residual(
                    requirement_id=row.requirement_id,
                    dependency_id=row.dependency_id,
                    source_unit_id=row.source_unit_id,
                    contract_id=row.contract_id,
                    context_id=row.context_id,
                    input_identity=row.input_identity,
                )
                for row in resolution.residuals
            ),
        )


def _validate_applicability_fixture_models(
    *,
    development: ContractSnapshot,
    fixture: SourceSnapshot,
    projection: RuntimeApplicabilityProjection,
) -> None:
    """Require every declared fixture model to be an executable finite model.

    The applicability schema deliberately owns the public manifest/reference
    vocabulary.  The runtime model grammar is already a separate closed
    contract implemented by :class:`FiniteSessionModel`; validating each
    fixture model through that parser prevents a structurally loose JSON
    object from becoming a deferred or hidden applicability input.  The
    check happens while the Git snapshots are still being bound, before a
    session can select a context or derive a P3 residual.
    """

    try:
        fixture_object = fixture.json_object()
        rows = fixture_object.get("models")
        if not isinstance(rows, list) or not rows:
            raise ValueError("fixture has no finite model rows")
        parsed_sources: set[bytes] = set()
        for row in rows:
            if not isinstance(row, Mapping) or set(row) != {"id", "algorithmModel"}:
                raise ValueError("fixture model row is malformed")
            if type(row.get("id")) is not str or not row["id"]:
                raise ValueError("fixture model identity is invalid")
            algorithm = row.get("algorithmModel")
            if not isinstance(algorithm, Mapping):
                raise ValueError("fixture model algorithm is malformed")
            public_model = algorithm.get("model")
            if not isinstance(public_model, Mapping) or set(public_model) != {
                "stateIds", "clockIds", "typedDomains",
            }:
                raise ValueError("fixture model public domain is malformed")
            state_ids = public_model.get("stateIds")
            clock_ids = public_model.get("clockIds")
            typed_domains = public_model.get("typedDomains")
            if (
                not isinstance(state_ids, list)
                or not isinstance(clock_ids, list)
                or not isinstance(typed_domains, Mapping)
                or any(type(item) is not str or not item for item in state_ids + clock_ids)
                or any(
                    type(name) is not str
                    or not name
                    or not isinstance(domain, list)
                    or any(type(member) is not str or not member for member in domain)
                    for name, domain in typed_domains.items()
                )
            ):
                raise ValueError("fixture model public domain is malformed")
            uncertainty = algorithm.get("uncertainty")
            if not isinstance(uncertainty, Mapping):
                raise ValueError("fixture model uncertainty is malformed")
            projection_clock = uncertainty.get("clockId")
            if (
                type(projection_clock) is not str
                or not projection_clock
                or projection_clock not in clock_ids
            ):
                raise ValueError("fixture model uncertainty clock is malformed")
            context = ModelContext.build(
                snapshot=development,
                model={
                    "stateIds": set(state_ids),
                    "clockIds": set(clock_ids),
                    "typedDomains": {
                        name: set(domain)
                        for name, domain in typed_domains.items()
                    },
                },
                projection_clock=projection_clock,
            )
            parsed = FiniteSessionModel.from_mapping(context=context, value=algorithm)
            parsed_sources.add(parsed._source_json)
        if not parsed_sources or any(
            context.model_source_json not in parsed_sources
            for context in projection.contexts.values()
        ):
            raise ValueError("fixture model binding differs from applicability contexts")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        message = str(exc) or type(exc).__name__
        raise ApplicabilityInputError(f"finite fixture model is invalid: {message}") from exc


def _verified_source_snapshot(value: object) -> bool:
    """Return whether a source snapshot still names its verified raw bytes."""

    if type(value) is not SourceSnapshot or value._verification_token is not _SOURCE_SNAPSHOT_TOKEN:
        return False
    try:
        path = _safe_repository_path(value.path)
        commit = _validate_commit(value.commit)
    except (AttributeError, TypeError, ValueError):
        return False
    return (
        path == value.path
        and commit == value.commit
        and type(value.blob_sha256) is str
        and type(value._content) is bytes
        and sha256(value._content).hexdigest() == value.blob_sha256
        and type(value._binding_sha256) is str
        and value._binding_sha256 == _source_snapshot_binding_digest(value)
    )


def _source_snapshot_binding_digest(value: SourceSnapshot) -> str:
    """Bind a source identity to the raw Git bytes issued by the factory."""

    return sha256(repr((value.commit, value.path, value.blob_sha256)).encode("utf-8")).hexdigest()


def _same_projection(
    actual: RuntimeAuthorityBinding,
    expected: RuntimeAuthorityBinding,
) -> bool:
    """Compare the finite binding fields against a fresh verified projection."""

    return (
        type(actual.development_artifact_id) is str
        and type(actual.development_version) is str
        and type(actual.finite_refinement_id) is str
        and type(actual.interface_ids) is frozenset
        and type(actual.record_ids) is frozenset
        and type(actual.runtime_parameter_ids) is frozenset
        and all(type(item) is str for item in actual.interface_ids)
        and all(type(item) is str for item in actual.record_ids)
        and all(type(item) is str for item in actual.runtime_parameter_ids)
        and actual.development_artifact_id == expected.development_artifact_id
        and actual.development_version == expected.development_version
        and actual.finite_refinement_id == expected.finite_refinement_id
        and actual.interface_ids == expected.interface_ids
        and actual.record_ids == expected.record_ids
        and actual.runtime_parameter_ids == expected.runtime_parameter_ids
        and _same_applicability_projection(actual, expected)
    )


def _same_applicability_projection(
    actual: RuntimeAuthorityBinding,
    expected: RuntimeAuthorityBinding,
) -> bool:
    """Compare the optional four-source runtime applicability projection."""

    actual_sources = (
        actual.applicability_schema,
        actual.applicability_manifest,
        actual.applicability_fixture,
        actual.integrity_baseline,
    )
    expected_sources = (
        expected.applicability_schema,
        expected.applicability_manifest,
        expected.applicability_fixture,
        expected.integrity_baseline,
    )
    if any(value is None for value in actual_sources) != any(value is None for value in expected_sources):
        return False
    if all(value is None for value in actual_sources + expected_sources):
        return actual.applicability is None and expected.applicability is None
    if any(value is None for value in actual_sources + expected_sources):
        return False
    if type(actual.applicability) is not RuntimeApplicabilityProjection or type(expected.applicability) is not RuntimeApplicabilityProjection:
        return False
    try:
        return (
            actual.applicability.identity == expected.applicability.identity
            and actual.applicability.source_identities == expected.applicability.source_identities
            and actual.applicability.contexts == expected.applicability.contexts
            and all(_verified_source_snapshot(value) for value in actual_sources)
        )
    except (AttributeError, TypeError, ValueError):
        return False


def _unique_string_ids(
    values: list[Any], field_name: str, label: str,
) -> frozenset[str]:
    ids: list[str] = []
    for value in values:
        if not isinstance(value, Mapping):
            raise ValueError(f"{label} entry is invalid")
        identifier = value.get(field_name)
        if not isinstance(identifier, str) or not identifier:
            raise ValueError(f"{label} has an invalid identifier")
        ids.append(identifier)
    if len(ids) != len(set(ids)):
        raise ValueError(f"{label} has duplicate identifiers")
    return frozenset(ids)
