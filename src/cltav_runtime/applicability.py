"""Closed finite applicability projection for B/C-2C stopping.

This module deliberately does *not* decide whether an ARINC 645 obligation is
true, false, qualified, or satisfied.  It only turns a separately controlled,
Git-bound synthetic-runtime task into an unresolved named dependency while the
runtime capability remains ``NOT-ESTABLISHED``.  The input is intentionally
finite and typed: it has no predicate language, no ``eval`` path, no caller
``applicable`` flag, and no access to evaluator truth or private environment
state.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


_IDENTITY_FIELDS = ("commit", "path", "blobSha256")
_INTEGRITY_DEPENDENCY = "DEP-INTEGRITY-RUNTIME"
_INTEGRITY_REQUIREMENTS = frozenset(
    {
        "CRS-M1-00076",
        "CRS-M1-00082",
        "CRS-M1-00085",
        "CRS-M1-00086",
        "CRS-M1-00087",
        "CRS-M1-00109",
    },
)


class ApplicabilityInputError(ValueError):
    """A named rejection of an invalid finite applicability input."""

    def __init__(self, message: str) -> None:
        super().__init__(f"APPLICABILITY-INPUT-ERROR: {message}")


def _fail(message: str) -> None:
    raise ApplicabilityInputError(message)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest(value: object) -> str:
    return sha256(repr(value).encode("utf-8")).hexdigest()


def _nonblank(value: object, label: str) -> str:
    if type(value) is not str or not value.strip():
        _fail(f"{label} is not a nonblank exact string")
    return value


def _exact_mapping(value: object, fields: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != fields:
        _fail(f"{label} has unknown or missing fields")
    return value


def _json_object(raw: bytes, label: str) -> Mapping[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ApplicabilityInputError(f"{label} is not UTF-8 JSON") from exc
    if not isinstance(value, Mapping):
        _fail(f"{label} root is not an object")
    return value


def _validate_document(schema: Mapping[str, Any], value: Mapping[str, Any], label: str) -> None:
    try:
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(value), key=lambda item: (list(item.absolute_path), item.message))
    except (AttributeError, SchemaError, TypeError, ValueError) as exc:
        raise ApplicabilityInputError(f"{label} schema cannot be applied") from exc
    if errors:
        first = errors[0]
        path = ".".join(str(part) for part in first.absolute_path) or "$"
        _fail(f"{label} violates closed schema at {path}: {first.message}")


def _identity(value: object, label: str) -> Mapping[str, str]:
    if not isinstance(value, Mapping) or set(value) != set(_IDENTITY_FIELDS):
        _fail(f"{label} identity is malformed")
    fields = {field: value.get(field) for field in _IDENTITY_FIELDS}
    if any(type(item) is not str or not item for item in fields.values()):
        _fail(f"{label} identity is incomplete")
    return MappingProxyType(fields)


def _declared_source_identity(value: object, actual: Mapping[str, str], label: str) -> None:
    declared = _exact_mapping(value, {"path", "blobSha256"}, label)
    path = _nonblank(declared.get("path"), f"{label} path")
    digest = _nonblank(declared.get("blobSha256"), f"{label} blob hash")
    if path != actual["path"] or digest != actual["blobSha256"]:
        _fail(f"{label} does not match the verified Git source identity")


def _rows_by_id(value: object, label: str) -> Mapping[str, Mapping[str, Any]]:
    if not isinstance(value, list) or not value:
        _fail(f"{label} is not a nonempty list")
    rows: dict[str, Mapping[str, Any]] = {}
    for row in value:
        if not isinstance(row, Mapping):
            _fail(f"{label} has a non-object row")
        identifier = _nonblank(row.get("id"), f"{label} identifier")
        if identifier in rows:
            _fail(f"{label} repeats {identifier!r}")
        rows[identifier] = row
    return MappingProxyType(rows)


def _hex_bytes(value: object, label: str) -> None:
    text = _nonblank(value, label)
    if len(text) % 2 or any(character not in "0123456789abcdefABCDEF" for character in text):
        _fail(f"{label} is not parseable hexadecimal bytes")


def _typed_bool(value: object, label: str, *, nullable: bool = False) -> bool | None:
    if value is None and nullable:
        return None
    if type(value) is not bool:
        _fail(f"{label} is not an exact boolean")
    return value


def _source_rows(development: Mapping[str, Any], baseline: Mapping[str, Any]) -> Mapping[str, tuple[str, str, str, str]]:
    dependencies = development.get("implementationDependencies")
    if not isinstance(dependencies, list):
        _fail("development authority has no implementation dependencies")
    matches = [row for row in dependencies if isinstance(row, Mapping) and row.get("id") == _INTEGRITY_DEPENDENCY]
    if len(matches) != 1:
        _fail("development authority lacks one integrity dependency")
    dependency = matches[0]
    if dependency.get("runtimeStatus") != "NOT-ESTABLISHED":
        _fail("integrity runtime status is not NOT-ESTABLISHED")
    bindings = dependency.get("sourceBindings")
    obligations = baseline.get("obligations")
    if not isinstance(bindings, list) or not isinstance(obligations, list):
        _fail("source authorities have no integrity binding rows")
    development_rows: dict[str, tuple[str, str, str, str]] = {}
    for row in bindings:
        if not isinstance(row, Mapping):
            _fail("development integrity source binding is invalid")
        requirement = _nonblank(row.get("requirementId"), "development requirement identity")
        source_unit = _nonblank(row.get("sourceUnitId"), "development source-unit identity")
        contract = _nonblank(row.get("contractId"), "development contract identity")
        if requirement in development_rows:
            _fail("development integrity source bindings repeat a requirement")
        development_rows[requirement] = (requirement, _INTEGRITY_DEPENDENCY, source_unit, contract)
    baseline_rows: dict[str, tuple[str, str, str, str]] = {}
    for row in obligations:
        if not isinstance(row, Mapping):
            _fail("integrity baseline obligation is invalid")
        requirement = _nonblank(row.get("requirementId"), "baseline requirement identity")
        source_unit = _nonblank(row.get("sourceUnitId"), "baseline source-unit identity")
        contract = _nonblank(row.get("contractId"), "baseline contract identity")
        if requirement in baseline_rows:
            _fail("integrity baseline repeats a requirement")
        baseline_rows[requirement] = (requirement, _INTEGRITY_DEPENDENCY, source_unit, contract)
    if set(development_rows) != _INTEGRITY_REQUIREMENTS or development_rows != baseline_rows:
        _fail("integrity source authorities do not provide the controlled six-row baseline")
    return MappingProxyType(development_rows)


@dataclass(frozen=True)
class ApplicabilityResidual:
    """One fully source-bound unresolved runtime task."""

    requirement_id: str
    dependency_id: str
    source_unit_id: str
    contract_id: str
    context_id: str
    input_identity: str


@dataclass(frozen=True)
class ResolvedApplicability:
    """Frozen P3 input derived from a selected controlled runtime context."""

    context_id: str
    input_identity: str
    status: str
    residuals: tuple[ApplicabilityResidual, ...]


@dataclass(frozen=True)
class _ContextProjection:
    context_id: str
    model_source_json: bytes
    action_ids: tuple[str, ...]
    status: str
    residual: ApplicabilityResidual | None


@dataclass(frozen=True)
class RuntimeApplicabilityProjection:
    """Immutable, Git-derived finite applicability projection.

    The only selector is a controlled context identifier.  Display scenario and
    service strings are intentionally validated as metadata but are not read
    by :meth:`resolve` when deciding whether a residual is active.
    """

    identity: str
    source_identities: Mapping[str, Mapping[str, str]]
    contexts: Mapping[str, _ContextProjection]

    def resolve(
        self,
        *,
        context_id: object,
        model_source_json: object,
        action_ids: object,
    ) -> ResolvedApplicability:
        identifier = _nonblank(context_id, "runtime applicability context identity")
        context = self.contexts.get(identifier)
        if context is None:
            _fail("runtime applicability context is not declared by the frozen manifest")
        if type(model_source_json) is not bytes or model_source_json != context.model_source_json:
            _fail("runtime model does not match the context-bound fixture model")
        if type(action_ids) is not tuple or action_ids != context.action_ids:
            _fail("runtime action domain does not match the context-bound fixture domain")
        return ResolvedApplicability(
            context_id=context.context_id,
            input_identity=context.residual.input_identity if context.residual is not None else _digest(
                (self.identity, context.context_id, context.status),
            ),
            status=context.status,
            residuals=() if context.residual is None else (context.residual,),
        )


def _fixture_indexes(fixture: Mapping[str, Any]) -> tuple[Mapping[str, Mapping[str, Any]], Mapping[str, Mapping[str, Any]]]:
    models = _rows_by_id(fixture.get("models"), "runtime fixture models")
    references = _exact_mapping(
        fixture.get("references"),
        {
            "receivers", "options", "supportDeclarations", "optionSelections", "byteBindings", "files",
            "algorithmConfigurations", "checkValues", "comparisonDeclarations", "operations",
            "events", "calculationIntervals", "statusStreams", "observationRanges", "methodOnlyReferences",
        },
        "runtime fixture references",
    )
    index: dict[str, Mapping[str, Any]] = {}
    for label, rows in references.items():
        for identifier, row in _rows_by_id(rows, f"runtime fixture {label}").items():
            if identifier in index:
                _fail(f"runtime fixture reference identity {identifier!r} is not globally unique")
            index[identifier] = row
    for model_id, model in models.items():
        if set(model) != {"id", "algorithmModel"} or not isinstance(model.get("algorithmModel"), Mapping):
            _fail(f"runtime fixture model {model_id} is malformed")
    return models, MappingProxyType(index)


def _reference(index: Mapping[str, Mapping[str, Any]], identifier: object, label: str) -> Mapping[str, Any]:
    return index.get(_nonblank(identifier, label)) or _missing_reference(label)


def _missing_reference(label: str) -> Mapping[str, Any]:
    _fail(f"{label} does not resolve in the finite runtime fixture")
    raise AssertionError("unreachable")  # pragma: no cover - satisfies type checkers


def _require_kind(row: Mapping[str, Any], *, expected: str, label: str) -> None:
    if row.get("kind") != expected:
        _fail(f"{label} has the wrong finite fixture kind")


def _validate_model_context(
    *,
    raw: Mapping[str, Any],
    models: Mapping[str, Mapping[str, Any]],
    context_id: str,
) -> tuple[bytes, tuple[str, ...]]:
    model_id = _nonblank(raw.get("modelId"), f"{context_id} model identity")
    model = models.get(model_id)
    if model is None:
        _fail(f"{context_id} references an unknown fixture model")
    algorithm = model["algorithmModel"]
    assert isinstance(algorithm, Mapping)
    actions = algorithm.get("actions")
    if not isinstance(actions, list) or not actions:
        _fail(f"{context_id} fixture model has no finite action domain")
    actual_ids: list[str] = []
    for action in actions:
        if not isinstance(action, Mapping):
            _fail(f"{context_id} fixture action is invalid")
        actual_ids.append(_nonblank(action.get("id"), f"{context_id} fixture action identity"))
    if len(actual_ids) != len(set(actual_ids)):
        _fail(f"{context_id} fixture model repeats an action identity")
    supplied = raw.get("actionIds")
    if not isinstance(supplied, list) or not supplied or any(type(item) is not str or not item for item in supplied):
        _fail(f"{context_id} action-domain binding is invalid")
    if len(supplied) != len(set(supplied)) or tuple(sorted(supplied)) != tuple(sorted(actual_ids)):
        _fail(f"{context_id} action-domain binding differs from its fixture model")
    return _canonical_bytes(algorithm), tuple(sorted(actual_ids))


def _valid_reference_ids(index: Mapping[str, Mapping[str, Any]], refs: object, context_id: str) -> None:
    if not isinstance(refs, list) or not refs or any(type(item) is not str or not item for item in refs):
        _fail(f"{context_id} reason references are invalid")
    if len(refs) != len(set(refs)) or any(item not in index for item in refs):
        _fail(f"{context_id} reason references do not resolve in the finite fixture")


def _support_context(
    *, requirement_id: str, values: Mapping[str, Any], index: Mapping[str, Mapping[str, Any]],
) -> bool:
    expected_service = "INFORMATION" if requirement_id == "CRS-M1-00076" else "UPLOAD"
    fields = {
        "receiverId", "optionId", "optionSelected", "selectionDeclarationId",
        "supportDeclarationId", "protectedBytesId",
    }
    _exact_mapping(values, fields, f"{requirement_id} public inputs")
    receiver = _reference(index, values.get("receiverId"), f"{requirement_id} receiver")
    option = _reference(index, values.get("optionId"), f"{requirement_id} option")
    selection = _reference(index, values.get("selectionDeclarationId"), f"{requirement_id} option selection")
    declaration = _reference(index, values.get("supportDeclarationId"), f"{requirement_id} support declaration")
    protected = _reference(index, values.get("protectedBytesId"), f"{requirement_id} protected bytes")
    _require_kind(receiver, expected="RECEIVER", label=f"{requirement_id} receiver")
    _require_kind(option, expected="OPTION", label=f"{requirement_id} option")
    _require_kind(selection, expected="OPTION-SELECTION", label=f"{requirement_id} option selection")
    _require_kind(declaration, expected="SUPPORT-DECLARATION", label=f"{requirement_id} support declaration")
    _require_kind(protected, expected="PROTECTED-BYTES", label=f"{requirement_id} protected bytes")
    if (
        receiver.get("service") != expected_service
        or receiver.get("role") != "RECEIVER"
        or option.get("service") != expected_service
        or option.get("purpose") != "INTEGRITY"
        or protected.get("service") != expected_service
    ):
        _fail(f"{requirement_id} public references use the wrong service domain")
    if (
        selection.get("receiverId") != receiver.get("id")
        or selection.get("optionId") != option.get("id")
        or declaration.get("receiverId") != receiver.get("id")
        or declaration.get("optionId") != option.get("id")
    ):
        _fail(f"{requirement_id} support declaration is not bound to its receiver and option")
    selected = _typed_bool(values.get("optionSelected"), f"{requirement_id} optionSelected")
    if selection.get("selected") is not selected:
        _fail(f"{requirement_id} option selection is not bound to its declared public selection")
    _nonblank(selection.get("source"), f"{requirement_id} option selection source")
    _nonblank(declaration.get("source"), f"{requirement_id} support declaration source")
    _hex_bytes(protected.get("hex"), f"{requirement_id} protected bytes")
    support = _typed_bool(declaration.get("declaredSupport"), f"{requirement_id} receiver support", nullable=True)
    if selected is False:
        return False
    if support is not True:
        _fail(f"{requirement_id} selected option lacks a true parseable receiver-support declaration")
    return True


def _integrity_file(
    row: Mapping[str, Any], *, label: str, index: Mapping[str, Mapping[str, Any]], expected_service: str = "UPLOAD",
) -> Mapping[str, Any]:
    _require_kind(row, expected="FILE", label=label)
    bytes_row = _reference(index, row.get("bytesId"), f"{label} bytes")
    _require_kind(bytes_row, expected="PROTECTED-BYTES", label=f"{label} bytes")
    if bytes_row.get("service") != expected_service:
        _fail(f"{label} bytes are outside the required {expected_service} service domain")
    _hex_bytes(bytes_row.get("hex"), f"{label} bytes")
    return bytes_row


def _final_image_context(values: Mapping[str, Any], index: Mapping[str, Mapping[str, Any]]) -> bool:
    fields = {
        "finalImageFileId", "lspFileId", "orderedBytesId", "algorithmConfigurationId",
        "finalImageCheckValueId", "lspCheckValueId",
    }
    _exact_mapping(values, fields, "CRS-M1-00085 public inputs")
    image = _reference(index, values.get("finalImageFileId"), "00085 final image")
    lsp = _reference(index, values.get("lspFileId"), "00085 LSP")
    ordered = _reference(index, values.get("orderedBytesId"), "00085 ordered bytes")
    algorithm = _reference(index, values.get("algorithmConfigurationId"), "00085 algorithm/configuration")
    image_check = _reference(index, values.get("finalImageCheckValueId"), "00085 final-image check field")
    lsp_check = _reference(index, values.get("lspCheckValueId"), "00085 LSP check field")
    image_bytes = _integrity_file(image, label="00085 final image", index=index)
    _integrity_file(lsp, label="00085 LSP", index=index)
    _require_kind(ordered, expected="PROTECTED-BYTES", label="00085 ordered bytes")
    _require_kind(algorithm, expected="ALGORITHM-CONFIGURATION", label="00085 algorithm/configuration")
    _require_kind(image_check, expected="CHECK-VALUE", label="00085 final-image check field")
    _require_kind(lsp_check, expected="CHECK-VALUE", label="00085 LSP check field")
    if (
        image.get("id") == lsp.get("id")
        or ordered.get("service") != "UPLOAD"
        or ordered.get("id") != image_bytes.get("id")
        or image_check.get("fileId") != image.get("id")
        or lsp_check.get("fileId") != lsp.get("id")
        or image_check.get("algorithmConfigurationId") != algorithm.get("id")
        or lsp_check.get("algorithmConfigurationId") != algorithm.get("id")
    ):
        _fail("00085 public references do not bind image/LSP bytes and check fields")
    _hex_bytes(ordered.get("hex"), "00085 ordered bytes")
    _nonblank(algorithm.get("algorithmId"), "00085 algorithm identity")
    _nonblank(algorithm.get("configurationId"), "00085 configuration identity")
    _nonblank(image_check.get("source"), "00085 final-image check source")
    _nonblank(lsp_check.get("source"), "00085 LSP check source")
    return True


def _comparison_context(values: Mapping[str, Any], index: Mapping[str, Mapping[str, Any]]) -> bool:
    fields = {
        "comparisonSelected", "comparisonDeclarationId", "oldFileId", "newFileId",
        "oldCheckValueId", "newCheckValueId",
    }
    _exact_mapping(values, fields, "CRS-M1-00086 public inputs")
    declaration = _reference(index, values.get("comparisonDeclarationId"), "00086 comparison declaration")
    old = _reference(index, values.get("oldFileId"), "00086 old file")
    new = _reference(index, values.get("newFileId"), "00086 new file")
    old_value = _reference(index, values.get("oldCheckValueId"), "00086 old check value")
    new_value = _reference(index, values.get("newCheckValueId"), "00086 new check value")
    _require_kind(declaration, expected="COMPARISON-DECLARATION", label="00086 comparison declaration")
    _integrity_file(old, label="00086 old file", index=index)
    _integrity_file(new, label="00086 new file", index=index)
    _require_kind(old_value, expected="CHECK-VALUE", label="00086 old check value")
    _require_kind(new_value, expected="CHECK-VALUE", label="00086 new check value")
    old_algorithm = _reference(
        index,
        old_value.get("algorithmConfigurationId"),
        "00086 old check-value algorithm/configuration",
    )
    new_algorithm = _reference(
        index,
        new_value.get("algorithmConfigurationId"),
        "00086 new check-value algorithm/configuration",
    )
    _require_kind(
        old_algorithm,
        expected="ALGORITHM-CONFIGURATION",
        label="00086 old check-value algorithm/configuration",
    )
    _require_kind(
        new_algorithm,
        expected="ALGORITHM-CONFIGURATION",
        label="00086 new check-value algorithm/configuration",
    )
    _nonblank(old_algorithm.get("algorithmId"), "00086 old check-value algorithm identity")
    _nonblank(old_algorithm.get("configurationId"), "00086 old check-value configuration identity")
    _nonblank(new_algorithm.get("algorithmId"), "00086 new check-value algorithm identity")
    _nonblank(new_algorithm.get("configurationId"), "00086 new check-value configuration identity")
    selected = _typed_bool(values.get("comparisonSelected"), "00086 comparisonSelected")
    if declaration.get("selected") is not selected:
        _fail("00086 comparison selection is not bound to its declaration")
    if declaration.get("oldFileId") != old.get("id") or declaration.get("newFileId") != new.get("id"):
        _fail("00086 comparison declaration is not bound to the consumed old/new files")
    _nonblank(declaration.get("source"), "00086 comparison declaration source")
    _nonblank(old_value.get("source"), "00086 old check-value source")
    _nonblank(new_value.get("source"), "00086 new check-value source")
    if selected is False:
        return False
    if old.get("id") == new.get("id") or old_value.get("fileId") != old.get("id") or new_value.get("fileId") != new.get("id"):
        _fail("00086 selected comparison lacks distinct correctly-bound files and values")
    return True


def _same_part_context(values: Mapping[str, Any], index: Mapping[str, Mapping[str, Any]]) -> bool:
    fields = {"fileAId", "fileBId", "algorithmConfigurationId", "checkValueAId", "checkValueBId"}
    _exact_mapping(values, fields, "CRS-M1-00087 public inputs")
    first = _reference(index, values.get("fileAId"), "00087 first file")
    second = _reference(index, values.get("fileBId"), "00087 second file")
    algorithm = _reference(index, values.get("algorithmConfigurationId"), "00087 algorithm/configuration")
    first_value = _reference(index, values.get("checkValueAId"), "00087 first check value")
    second_value = _reference(index, values.get("checkValueBId"), "00087 second check value")
    _integrity_file(first, label="00087 first file", index=index)
    _integrity_file(second, label="00087 second file", index=index)
    _require_kind(algorithm, expected="ALGORITHM-CONFIGURATION", label="00087 algorithm/configuration")
    _require_kind(first_value, expected="CHECK-VALUE", label="00087 first check value")
    _require_kind(second_value, expected="CHECK-VALUE", label="00087 second check value")
    if first.get("id") == second.get("id"):
        _fail("00087 requires two distinct file identities")
    first_part = _nonblank(first.get("partNumber"), "00087 first part number")
    second_part = _nonblank(second.get("partNumber"), "00087 second part number")
    if first_part != second_part:
        _fail("00087 finite context lacks a same-part-number relation")
    _nonblank(first.get("partNumberSource"), "00087 first part-number source")
    _nonblank(second.get("partNumberSource"), "00087 second part-number source")
    _nonblank(algorithm.get("algorithmId"), "00087 algorithm identity")
    _nonblank(algorithm.get("configurationId"), "00087 configuration identity")
    if (
        first_value.get("fileId") != first.get("id")
        or second_value.get("fileId") != second.get("id")
        or first_value.get("algorithmConfigurationId") != algorithm.get("id")
        or second_value.get("algorithmConfigurationId") != algorithm.get("id")
    ):
        _fail("00087 check-value sources are not bound to their distinct files")
    _nonblank(first_value.get("source"), "00087 first check-value source")
    _nonblank(second_value.get("source"), "00087 second check-value source")
    return True


def _status_context(values: Mapping[str, Any], index: Mapping[str, Mapping[str, Any]]) -> bool:
    fields = {
        "operationId", "finalDataEventId", "calculationIntervalId", "statusStreamId",
        "observationRangeId", "observationComplete",
    }
    _exact_mapping(values, fields, "CRS-M1-00109 public inputs")
    operation = _reference(index, values.get("operationId"), "00109 operation")
    final_data = _reference(index, values.get("finalDataEventId"), "00109 FINAL-DATA event")
    interval = _reference(index, values.get("calculationIntervalId"), "00109 calculation interval")
    stream = _reference(index, values.get("statusStreamId"), "00109 status stream")
    observation = _reference(index, values.get("observationRangeId"), "00109 observation range")
    _require_kind(operation, expected="OPERATION", label="00109 operation")
    _require_kind(final_data, expected="EVENT", label="00109 FINAL-DATA event")
    _require_kind(interval, expected="CALCULATION-INTERVAL", label="00109 calculation interval")
    _require_kind(stream, expected="STATUS-STREAM", label="00109 status stream")
    _require_kind(observation, expected="OBSERVATION-RANGE", label="00109 observation range")
    operation_id = operation.get("id")
    if (
        operation.get("service") != "UPLOAD"
        or final_data.get("operationId") != operation_id
        or final_data.get("eventKind") != "FINAL-DATA"
        or interval.get("operationId") != operation_id
        or interval.get("state") != "CALCULATION-IN-PROGRESS"
        or stream.get("operationId") != operation_id
        or observation.get("operationId") != operation_id
        or observation.get("scope") != "FINITE-SPECIFICATION-WITNESS-NOT-PROTOCOL-FREQUENCY"
    ):
        _fail("00109 public references do not describe one finite calculation operation")
    final_at = final_data.get("at")
    interval_start = interval.get("start")
    interval_end = interval.get("end")
    if (
        type(final_at) is not int
        or type(interval_start) is not int
        or type(interval_end) is not int
        or interval_start > interval_end
        or final_at > interval_start
    ):
        _fail("00109 calculation interval is invalid")
    _nonblank(interval.get("source"), "00109 calculation interval source")
    event_ids = stream.get("eventIds")
    point_ids = observation.get("observationEventIds")
    if (
        not isinstance(event_ids, list)
        or not isinstance(point_ids, list)
        or len(event_ids) != len(set(event_ids))
        or len(point_ids) != len(set(point_ids))
        or not set(point_ids) <= set(event_ids)
        or final_data.get("id") in event_ids
    ):
        _fail("00109 status/observation references are incomplete")
    status_ticks: dict[str, int] = {}
    for identifier in event_ids:
        event = _reference(index, identifier, "00109 status observation event")
        _require_kind(event, expected="EVENT", label="00109 status observation event")
        event_at = event.get("at")
        if (
            event.get("operationId") != operation_id
            or event.get("eventKind") != "STATUS"
            or type(event_at) is not int
            or event_at <= final_at
            or event_at < interval_start
            or event_at > interval_end
        ):
            _fail("00109 status/observation event is not in the bound operation stream")
        status_ticks[identifier] = event_at
    if tuple(status_ticks) != tuple(sorted(status_ticks, key=lambda item: (status_ticks[item], item))):
        _fail("00109 status stream is not ordered after FINAL-DATA")
    _typed_bool(values.get("observationComplete"), "00109 observationComplete")
    # Completion is deliberately not an activation gate: an incomplete public
    # observation leaves the named unresolved task active rather than making
    # it non-applicable.
    return True


def _task_active(requirement_id: str, values: Mapping[str, Any], index: Mapping[str, Mapping[str, Any]]) -> bool:
    if requirement_id in {"CRS-M1-00076", "CRS-M1-00082"}:
        return _support_context(requirement_id=requirement_id, values=values, index=index)
    if requirement_id == "CRS-M1-00085":
        return _final_image_context(values, index)
    if requirement_id == "CRS-M1-00086":
        return _comparison_context(values, index)
    if requirement_id == "CRS-M1-00087":
        return _same_part_context(values, index)
    if requirement_id == "CRS-M1-00109":
        return _status_context(values, index)
    _fail("finite applicability task has an unsupported requirement identity")
    raise AssertionError("unreachable")  # pragma: no cover


def _exact_reason_references(
    *,
    supplied: object,
    expected: set[str],
    index: Mapping[str, Mapping[str, Any]],
    context_id: str,
) -> None:
    """Require the review-facing basis list to name every consumed input.

    ``reasonRefs`` is not an independent eligibility selector.  It is a
    traceable rendering of the typed fields already consumed by one finite
    context, so a valid but unrelated fixture identifier cannot make a task
    look sourced while hiding its actual input basis.
    """

    _valid_reference_ids(index, supplied, context_id)
    assert isinstance(supplied, list)  # established by _valid_reference_ids
    if set(supplied) != expected:
        _fail(f"{context_id} reason references do not exactly cover its consumed public inputs")


def _task_reason_reference_ids(requirement_id: str, values: Mapping[str, Any]) -> set[str]:
    """Return the reference identities that one typed task actually reads."""

    fields_by_requirement = {
        "CRS-M1-00076": {
            "receiverId", "optionId", "selectionDeclarationId", "supportDeclarationId", "protectedBytesId",
        },
        "CRS-M1-00082": {
            "receiverId", "optionId", "selectionDeclarationId", "supportDeclarationId", "protectedBytesId",
        },
        "CRS-M1-00085": {
            "finalImageFileId", "lspFileId", "orderedBytesId", "algorithmConfigurationId",
            "finalImageCheckValueId", "lspCheckValueId",
        },
        "CRS-M1-00086": {
            "comparisonDeclarationId", "oldFileId", "newFileId", "oldCheckValueId", "newCheckValueId",
        },
        "CRS-M1-00087": {
            "fileAId", "fileBId", "algorithmConfigurationId", "checkValueAId", "checkValueBId",
        },
        "CRS-M1-00109": {
            "operationId", "finalDataEventId", "calculationIntervalId", "statusStreamId", "observationRangeId",
        },
    }
    fields = fields_by_requirement.get(requirement_id)
    if fields is None:
        _fail("finite applicability task has an unsupported requirement identity")
    result: set[str] = set()
    for field in fields:
        value = values.get(field)
        if type(value) is not str or not value:
            _fail(f"{requirement_id} consumed {field} is not a nonblank reference identity")
        result.add(value)
    return result


def build_runtime_applicability_projection(
    *,
    schema_bytes: bytes,
    manifest_bytes: bytes,
    fixture_bytes: bytes,
    development: Mapping[str, Any],
    integrity_baseline_bytes: bytes,
    source_identities: Mapping[str, Mapping[str, str]],
) -> RuntimeApplicabilityProjection:
    """Validate exact Git bytes and derive the finite P3 input projection."""

    schema = _json_object(schema_bytes, "runtime applicability schema")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        raise ApplicabilityInputError("runtime applicability schema is invalid") from exc
    manifest = _json_object(manifest_bytes, "runtime applicability manifest")
    fixture = _json_object(fixture_bytes, "runtime applicability fixture")
    baseline = _json_object(integrity_baseline_bytes, "integrity obligation baseline")
    _validate_document(schema, manifest, "runtime applicability manifest")
    _validate_document(schema, fixture, "runtime applicability fixture")
    expected_identity_names = {"schema", "manifest", "fixture", "development", "integrityBaseline"}
    if not isinstance(source_identities, Mapping) or set(source_identities) != expected_identity_names:
        _fail("runtime applicability source identities are incomplete")
    identities = MappingProxyType({
        name: _identity(source_identities[name], f"runtime applicability {name}")
        for name in sorted(expected_identity_names)
    })
    source_bindings = _exact_mapping(
        manifest.get("sourceBindings"), {"schema", "development", "integrityBaseline", "fixture"},
        "runtime applicability source bindings",
    )
    for name in ("schema", "development", "integrityBaseline", "fixture"):
        _declared_source_identity(source_bindings[name], identities[name], f"runtime applicability {name}")
    artifact = _exact_mapping(
        manifest.get("artifact"),
        {"id", "version", "purpose", "purposeZh", "scope", "experimentBoundary", "qualificationBoundary"},
        "runtime applicability artifact",
    )
    for field in ("id", "version", "purpose", "purposeZh"):
        _nonblank(artifact.get(field), f"runtime applicability artifact {field}")
    if (
        artifact.get("scope") != "ENGINEERING-SYNTHETIC-RUNTIME"
        or artifact.get("experimentBoundary") != "NOT-PR23-EXPERIMENT"
        or artifact.get("qualificationBoundary") != "NOT-ESTABLISHED"
    ):
        _fail("runtime applicability artifact crosses its controlled engineering boundary")
    fixture_artifact = _exact_mapping(
        fixture.get("artifact"), {"id", "version", "purpose", "scope"}, "runtime applicability fixture artifact",
    )
    for field in ("id", "version", "purpose"):
        _nonblank(fixture_artifact.get(field), f"runtime applicability fixture {field}")
    if fixture_artifact.get("scope") != "ENGINEERING-SYNTHETIC-RUNTIME":
        _fail("runtime applicability fixture crosses its controlled engineering boundary")
    controlled_rows = _source_rows(development, baseline)
    models, references = _fixture_indexes(fixture)
    tasks = manifest.get("tasks")
    if not isinstance(tasks, list) or len(tasks) != len(_INTEGRITY_REQUIREMENTS):
        _fail("runtime applicability manifest must declare exactly six integrity tasks")
    contexts: dict[str, _ContextProjection] = {}
    seen_task_ids: set[str] = set()
    task_rows: dict[str, tuple[str, str, str, str]] = {}
    for raw in tasks:
        fields = {
            "id", "contextId", "requirementId", "dependencyId", "sourceUnitId", "contractId",
            "modelId", "actionIds", "displayScenarioId", "displayService", "reasonRefs", "publicInputs",
        }
        row = _exact_mapping(raw, fields, "runtime applicability task")
        task_id = _nonblank(row.get("id"), "runtime applicability task identity")
        context_id = _nonblank(row.get("contextId"), f"{task_id} context identity")
        if task_id in seen_task_ids or context_id in contexts:
            _fail("runtime applicability task/context identity repeats")
        seen_task_ids.add(task_id)
        requirement_id = _nonblank(row.get("requirementId"), f"{task_id} requirement identity")
        source = (
            requirement_id,
            _nonblank(row.get("dependencyId"), f"{task_id} dependency identity"),
            _nonblank(row.get("sourceUnitId"), f"{task_id} source-unit identity"),
            _nonblank(row.get("contractId"), f"{task_id} contract identity"),
        )
        if requirement_id in task_rows or controlled_rows.get(requirement_id) != source:
            _fail(f"{task_id} does not exactly match its controlled source binding")
        task_rows[requirement_id] = source
        _nonblank(row.get("displayScenarioId"), f"{task_id} display scenario metadata")
        _nonblank(row.get("displayService"), f"{task_id} display service metadata")
        model_source_json, action_ids = _validate_model_context(
            raw=row, models=models, context_id=context_id,
        )
        values = row.get("publicInputs")
        if not isinstance(values, Mapping):
            _fail(f"{task_id} public inputs are not an object")
        active = _task_active(requirement_id, values, references)
        _exact_reason_references(
            supplied=row.get("reasonRefs"),
            expected=_task_reason_reference_ids(requirement_id, values),
            index=references,
            context_id=context_id,
        )
        input_identity = _digest((
            tuple((name, tuple(sorted(identity.items()))) for name, identity in identities.items()),
            task_id, context_id, source, _canonical_bytes(row),
        ))
        residual = ApplicabilityResidual(*source, context_id=context_id, input_identity=input_identity) if active else None
        contexts[context_id] = _ContextProjection(
            context_id=context_id,
            model_source_json=model_source_json,
            action_ids=action_ids,
            status="P3-ACTIVE" if active else "P3-EXPLICIT-INACTIVE",
            residual=residual,
        )
    if task_rows != controlled_rows:
        _fail("runtime applicability tasks do not exactly cover all six controlled source bindings")
    method_contexts = manifest.get("methodOnlyContexts")
    if not isinstance(method_contexts, list) or not method_contexts:
        _fail("runtime applicability manifest lacks a method-only control")
    integrity_domains = {
        (context.model_source_json, context.action_ids)
        for context in contexts.values()
    }
    integrity_action_ids = {
        action_id
        for _model_source_json, action_ids in integrity_domains
        for action_id in action_ids
    }
    for raw in method_contexts:
        row = _exact_mapping(
            raw,
            {"id", "modelId", "actionIds", "displayScenarioId", "displayService", "reasonRefs", "publicContext"},
            "method-only runtime context",
        )
        context_id = _nonblank(row.get("id"), "method-only context identity")
        if context_id in contexts:
            _fail("method-only context repeats an integrity context identity")
        _nonblank(row.get("displayScenarioId"), f"{context_id} display scenario metadata")
        _nonblank(row.get("displayService"), f"{context_id} display service metadata")
        public_context = _exact_mapping(
            row.get("publicContext"), {"kind", "description", "referenceId"}, f"{context_id} public method context",
        )
        if public_context.get("kind") != "METHOD-ONLY-NO-INTEGRITY-CONTEXT":
            _fail(f"{context_id} is not an explicit method-only context")
        _nonblank(public_context.get("description"), f"{context_id} public method description")
        method_reference = _reference(index=references, identifier=public_context.get("referenceId"), label=f"{context_id} public method reference")
        _require_kind(method_reference, expected="METHOD-ONLY-REFERENCE", label=f"{context_id} public method reference")
        _nonblank(method_reference.get("source"), f"{context_id} public method reference source")
        _exact_reason_references(
            supplied=row.get("reasonRefs"), expected={method_reference["id"]}, index=references, context_id=context_id,
        )
        model_source_json, action_ids = _validate_model_context(raw=row, models=models, context_id=context_id)
        if (model_source_json, action_ids) in integrity_domains or set(action_ids) & integrity_action_ids:
            _fail(f"{context_id} reuses an integrity task model/action domain")
        contexts[context_id] = _ContextProjection(
            context_id=context_id,
            model_source_json=model_source_json,
            action_ids=action_ids,
            status="P3-METHOD-ONLY",
            residual=None,
        )
    identity = _digest((
        tuple((name, tuple(sorted(source.items()))) for name, source in identities.items()),
        _canonical_bytes(manifest), _canonical_bytes(fixture),
    ))
    return RuntimeApplicabilityProjection(
        identity=identity,
        source_identities=identities,
        contexts=MappingProxyType(dict(contexts)),
    )
