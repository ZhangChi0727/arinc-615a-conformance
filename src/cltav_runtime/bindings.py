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

from .kernel import ContractSnapshot


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

    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("controlled source path must be a nonempty POSIX path")
    if PureWindowsPath(value).is_absolute() or PurePosixPath(value).is_absolute():
        raise ValueError("controlled source path must be repository-relative")
    path = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("controlled source path contains an unsafe component")
    return path.as_posix()


def _validate_commit(value: str) -> str:
    if (
        not isinstance(value, str)
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
        object.__setattr__(snapshot, "_verification_token", _SOURCE_SNAPSHOT_TOKEN)
        return snapshot

    def json_object(self) -> Mapping[str, Any]:
        if self._verification_token is not _SOURCE_SNAPSHOT_TOKEN:
            raise ValueError("controlled source snapshot is not verified")
        try:
            value = json.loads(self._content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("controlled source object must be UTF-8 JSON") from exc
        if not isinstance(value, Mapping):
            raise ValueError("controlled source root must be an object")
        return value

    def identity(self) -> Mapping[str, str]:
        if self._verification_token is not _SOURCE_SNAPSHOT_TOKEN:
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
        return cls._from_verified_snapshots(development=development, interfaces=interfaces)

    @classmethod
    def _from_verified_snapshots(
        cls, *, development: ContractSnapshot, interfaces: SourceSnapshot,
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
        result = cls(
            development=development,
            interfaces=interfaces,
            development_artifact_id=artifact_id,
            development_version=version,
            finite_refinement_id="AR-FINITE",
            interface_ids=frozenset(bound_ids),
            record_ids=frozenset(record_ids),
            runtime_parameter_ids=frozenset(parameter_ids),
        )
        object.__setattr__(result, "_verification_token", _BINDING_TOKEN)
        return result

    def identities(self) -> Mapping[str, Mapping[str, str]]:
        if self._verification_token is not _BINDING_TOKEN:
            raise ValueError("runtime authority binding is not verified")
        return MappingProxyType(
            {
                "development": MappingProxyType(
                    {
                        "commit": self.development.contract_commit,
                        "path": self.development.contract_path,
                        "blobSha256": self.development.contract_blob_sha256,
                    },
                ),
                "interfaceRegistry": self.interfaces.identity(),
            },
        )

    def named_interface_adapters(self) -> Mapping[str, Mapping[str, str]]:
        """Return the closed source-to-runtime aliases for all eight interfaces."""

        if self._verification_token is not _BINDING_TOKEN:
            raise ValueError("runtime authority binding is not verified")
        return NAMED_INTERFACE_ADAPTERS


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
