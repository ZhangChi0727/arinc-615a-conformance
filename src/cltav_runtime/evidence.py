"""Versioned, replayable evidence for the bounded CL-TAV reference runtime.

This module is deliberately narrower than a general persistence layer.  It
serialises one finite, synthetic engineering run or an explicitly open prefix
which is reconstructed from three explicitly named Git objects: the
development contract, the interface registry, and a closed scenario object.
Neither artifact is a conformance verdict, an experiment result, or an
attestation for an arbitrary external executor.

The crucial boundary is that evidence is checked by rebuilding the same finite
run from the verified Git bytes.  A field in the JSON file therefore never
selects its own replay branch.  In particular, a resolution code, an opaque
producer label, or a refreshed digest cannot make a modified trace acceptable.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from fractions import Fraction
from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version as distribution_version
import json
import os
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable, Mapping
from uuid import uuid4

from .bindings import RuntimeAuthorityBinding, SourceSnapshot
from .interpretation import (
    InterpretationContract,
    ObservationAssessment,
    ObservationInput,
    OwnershipEvent,
    OwnershipReplay,
    OwnershipResolution,
)
from .kernel import ContractSnapshot, FrontierEntry, Interval, KernelDiagnostic, ModelContext
from .model import FiniteSessionModel, PredictionClass
from .session import (
    AlgorithmResourceView,
    ReferenceSession,
    ResourceState,
    RoundEvidence,
    SessionResult,
    SessionState,
)
from .synthetic import EnvironmentExecution, ExecutionRequest, SyntheticEnvironment, VisibleExecutionRecord
from .stopping import EquivalenceStatus, Named645Residual, StopTrace


EVIDENCE_ARTIFACT_TYPE = "CLTAV-FINITE-RUNTIME-EVIDENCE"
EVIDENCE_SCHEMA_VERSION = "1.0"
CHECKPOINT_ARTIFACT_TYPE = "CLTAV-FINITE-RUNTIME-CHECKPOINT"
CHECKPOINT_SCHEMA_VERSION = "1.0"
SCENARIO_ARTIFACT_TYPE = "CLTAV-FINITE-SYNTHETIC-SCENARIO"
SCENARIO_SCHEMA_VERSION = "1.0"
_PRODUCER_PROTOCOL = "CLTAV-FINITE-PRODUCER/1.0"
_RUNTIME_DISTRIBUTION = "a615a-sim"
_CHECKPOINT_TOKEN = object()
_CHECKPOINT_RUN_TOKEN = object()


def _runtime_distribution_version() -> str:
    """Return the installed package identity without consulting a checkout."""

    try:
        return distribution_version(_RUNTIME_DISTRIBUTION)
    except PackageNotFoundError:  # pragma: no cover - source-only defensive boundary.
        return "UNINSTALLED-SOURCE"


_RUNTIME_VERSION = _runtime_distribution_version()


class EvidenceError(ValueError):
    """A named, non-success failure at the finite evidence boundary."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


@dataclass(frozen=True)
class EvidenceSources:
    """The three raw Git objects consumed by one evidence production run."""

    repository: Path
    development: ContractSnapshot
    interfaces: SourceSnapshot
    scenario: SourceSnapshot

    def identities(self) -> dict[str, dict[str, str]]:
        return {
            "development": {
                "commit": self.development.contract_commit,
                "path": self.development.contract_path,
                "blobSha256": self.development.contract_blob_sha256,
            },
            "interfaceRegistry": dict(self.interfaces.identity()),
            "scenario": dict(self.scenario.identity()),
        }


@dataclass(frozen=True)
class RuntimeScenario:
    """A closed finite synthetic scenario parsed from verified raw Git bytes."""

    scenario_id: str
    model_mapping: Mapping[str, Any]
    environment_mapping: Mapping[str, Any]
    interpretation_mapping: Mapping[str, Any] | None
    session_id: str
    run_id: str
    initial_summary: str
    resource_mode: str
    resource_remaining: int
    retry_cap: int
    maximum_rounds: int
    producer_mode: str


@dataclass(frozen=True)
class EvidenceRun:
    """The private result of one actual finite producer/session execution."""

    scenario: RuntimeScenario
    sources: EvidenceSources
    result: SessionResult


@dataclass(frozen=True)
class _RuntimeContext:
    """One source-built live runtime, retained only for bounded G3 work."""

    scenario: RuntimeScenario
    sources: EvidenceSources
    session: ReferenceSession
    producer: SyntheticEnvironment | _FiniteFaultDriver


@dataclass(frozen=True)
class CheckpointRun:
    """An open, source-derived finite prefix before durable validation.

    This is deliberately not a deserialised JSON checkpoint.  It can only be
    created from explicit Git sources, and publication validates its projected
    bytes before handing back a continuation-capable typed checkpoint.
    """

    scenario: RuntimeScenario
    sources: EvidenceSources
    result: SessionResult
    prefix_rounds: int
    _context: _RuntimeContext = field(repr=False, compare=False)
    _construction_token: object | None = field(
        default=None, init=False, repr=False, compare=False,
    )


@dataclass(frozen=True)
class VerifiedCheckpoint:
    """A validated, source-reconstructed typed prefix for formal continuation.

    No JSON field is converted into a ``SessionState`` or environment.  The
    state and environment are the outputs of a fresh execution from the
    caller's verified Git objects whose canonical checkpoint projection was
    proven equal to the supplied durable package.
    """

    scenario: RuntimeScenario
    sources: EvidenceSources
    result: SessionResult
    prefix_rounds: int
    _context: _RuntimeContext = field(repr=False, compare=False)
    _verification_token: object | None = field(
        default=None, init=False, repr=False, compare=False,
    )


_PRODUCER_MODES = frozenset(
    {
        "SYNTHETIC-NORMAL",
        "CALCULABLE-IDENTITY-MISMATCH",
        "OPAQUE-INVALID-SUCCESSOR",
        "OPAQUE-TOOL-ERROR",
    },
)


def canonical_json_bytes(value: object) -> bytes:
    """Encode one finite JSON value with a single documented byte form.

    Evidence files are UTF-8, key-sorted and LF-terminated.  Git source bytes
    are intentionally *not* normalised here: their SHA-256 identity belongs to
    the raw object that was actually read through ``git show``.
    """

    _reject_floats(value)
    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise EvidenceError("EVIDENCE-ENCODING-ERROR", "evidence contains a non-JSON finite value") from exc
    return rendered.encode("utf-8") + b"\n"


def _reject_floats(value: object) -> None:
    """Keep exact quantities explicit instead of silently accepting floats."""

    if type(value) is float:
        raise EvidenceError("EVIDENCE-FLOAT-FORBIDDEN", "finite evidence cannot contain a floating-point value")
    if isinstance(value, Mapping):
        for key, item in value.items():
            if type(key) is not str:
                raise EvidenceError("EVIDENCE-ENCODING-ERROR", "evidence mapping keys must be strings")
            _reject_floats(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_floats(item)


def _strict_json_object(raw: bytes, *, label: str) -> dict[str, Any]:
    """Parse a UTF-8 JSON object without duplicate-object-key ambiguity."""

    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, item in pairs:
            if key in result:
                raise EvidenceError("EVIDENCE-DUPLICATE-KEY", f"{label} contains duplicate key {key!r}")
            result[key] = item
        return result

    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates)
    except EvidenceError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError("EVIDENCE-JSON-ERROR", f"{label} is not UTF-8 JSON") from exc
    if type(value) is not dict:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", f"{label} must be a JSON object")
    _reject_floats(value)
    return value


def load_evidence_bytes(raw: bytes) -> dict[str, Any]:
    """Load a canonical evidence document once for schema and relation checks."""

    return _load_canonical_document(raw, label="evidence")


def _load_canonical_document(raw: bytes, *, label: str) -> dict[str, Any]:
    """Decode one canonical finite JSON envelope without double-reading it."""

    value = _strict_json_object(raw, label=label)
    if canonical_json_bytes(value) != raw:
        raise EvidenceError(
            "EVIDENCE-NONCANONICAL-ENCODING",
            f"{label} must use the documented UTF-8, sorted-key, LF-terminated encoding",
        )
    return value


def load_checkpoint_bytes(raw: bytes) -> dict[str, Any]:
    """Load one canonical durable open-prefix checkpoint exactly once."""

    return _load_canonical_document(raw, label="checkpoint")


def load_sources(
    *,
    repository: Path | str,
    commit: str,
    development_path: str,
    interface_path: str,
    scenario_path: str,
) -> EvidenceSources:
    """Read every production input from explicit raw Git objects.

    No current worktree file, test fixture path, source-tree-relative resource,
    or ambient ``HEAD`` is used as an authority input.
    """

    try:
        repo = Path(repository).resolve(strict=True)
    except OSError as exc:
        raise EvidenceError("EVIDENCE-SOURCE-ERROR", "authority repository cannot be resolved") from exc
    if not repo.is_dir():
        raise EvidenceError("EVIDENCE-SOURCE-ERROR", "authority repository must be an existing directory")
    try:
        development = ContractSnapshot.from_git_object(
            repository=repo,
            contract_commit=commit,
            contract_path=development_path,
        )
        interfaces = SourceSnapshot.from_git_object(repository=repo, commit=commit, path=interface_path)
        scenario = SourceSnapshot.from_git_object(repository=repo, commit=commit, path=scenario_path)
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise EvidenceError("EVIDENCE-SOURCE-ERROR", str(exc) or type(exc).__name__) from exc
    return EvidenceSources(repo, development, interfaces, scenario)


def parse_scenario(snapshot: SourceSnapshot) -> RuntimeScenario:
    """Parse the closed scenario grammar from its exact Git bytes."""

    try:
        # ``identity`` also verifies the private snapshot token.  Do this
        # before looking at the retained bytes so a manually constructed
        # ``SourceSnapshot`` cannot impersonate a Git-qualified scenario
        # when this module is used as a library rather than through the CLI.
        snapshot.identity()
        raw = snapshot._content
        scenario = _strict_json_object(raw, label="runtime scenario")
    except (AttributeError, TypeError, ValueError) as exc:
        if isinstance(exc, EvidenceError):
            raise
        raise EvidenceError("SCENARIO-INPUT-ERROR", "verified runtime scenario cannot be decoded") from exc
    required = {
        "artifactType", "schemaVersion", "purpose", "scenarioId", "model", "environment", "interpretationContract", "session", "producerMode",
    }
    if set(scenario) != required:
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario has unknown or missing top-level fields")
    if scenario["artifactType"] != SCENARIO_ARTIFACT_TYPE or scenario["schemaVersion"] != SCENARIO_SCHEMA_VERSION:
        raise EvidenceError("SCENARIO-VERSION-ERROR", "runtime scenario artifact type or schema version is unsupported")
    if scenario["purpose"] != "SYNTHETIC-ENGINEERING-VALIDATION":
        raise EvidenceError("SCENARIO-PURPOSE-ERROR", "runtime scenario must remain synthetic engineering validation")
    scenario_id = scenario["scenarioId"]
    model = scenario["model"]
    environment = scenario["environment"]
    interpretation = scenario["interpretationContract"]
    session = scenario["session"]
    producer_mode = scenario["producerMode"]
    if type(scenario_id) is not str or not scenario_id:
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario identity is invalid")
    if type(model) is not dict or type(environment) is not dict or type(session) is not dict:
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario model, environment, and session must be objects")
    if interpretation is not None and type(interpretation) is not dict:
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario interpretation contract must be null or an object")
    if type(producer_mode) is not str:
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario producer mode is invalid")
    if producer_mode == "EXTERNAL-OPAQUE-UNVERIFIED":
        raise EvidenceError(
            "EXTERNAL-OPAQUE-SOURCE-UNSUPPORTED",
            "external opaque material cannot enter qualified finite replay",
        )
    if producer_mode not in _PRODUCER_MODES:
        raise EvidenceError("SCENARIO-PRODUCER-ERROR", "runtime scenario producer mode is unsupported")
    required_session = {
        "sessionId", "runId", "initialSummary", "resourceMode", "resourceRemaining", "retryCap", "maximumRounds",
    }
    if set(session) != required_session:
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario session uses unknown or missing fields")
    session_id = session["sessionId"]
    run_id = session["runId"]
    initial_summary = session["initialSummary"]
    mode = session["resourceMode"]
    remaining = session["resourceRemaining"]
    retry_cap = session["retryCap"]
    maximum_rounds = session["maximumRounds"]
    if any(type(value) is not str or not value for value in (session_id, run_id, initial_summary)):
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario session identifiers are invalid")
    # Check the exact JSON scalar type before set membership.  This both
    # distinguishes bool from integer-like values and prevents malformed
    # arrays/objects from leaking Python's unhashable-container exception.
    if type(mode) is not str or mode not in {"ROUNDS", "BUDGET"}:
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario resource mode is invalid")
    if any(type(value) is not int or value < 1 for value in (remaining, retry_cap, maximum_rounds)):
        raise EvidenceError("SCENARIO-SHAPE-ERROR", "runtime scenario numeric limits must be positive integers")
    # The scenario grammar deliberately excludes evaluator truth, experiment
    # labels, callable imports, and arbitrary producer objects by having a
    # closed top level and a finite producer-mode vocabulary.  The existing
    # model/environment parsers close their own nested grammars below.
    return RuntimeScenario(
        scenario_id=scenario_id,
        model_mapping=MappingProxyType(dict(model)),
        environment_mapping=MappingProxyType(dict(environment)),
        interpretation_mapping=(None if interpretation is None else MappingProxyType(dict(interpretation))),
        session_id=session_id,
        run_id=run_id,
        initial_summary=initial_summary,
        resource_mode=mode,
        resource_remaining=remaining,
        retry_cap=retry_cap,
        maximum_rounds=maximum_rounds,
        producer_mode=producer_mode,
    )


def run_scenario(sources: EvidenceSources) -> EvidenceRun:
    """Run one actual finite synthetic scenario using the verified sources."""

    context = _build_runtime(sources)
    try:
        result = context.session.run(context.producer, maximum_rounds=context.scenario.maximum_rounds)  # type: ignore[arg-type]
    except EvidenceError:
        raise
    except (AttributeError, TypeError, ValueError) as exc:
        raise EvidenceError("SCENARIO-EXECUTION-ERROR", str(exc) or type(exc).__name__) from exc
    return EvidenceRun(context.scenario, sources, result)


def _build_runtime(sources: EvidenceSources) -> _RuntimeContext:
    """Build one live finite runtime solely from verified Git source objects."""

    try:
        scenario = parse_scenario(sources.scenario)
        binding = RuntimeAuthorityBinding._from_verified_snapshots(
            development=sources.development,
            interfaces=sources.interfaces,
        )
        model = _model_from_scenario(sources.development, scenario)
        interpretation_contract = _interpretation_contract_from_scenario(model, scenario)
        environment = SyntheticEnvironment.from_mapping(scenario.environment_mapping)
        resources = (
            ResourceState.rounds(scenario.resource_remaining)
            if scenario.resource_mode == "ROUNDS"
            else ResourceState.budget(scenario.resource_remaining)
        )
        session = ReferenceSession(
            binding=binding,
            model=model,
            session_id=scenario.session_id,
            run_id=scenario.run_id,
            initial_summary=scenario.initial_summary,
            resources=resources,
            retry_cap=scenario.retry_cap,
            interpretation_contract=interpretation_contract,
        )
        producer: SyntheticEnvironment | _FiniteFaultDriver
        if scenario.producer_mode == "SYNTHETIC-NORMAL":
            producer = environment
        else:
            producer = _FiniteFaultDriver(environment, scenario.producer_mode)
    except EvidenceError:
        raise
    except (AttributeError, TypeError, ValueError) as exc:
        raise EvidenceError("SCENARIO-EXECUTION-ERROR", str(exc) or type(exc).__name__) from exc
    return _RuntimeContext(scenario, sources, session, producer)


def create_checkpoint(sources: EvidenceSources, *, prefix_rounds: int) -> CheckpointRun:
    """Create one bounded open prefix from explicit source authority.

    The result is useful only after :func:`publish_checkpoint` or
    :func:`validate_checkpoint_bytes` establishes the durable relation.  It
    contains typed outputs from an actual public ``ReferenceSession`` run; it
    never rehydrates a state from evidence JSON.
    """

    if type(prefix_rounds) is not int or prefix_rounds < 1:
        raise EvidenceError("CHECKPOINT-PREFIX-ERROR", "checkpoint prefix rounds must be a positive integer")
    context = _build_runtime(sources)
    if prefix_rounds >= context.scenario.maximum_rounds:
        raise EvidenceError(
            "CHECKPOINT-PREFIX-ERROR",
            "checkpoint prefix must leave at least one declared source round for continuation",
        )
    try:
        result = context.session.run(context.producer, maximum_rounds=prefix_rounds)  # type: ignore[arg-type]
    except (AttributeError, TypeError, ValueError) as exc:
        raise EvidenceError("CHECKPOINT-EXECUTION-ERROR", str(exc) or type(exc).__name__) from exc
    if (
        result.stop_reason != "Stop-Round-Limit"
        or len(result.state.evidence) != prefix_rounds
        or (result.state.evidence and result.state.evidence[-1].stop_reason is not None)
    ):
        raise EvidenceError(
            "CHECKPOINT-NOT-OPEN",
            "checkpoint prefix must end at an open round-limit boundary rather than a terminal session state",
        )
    checkpoint = CheckpointRun(
        scenario=context.scenario,
        sources=sources,
        result=result,
        prefix_rounds=prefix_rounds,
        _context=context,
    )
    object.__setattr__(checkpoint, "_construction_token", _CHECKPOINT_RUN_TOKEN)
    return checkpoint


def _require_checkpoint_run(value: object) -> CheckpointRun:
    if type(value) is not CheckpointRun or value._construction_token is not _CHECKPOINT_RUN_TOKEN:
        raise EvidenceError("CHECKPOINT-PROVENANCE-ERROR", "checkpoint prefix was not created by the verified finite runtime")
    return value


def _verified_checkpoint(run: CheckpointRun) -> VerifiedCheckpoint:
    """Mark one already stage-validated source prefix as continuation-ready."""

    run = _require_checkpoint_run(run)
    verified = VerifiedCheckpoint(
        scenario=run.scenario,
        sources=run.sources,
        result=run.result,
        prefix_rounds=run.prefix_rounds,
        _context=run._context,
    )
    object.__setattr__(verified, "_verification_token", _CHECKPOINT_TOKEN)
    return verified


def _require_verified_checkpoint(value: object) -> VerifiedCheckpoint:
    if type(value) is not VerifiedCheckpoint or value._verification_token is not _CHECKPOINT_TOKEN:
        raise EvidenceError("CHECKPOINT-PROVENANCE-ERROR", "checkpoint was not validated from explicit Git sources")
    return value


def continue_checkpoint(checkpoint: VerifiedCheckpoint) -> EvidenceRun:
    """Execute only the remaining declared rounds from a verified prefix.

    The original evidence, attempts, history and resource ledger remain in
    ``checkpoint.result.state``.  This function calls the public ``step``
    boundary only for post-prefix work; it never re-runs the initial prefix.
    """

    checkpoint = _require_verified_checkpoint(checkpoint)
    remaining_rounds = checkpoint.scenario.maximum_rounds - checkpoint.prefix_rounds
    if remaining_rounds < 1:
        raise EvidenceError("CHECKPOINT-NOT-OPEN", "checkpoint has no declared source rounds remaining")
    state = checkpoint.result.state
    environment = checkpoint.result.environment
    session = checkpoint._context.session
    for _ in range(remaining_rounds):
        step = session.step(state, environment)
        state, environment = step.state, step.environment
        if step.stop_reason is not None:
            return EvidenceRun(
                checkpoint.scenario,
                checkpoint.sources,
                SessionResult(state, environment, step.stop_reason, step.diagnostics, step.stop_trace),
            )
    return EvidenceRun(
        checkpoint.scenario,
        checkpoint.sources,
        SessionResult(
            state,
            environment,
            "Stop-Round-Limit",
            (KernelDiagnostic("ROUND-LIMIT", "declared synthetic round limit reached"),),
        ),
    )


def _model_from_scenario(development: ContractSnapshot, scenario: RuntimeScenario) -> FiniteSessionModel:
    """Construct the model from the exact scenario object, not a fixture path."""

    try:
        public_model = scenario.model_mapping.get("model")
        uncertainty = scenario.model_mapping.get("uncertainty")
        if type(public_model) is not dict or set(public_model) != {"stateIds", "clockIds", "typedDomains"}:
            raise ValueError("scenario public model projection is invalid")
        if type(uncertainty) is not dict or type(uncertainty.get("clockId")) is not str:
            raise ValueError("scenario uncertainty projection is invalid")
        state_ids = public_model["stateIds"]
        clock_ids = public_model["clockIds"]
        typed_domains = public_model["typedDomains"]
        if (
            type(state_ids) is not list
            or type(clock_ids) is not list
            or type(typed_domains) is not dict
            or any(type(value) is not str or not value for value in state_ids + clock_ids)
            or any(
                type(name) is not str
                or not name
                or type(values) is not list
                or any(type(member) not in {str, int, bool} for member in values)
                for name, values in typed_domains.items()
            )
        ):
            raise ValueError("scenario finite model domain is invalid")
        context = ModelContext.build(
            snapshot=development,
            model={
                "stateIds": set(state_ids),
                "clockIds": set(clock_ids),
                "typedDomains": {name: set(values) for name, values in typed_domains.items()},
            },
            projection_clock=uncertainty["clockId"],
        )
        # ``RuntimeScenario`` freezes its outer mapping for the evidence
        # boundary.  The established model parser deliberately accepts only
        # ordinary JSON containers, so pass a fresh plain outer object rather
        # than asking it to serialise a ``mappingproxy``.
        return FiniteSessionModel.from_mapping(context=context, value=dict(scenario.model_mapping))
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise EvidenceError("SCENARIO-MODEL-ERROR", str(exc) or type(exc).__name__) from exc


def _interpretation_contract_from_scenario(
    model: FiniteSessionModel,
    scenario: RuntimeScenario,
) -> InterpretationContract | None:
    """Decode the optional, Git-bound synthetic timing contract.

    The contract belongs to the scenario source rather than to raw environment
    material.  A single explicit token binds its error-budget identity to the
    already parsed model uncertainty, so a JSON fixture cannot select a
    different clock/budget identity while still appearing to match the model.
    ``REVIEWED`` deadlines remain unavailable to this bounded runtime and are
    rejected by the established session constructor.
    """

    value = scenario.interpretation_mapping
    if value is None:
        return None
    required = {
        "contractId", "triggerEventType", "responseEventType", "key", "policy", "concurrentSameKey",
        "cancellationEventType", "supersessionEventType", "physicalDomain", "requirementWindow",
        "clockIdentity", "uncertaintyIdentity", "errorBudgetIdentity", "unit", "clockValid",
        "errorBudgetValid", "deadlineAuthority", "deadlineIdentity", "upperBound", "upperClosed",
    }
    if set(value) != required:
        raise EvidenceError("SCENARIO-CONTRACT-ERROR", "synthetic interpretation contract uses unknown or missing fields")
    string_fields = (
        "contractId", "triggerEventType", "responseEventType", "key", "policy", "cancellationEventType",
        "supersessionEventType", "clockIdentity", "uncertaintyIdentity", "errorBudgetIdentity", "unit",
        "deadlineAuthority",
    )
    if any(type(value[field]) is not str or not value[field] for field in string_fields):
        raise EvidenceError("SCENARIO-CONTRACT-ERROR", "synthetic interpretation contract has an invalid identity field")
    if value["deadlineIdentity"] is not None and (
        type(value["deadlineIdentity"]) is not str or not value["deadlineIdentity"]
    ):
        raise EvidenceError("SCENARIO-CONTRACT-ERROR", "synthetic interpretation contract has an invalid deadline identity")
    if any(type(value[field]) is not bool for field in ("concurrentSameKey", "clockValid", "errorBudgetValid", "upperClosed")):
        raise EvidenceError("SCENARIO-CONTRACT-ERROR", "synthetic interpretation contract Boolean fields are invalid")
    if value["deadlineAuthority"] not in {"METHOD-ONLY", "UNRESOLVED"}:
        raise EvidenceError(
            "SCENARIO-CONTRACT-ERROR",
            "synthetic interpretation contract cannot claim a reviewed protocol deadline",
        )
    if (
        value["clockIdentity"] != model.uncertainty.clock_id
        or value["uncertaintyIdentity"] != model.uncertainty.uncertainty_id
        or value["unit"] != model.uncertainty.time_unit
        or value["errorBudgetIdentity"] != "MODEL-UNCERTAINTY-DIGEST"
    ):
        raise EvidenceError(
            "SCENARIO-CONTRACT-ERROR",
            "synthetic interpretation contract does not bind the parsed model uncertainty",
        )
    try:
        physical = Interval.from_mapping(value["physicalDomain"])
        requirement = Interval.from_mapping(value["requirementWindow"])
        upper = _exact_fraction_or_none(value["upperBound"])
        return InterpretationContract(
            value["contractId"],
            value["triggerEventType"],
            value["responseEventType"],
            value["key"],
            value["policy"],
            value["concurrentSameKey"],
            value["cancellationEventType"],
            value["supersessionEventType"],
            physical,
            requirement,
            value["clockIdentity"],
            value["uncertaintyIdentity"],
            model.uncertainty.identity,
            value["unit"],
            value["clockValid"],
            value["errorBudgetValid"],
            value["deadlineAuthority"],
            value["deadlineIdentity"],
            upper,
            value["upperClosed"],
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise EvidenceError("SCENARIO-CONTRACT-ERROR", "synthetic interpretation contract is invalid") from exc


def _exact_fraction_or_none(value: object) -> Fraction | None:
    if value is None:
        return None
    if type(value) is int:
        return Fraction(value)
    if type(value) is dict and set(value) == {"numerator", "positiveDenominator"}:
        numerator = value["numerator"]
        denominator = value["positiveDenominator"]
        if type(numerator) is int and type(denominator) is int and denominator > 0:
            return Fraction(numerator, denominator)
    raise ValueError("exact rational is invalid")


class _FiniteFaultDriver:
    """A finite, Git-configured synthetic source for G1 causal evidence.

    It is intentionally not a plugin mechanism.  Each mode is a fixed
    producer behavior that is exercised through the public session S4 call.
    The evidence serializer derives the producer fact from the observed S7
    result and the verified scenario; it never accepts an evidence-supplied
    fact as an instruction.
    """

    def __init__(self, environment: SyntheticEnvironment, mode: str) -> None:
        self._environment = environment
        self._mode = mode
        self._fault_emitted = False

    def execute(self, request: ExecutionRequest) -> EnvironmentExecution:
        # A fault plan is scoped to the first issued S4 attempt.  In
        # particular, an opaque failure can leave this wrapper in place for a
        # later Recover because no valid successor is available to replace it.
        # That later action must exercise the ordinary synthetic environment,
        # not silently receive the same injected fault until retry-cap hides
        # the recovery relation.
        if self._fault_emitted:
            return self._environment.execute(request)
        self._fault_emitted = True
        if self._mode == "OPAQUE-TOOL-ERROR":
            raise RuntimeError("finite synthetic tool boundary error")
        execution = self._environment.execute(request)
        if self._mode == "CALCULABLE-IDENTITY-MISMATCH":
            return EnvironmentExecution(
                replace(execution.record, action_id=f"forged:{request.action_id}"),
                execution.successor,
            )
        if self._mode == "OPAQUE-INVALID-SUCCESSOR":
            # The returned raw record is typed and may be retained by the
            # existing G1 policy, while the producer-stage successor fact is
            # not inferable from the record alone.
            return EnvironmentExecution(execution.record, None)  # type: ignore[arg-type]
        raise AssertionError("finite fault driver mode was not closed")


def evidence_document(run: EvidenceRun) -> dict[str, Any]:
    """Project an actual run into a canonical public evidence document."""

    result = run.result
    state = result.state
    payload: dict[str, Any] = {
        "artifactType": EVIDENCE_ARTIFACT_TYPE,
        "schemaVersion": EVIDENCE_SCHEMA_VERSION,
        "boundary": {
            "purpose": "SYNTHETIC-ENGINEERING-VALIDATION",
            "conformanceVerdict": "NOT-EVALUATED",
            "runtimeIntegrity": "NOT-ESTABLISHED",
            "externalOpaqueSource": "UNSUPPORTED-FOR-QUALIFIED-REPLAY",
        },
        "inputs": run.sources.identities(),
        "run": {
            "scenarioId": run.scenario.scenario_id,
            "sessionId": run.scenario.session_id,
            "runId": run.scenario.run_id,
            # The bounded synthetic producer has no external reset adapter.
            # Make that absence explicit rather than manufacturing a reset
            # identity or silently dropping the field from a persistent run.
            "resetId": None,
            "maximumRounds": run.scenario.maximum_rounds,
            "producerMode": run.scenario.producer_mode,
        },
        "rounds": [_round_mapping(item) for item in state.evidence],
        "producerFacts": _producer_facts(run),
        "outcome": {
            "stopReason": result.stop_reason,
            "diagnostics": [_diagnostic_mapping(item) for item in result.diagnostics],
            "state": _state_mapping(state),
        },
    }
    digest = sha256(canonical_json_bytes(payload)).hexdigest()
    return {**payload, "integrity": {"canonicalPayloadSha256": digest}}


def evidence_bytes(run: EvidenceRun) -> bytes:
    """Return the canonical bytes of a newly produced evidence document."""

    return canonical_json_bytes(evidence_document(run))


def checkpoint_document(checkpoint: CheckpointRun) -> dict[str, Any]:
    """Project one open source prefix into a versioned checkpoint envelope."""

    checkpoint = _require_checkpoint_run(checkpoint)
    # Start from the same independently projected state/evidence relation as
    # a final run, then make the open-prefix boundary explicit.  The
    # checkpoint is not a terminal verdict and cannot silently impersonate a
    # complete evidence artifact.
    projected = evidence_document(EvidenceRun(
        checkpoint.scenario,
        checkpoint.sources,
        checkpoint.result,
    ))
    payload = {key: value for key, value in projected.items() if key != "integrity"}
    payload["artifactType"] = CHECKPOINT_ARTIFACT_TYPE
    payload["schemaVersion"] = CHECKPOINT_SCHEMA_VERSION
    payload["checkpoint"] = {
        "prefixRounds": checkpoint.prefix_rounds,
        "sourceMaximumRounds": checkpoint.scenario.maximum_rounds,
        "status": "OPEN-PREFIX",
    }
    digest = sha256(canonical_json_bytes(payload)).hexdigest()
    return {**payload, "integrity": {"canonicalPayloadSha256": digest}}


def checkpoint_bytes(checkpoint: CheckpointRun) -> bytes:
    """Return canonical durable bytes for an open finite prefix."""

    return canonical_json_bytes(checkpoint_document(checkpoint))


def _producer_facts(run: EvidenceRun) -> list[dict[str, str]]:
    """Derive stage facts from actual S4/S7 output plus verified scenario mode.

    A scenario controls at most the first faulting call.  If the real session
    accepts the actual successor and later issues a Recover, the later round
    is produced by the ordinary ``SyntheticEnvironment`` and must therefore
    be described as such.  The checks below keep a scenario label from
    masquerading as an observed stage/result fact.
    """

    facts: list[dict[str, str]] = []
    for index, item in enumerate(run.result.state.evidence):
        is_fault_round = index == 0 and run.scenario.producer_mode != "SYNTHETIC-NORMAL"
        mode = run.scenario.producer_mode if is_fault_round else "SYNTHETIC-NORMAL"
        base = {
            "producerId": (
                "cltav-runtime-finite-fault-driver"
                if is_fault_round else "cltav-runtime-synthetic-environment"
            ),
            "producerProtocol": _PRODUCER_PROTOCOL,
            "runtimeDistribution": _RUNTIME_DISTRIBUTION,
            "runtimeVersion": _RUNTIME_VERSION,
            "runId": run.scenario.run_id,
            "sessionId": run.scenario.session_id,
            "attemptId": item.execution.execution_attempt_id,
            "issuedActionId": item.snapshot.action_id,
            "actionKind": item.snapshot.action_kind,
        }
        if mode == "SYNTHETIC-NORMAL":
            # This fact is about the observed producer boundary, not whether
            # the coordinator later commits the result.  In particular, a
            # normal finite environment can truthfully return a
            # CONFIRMED-NOT-SENT or UNKNOWN-EFFECT record, and a valid timing
            # contract can retain response-free material through S7.  Keep
            # those distinct from an injected fault and let the established
            # session/rebuild validate their downstream history and resource
            # semantics.
            normal_facts = {
                "NONE": "TYPED-VISIBLE-RECORD",
                "CONFIRMED-NOT-SENT": "TYPED-CONFIRMED-NOT-SENT",
                "UNKNOWN-EFFECT": "TYPED-UNKNOWN-EFFECT",
            }
            normal_fact = normal_facts.get(item.execution.effect_class)
            if normal_fact is None or item.execution.action_id != item.snapshot.action_id:
                raise EvidenceError(
                    "PRODUCER-FACT-MISMATCH",
                    "normal finite producer did not return a typed record for the issued action",
                )
            if (
                item.execution.effect_class == "NONE"
                and item.observation_assessment is not None
                and item.observation_assessment.kind == "NO-RESPONSE"
            ):
                normal_fact = "TYPED-NO-RESPONSE-MATERIAL"
            facts.append({**base, "stage": "S4-EXECUTE-RETURN", "fact": normal_fact})
        elif mode == "CALCULABLE-IDENTITY-MISMATCH":
            if (
                item.resolution_code != "EXECUTION-IDENTITY-ERROR"
                or item.rejected_response is None
                or item.rejected_response.action_id == item.snapshot.action_id
            ):
                raise EvidenceError(
                    "PRODUCER-FACT-MISMATCH",
                    "finite calculable identity driver did not reach the typed production classifier",
                )
            facts.append({**base, "stage": "S4-EXECUTE-RETURN", "fact": "CALCULABLE-IDENTITY-MISMATCH"})
        elif mode == "OPAQUE-INVALID-SUCCESSOR":
            if item.resolution_code != "EXECUTION-RESULT-TYPE-ERROR" or item.rejected_response is None:
                raise EvidenceError(
                    "PRODUCER-FACT-MISMATCH",
                    "finite opaque successor driver did not reach the production result-type branch",
                )
            facts.append({**base, "stage": "S4-EXECUTE-RETURN", "fact": "INVALID-SUCCESSOR-TYPE"})
        elif mode == "OPAQUE-TOOL-ERROR":
            if item.resolution_code != "EXECUTION-TOOL-ERROR" or item.rejected_response is not None:
                raise EvidenceError(
                    "PRODUCER-FACT-MISMATCH",
                    "finite tool-error driver did not reach the execute-boundary error branch",
                )
            facts.append({**base, "stage": "S4-EXECUTE-CALL", "fact": "FINITE-TOOL-EXCEPTION"})
        else:  # pragma: no cover - parse_scenario closes this vocabulary.
            raise EvidenceError("SCENARIO-PRODUCER-ERROR", "producer mode is unsupported")
    return facts


def _round_mapping(item: RoundEvidence) -> dict[str, Any]:
    return {
        "selection": {
            "snapshotId": item.snapshot.snapshot_id,
            "actionId": item.snapshot.action_id,
            "actionKind": item.snapshot.action_kind,
            "summaryAtSelect": item.snapshot.q_used_at_select,
            "historyVersion": item.snapshot.history_version,
            "hypotheses": sorted(item.snapshot.hypotheses),
            "modelIdentity": item.snapshot.model_identity,
            "uncertaintyIdentity": item.snapshot.uncertainty_identity,
            "uncertaintyDigest": item.snapshot.uncertainty_digest,
            "authorityIdentities": _identity_mapping(item.snapshot.authority_identities),
            "prediction": _prediction_mapping(item.prediction),
        },
        "execution": _execution_mapping(item.execution),
        "issuedToExecutor": item.issued_to_executor,
        "chargedOnce": item.charged_once,
        "resourceBefore": _resource_mapping(item.resource_before),
        "resourceAfter": _resource_mapping(item.resource_after),
        "detailCharges": _int_mapping(item.detail_charges),
        "projectedCost": _int_mapping(item.projected_cost),
        "historyBefore": _history_mapping(item.history_before),
        "historyAfter": _history_mapping(item.history_after),
        "summaryAfter": item.summary_after,
        "committed": item.committed,
        "resolutionCode": item.resolution_code,
        "observationAssessment": _assessment_mapping(item.observation_assessment),
        "stopTrace": _stop_trace_mapping(item.stop_trace),
        "stopReason": item.stop_reason,
        "rejectedResponse": None if item.rejected_response is None else _execution_mapping(item.rejected_response),
    }


def _identity_mapping(value: Mapping[str, Mapping[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for source in sorted(value):
        identity = value[source]
        result[source] = {
            "commit": identity["commit"],
            "path": identity["path"],
            "blobSha256": identity["blobSha256"],
        }
    return result


def _prediction_mapping(prediction: object) -> dict[str, Any]:
    if not hasattr(prediction, "action_id") or not hasattr(prediction, "classes") or not hasattr(prediction, "diagnostics"):
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "round prediction has an invalid type")
    classes = getattr(prediction, "classes")
    diagnostics = getattr(prediction, "diagnostics")
    return {
        "actionId": prediction.action_id,
        "classes": [_prediction_class_mapping(value) for value in classes],
        "diagnostics": [_diagnostic_mapping(value) for value in diagnostics],
    }


def _prediction_class_mapping(value: PredictionClass) -> dict[str, Any]:
    return {
        "observable": value.observable,
        "hypotheses": sorted(value.hypotheses),
        "conservativeHypotheses": sorted(value.conservative_hypotheses),
        "measurementWindows": {
            name: _interval_mapping(interval)
            for name, interval in sorted(value.measurement_windows.items())
        },
        "successorProvenance": {
            name: [list(entry.history_provenance) for entry in paths]
            for name, paths in sorted(value.successors.items())
        },
    }


def _execution_mapping(record: VisibleExecutionRecord) -> dict[str, Any]:
    result: dict[str, Any] = {
        "executionAttemptId": record.execution_attempt_id,
        "actionId": record.action_id,
        "effectClass": record.effect_class,
        "observable": record.observable,
        "summaryConfirmed": record.summary_confirmed,
        "postSummary": record.post_summary,
        "measurementTick": None if record.measurement_tick is None else _fraction_mapping(record.measurement_tick),
        "uncertaintyIdentity": record.uncertainty_identity,
        "evidenceRef": record.evidence_ref,
        "responseId": record.response_id,
        "observationInput": _observation_input_mapping(record.observation_input),
    }
    if record.prep_recover is not None:
        result["prepRecover"] = {
            "targetConfirmed": record.prep_recover.target_confirmed,
            "summaryConfirmed": record.prep_recover.summary_confirmed,
            "prepError": record.prep_recover.prep_error,
            "ineligible": record.prep_recover.ineligible,
            "declaredTarget": record.prep_recover.declared_target,
            "evidence": record.prep_recover.evidence,
            "postSummary": record.prep_recover.post_summary,
        }
    return result


def _observation_input_mapping(value: ObservationInput | None) -> dict[str, Any] | None:
    """Project raw public timing material without accepting an evaluator answer."""

    if value is None:
        return None
    if type(value) is not ObservationInput:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "observation input is not typed")
    if type(value.events) is not tuple:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "observation input events are not closed")
    return {
        "events": [_ownership_event_mapping(item) for item in value.events],
        "triggerEventId": _json_safe_scalar(value.trigger_event_id),
        "responseId": _json_safe_scalar(value.response_id),
        "measurementInterval": _interval_mapping_or_none(value.measurement_interval),
        "observationEndQualified": _json_safe_scalar(value.observation_end_qualified),
        "earliestElapsed": _fraction_mapping_or_none(value.earliest_elapsed),
        "clockIdentity": _json_safe_scalar(value.clock_identity),
        "unit": _json_safe_scalar(value.unit),
        "executionAttemptId": _json_safe_scalar(value.execution_attempt_id),
        "actionId": _json_safe_scalar(value.action_id),
        "evidenceRef": _json_safe_scalar(value.evidence_ref),
        "measurementTick": _fraction_mapping_or_none(value.measurement_tick),
        "uncertaintyIdentity": _json_safe_scalar(value.uncertainty_identity),
    }


def _ownership_event_mapping(value: OwnershipEvent) -> dict[str, object]:
    if type(value) is not OwnershipEvent:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "ownership event is not typed")
    return {
        "id": _json_safe_scalar(value.event_id),
        "sequence": _json_safe_scalar(value.sequence),
        "kind": _json_safe_scalar(value.kind),
        "key": _json_safe_scalar(value.key),
        "eventType": _json_safe_scalar(value.event_type),
        "timestamp": _json_safe_scalar(value.timestamp),
        "targetRequestId": _json_safe_scalar(value.target_request_id),
    }


def _assessment_mapping(value: ObservationAssessment | None) -> dict[str, Any] | None:
    """Project a session-derived assessment and its complete ownership replay."""

    if value is None:
        return None
    if type(value) is not ObservationAssessment:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "observation assessment is not typed")
    return {
        "kind": value.kind,
        "verdict": value.verdict,
        "scoreDisposition": value.score_disposition,
        "answered": value.answered,
        "reason": value.reason,
        "contractId": value.contract_id,
        "executionAttemptId": value.execution_attempt_id,
        "actionId": value.action_id,
        "evidenceRef": value.evidence_ref,
        "triggerEventId": value.trigger_event_id,
        "responseId": value.response_id,
        "ownership": _ownership_resolution_mapping(value.ownership),
        "replay": _ownership_replay_mapping(value.replay),
        "measurementInterval": _interval_mapping_or_none(value.measurement_interval),
        "physicalInterval": _interval_mapping_or_none(value.physical_interval),
        "requirementWindow": _interval_mapping_or_none(value.requirement_window),
        "clockIdentity": value.clock_identity,
        "uncertaintyIdentity": value.uncertainty_identity,
        "errorBudgetIdentity": value.error_budget_identity,
        "unit": value.unit,
        "deadlineIdentity": value.deadline_identity,
        "evidenceRefs": list(value.evidence_refs),
        "diagnostics": [_diagnostic_mapping(item) for item in value.diagnostics],
    }


def _ownership_resolution_mapping(value: OwnershipResolution | None) -> dict[str, Any] | None:
    if value is None:
        return None
    if type(value) is not OwnershipResolution:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "ownership resolution is not typed")
    return {
        "responseId": value.response_id,
        "status": value.status,
        "ownerRequestId": value.owner_request_id,
        "candidateRequestIds": list(value.candidate_request_ids),
        "evidenceRefs": list(value.evidence_refs),
        "diagnostics": [_diagnostic_mapping(item) for item in value.diagnostics],
    }


def _ownership_replay_mapping(value: OwnershipReplay | None) -> dict[str, Any] | None:
    if value is None:
        return None
    if type(value) is not OwnershipReplay:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "ownership replay is not typed")
    return {
        "contractId": value.contract_id,
        "requestDispositions": dict(sorted(value.request_dispositions.items())),
        "terminationRefs": dict(sorted(value.termination_refs.items())),
        "responseResolutions": {
            response_id: _ownership_resolution_mapping(resolution)
            for response_id, resolution in sorted(value.response_resolutions.items())
        },
        "eventRefs": {
            event_id: _ownership_event_mapping(event)
            for event_id, event in sorted(value.event_refs.items())
        },
        "rejectedEventIds": sorted(value.rejected_event_ids),
        "diagnostics": [_diagnostic_mapping(item) for item in value.diagnostics],
    }


def _stop_trace_mapping(value: StopTrace | None) -> dict[str, Any] | None:
    if value is None:
        return None
    if type(value) is not StopTrace:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "stop trace is not typed")
    return {
        "phase": value.phase,
        "stopClass": value.stop_class,
        "reason": value.reason,
        "finalHypotheses": list(value.final_hypotheses),
        "historyVersion": value.history_version,
        "resourceMode": value.resource_mode,
        "resourceRemaining": value.resource_remaining,
        "retryCount": value.retry_count,
        "retryCap": value.retry_cap,
        "applicabilityStatus": value.applicability_status,
        "applicabilityContextId": value.applicability_context_id,
        "applicabilityInputIdentity": value.applicability_input_identity,
        "activeNamed645Residuals": [_residual_mapping(item) for item in value.active_named_645_residuals],
        "equivalence": _equivalence_mapping(value.equivalence),
        "modelIdentity": value.model_identity,
        "authorityIdentity": value.authority_identity,
        "traceIdentity": value.trace_identity,
    }


def _residual_mapping(value: Named645Residual) -> dict[str, str]:
    if type(value) is not Named645Residual:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "named residual is not typed")
    return {
        "requirementId": value.requirement_id,
        "dependencyId": value.dependency_id,
        "sourceUnitId": value.source_unit_id,
        "contractId": value.contract_id,
        "contextId": value.context_id,
        "inputIdentity": value.input_identity,
        "identity": value.identity,
    }


def _equivalence_mapping(value: EquivalenceStatus) -> dict[str, Any]:
    if type(value) is not EquivalenceStatus:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "equivalence status is not typed")
    return {
        "tag": value.tag,
        "reason": value.reason,
        "hypotheses": list(value.hypotheses),
        "historyVersion": value.history_version,
        "actionDomainIdentity": value.action_domain_identity,
        "pathLimit": value.path_limit,
        "frontierLimit": value.frontier_limit,
        "observationClassLimit": value.observation_class_limit,
        "calculationDiagnosticCodes": list(value.calculation_diagnostic_codes),
    }


def _interval_mapping_or_none(value: object) -> dict[str, Any] | None:
    if value is None:
        return None
    if type(value) is not Interval:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "interval is not typed")
    return _interval_mapping(value)


def _fraction_mapping_or_none(value: object) -> dict[str, int] | None:
    if value is None:
        return None
    if type(value) is not Fraction:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "exact rational is not typed")
    return _fraction_mapping(value)


def _resource_mapping(value: AlgorithmResourceView) -> dict[str, Any]:
    return {
        "mode": value.mode,
        "remaining": value.remaining,
        "declaredActionCost": value.declared_action_cost,
    }


def _history_mapping(value: object) -> dict[str, Any]:
    if not hasattr(value, "hypotheses") or not hasattr(value, "compatible_state_by_hypothesis"):
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "history projection is invalid")
    return {
        "hypotheses": sorted(value.hypotheses),
        "compatibleStateByHypothesis": {
            name: list(refs) for name, refs in sorted(value.compatible_state_by_hypothesis.items())
        },
        "statusByHypothesis": {name: status for name, status in sorted(value.status_by_hypothesis.items())},
        "version": value.version,
        "processed": value.processed,
    }


def _state_mapping(state: SessionState) -> dict[str, Any]:
    return {
        "summary": state.context.current_summary,
        "summaryStatus": state.context.q_status,
        "knownTarget": state.context.known_target,
        "knownEvidence": list(state.context.known_evidence),
        "errorHistory": list(state.context.error_history),
        "unknownHistory": list(state.context.unknown_history),
        "history": _history_mapping(state.history),
        "frontiers": {
            hypothesis: [_frontier_mapping(entry) for entry in entries]
            for hypothesis, entries in sorted(state.frontiers.items())
        },
        "resource": {"mode": state.resources.mode, "remaining": state.resources.remaining},
        "retryCount": state.context.retry_count,
        "retryCap": state.context.retry_cap,
        "attempts": state.attempts,
        "processedExecutionAttemptIds": sorted(state.processed_execution_attempt_ids),
        "consumedResponseIds": sorted(state.consumed_response_ids),
        "terminalTriggerEventIds": sorted(state.terminal_trigger_event_ids),
        "activeTriggerEventIds": sorted(state.active_trigger_event_ids),
        "eventIdentityRefs": {
            event_id: _ownership_event_mapping(event)
            for event_id, event in sorted(state.event_identity_refs.items())
        },
    }


def _frontier_mapping(entry: FrontierEntry) -> dict[str, Any]:
    return {
        "controlStateId": entry.control_state_id,
        "clockConstraints": {name: _interval_mapping(value) for name, value in sorted(entry.clocks.items())},
        "typedStore": _json_safe_mapping(entry.typed_store),
        "pathLength": entry.path_length,
        "historyProvenance": list(entry.history_provenance),
        "status": entry.status,
        "modelIdentity": entry.model_identity,
    }


def _json_safe_mapping(value: Mapping[str, Any]) -> dict[str, Any]:
    return {name: _json_safe_scalar(item) for name, item in sorted(value.items())}


def _json_safe_scalar(value: object) -> object:
    if type(value) is Fraction:
        return _fraction_mapping(value)
    if type(value) in {str, int, bool} or value is None:
        return value
    raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "finite typed-store value is not JSON scalar")


def _fraction_mapping(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "positiveDenominator": value.denominator}


def _interval_mapping(value: Interval) -> dict[str, Any]:
    return {
        "lower": _fraction_mapping(value.lower),
        "upper": _fraction_mapping(value.upper),
        "lowerClosed": value.lower_closed,
        "upperClosed": value.upper_closed,
    }


def _int_mapping(value: Mapping[str, int]) -> dict[str, int]:
    return {name: item for name, item in sorted(value.items())}


def _diagnostic_mapping(value: object) -> dict[str, str]:
    code = getattr(value, "code", None)
    message = getattr(value, "message", None)
    if type(code) is not str or type(message) is not str:
        raise EvidenceError("EVIDENCE-PROJECTION-ERROR", "diagnostic is not typed")
    return {"code": code, "message": message}


def validate_evidence_document(document: object, *, sources: EvidenceSources) -> dict[str, Any]:
    """Validate one decoded document against one independently rebuilt run.

    ``document`` is intentionally passed in, rather than read again, so shape
    and relation validation consume one decoded object.  This prevents a file
    replacement between a superficial schema check and causal replay.
    """

    if type(document) is not dict:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence must be a JSON object")
    _reject_floats(document)
    _validate_evidence_shape(document)
    _validate_integrity(document)
    if document.get("artifactType") != EVIDENCE_ARTIFACT_TYPE or document.get("schemaVersion") != EVIDENCE_SCHEMA_VERSION:
        raise EvidenceError("EVIDENCE-VERSION-ERROR", "evidence artifact type or schema version is unsupported")
    # The envelope identities are checked before source reconstruction.  A
    # package cannot select another Git path/commit and cause an unnecessary
    # verification execution before receiving its named source rejection.
    actual_inputs = document.get("inputs")
    expected_inputs = sources.identities()
    if _first_difference(actual_inputs, expected_inputs, "$.inputs"):
        raise EvidenceError("EVIDENCE-SOURCE-MISMATCH", "evidence source identities differ from the explicit Git inputs")
    expected_run = run_scenario(sources)
    expected = evidence_document(expected_run)
    # Integrity is already independently checked against the supplied
    # canonical payload.  Compare the semantic payload without the derived
    # digest so a coordinated, self-consistent mutation is located at the
    # actual action/raw/history field.  ``_first_difference`` remains exact
    # about types, unlike ordinary Python dict equality (where True == 1).
    actual_payload = {key: value for key, value in document.items() if key != "integrity"}
    expected_payload = {key: value for key, value in expected.items() if key != "integrity"}
    path = _first_difference(actual_payload, expected_payload)
    if path:
        raise EvidenceError("EVIDENCE-RELATION-MISMATCH", f"evidence does not match the rebuilt finite run at {path}")
    return expected


def _validate_evidence_shape(document: dict[str, Any], *, checkpoint: bool = False) -> None:
    """Reject an incomplete or open envelope before relation replay.

    The exact nested relation is still checked against a fresh production run
    below.  This bounded front gate makes malformed documents fail with a
    stable shape diagnostic instead of asking a relation comparator to infer a
    missing top-level contract.
    """

    required = {
        "artifactType", "schemaVersion", "boundary", "inputs", "run", "rounds", "producerFacts", "outcome", "integrity",
    }
    if checkpoint:
        required.add("checkpoint")
    if set(document) != required:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence has unknown or missing top-level fields")
    boundary = document["boundary"]
    if type(boundary) is not dict or set(boundary) != {
        "purpose", "conformanceVerdict", "runtimeIntegrity", "externalOpaqueSource",
    }:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence boundary declaration is invalid")
    if boundary != {
        "purpose": "SYNTHETIC-ENGINEERING-VALIDATION",
        "conformanceVerdict": "NOT-EVALUATED",
        "runtimeIntegrity": "NOT-ESTABLISHED",
        "externalOpaqueSource": "UNSUPPORTED-FOR-QUALIFIED-REPLAY",
    }:
        raise EvidenceError("EVIDENCE-BOUNDARY-ERROR", "evidence boundary declaration is not the finite synthetic boundary")
    inputs = document["inputs"]
    if type(inputs) is not dict or set(inputs) != {"development", "interfaceRegistry", "scenario"}:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence source identity mapping is invalid")
    for label, identity in inputs.items():
        if type(identity) is not dict or set(identity) != {"commit", "path", "blobSha256"} or any(
            type(identity.get(field)) is not str or not identity[field]
            for field in ("commit", "path", "blobSha256")
        ):
            raise EvidenceError("EVIDENCE-SHAPE-ERROR", f"evidence {label} identity is invalid")
    run = document["run"]
    if type(run) is not dict or set(run) != {
        "scenarioId", "sessionId", "runId", "resetId", "maximumRounds", "producerMode",
    }:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence run identity is invalid")
    if (
        any(type(run.get(field)) is not str or not run[field] for field in ("scenarioId", "sessionId", "runId", "producerMode"))
        or run["resetId"] is not None
        or type(run["maximumRounds"]) is not int
        or run["maximumRounds"] < 1
    ):
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence run fields are invalid")
    if type(document["rounds"]) is not list or type(document["producerFacts"]) is not list:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence round/fact collections are invalid")
    for fact in document["producerFacts"]:
        if type(fact) is not dict or set(fact) != {
            "producerId", "producerProtocol", "runtimeDistribution", "runtimeVersion", "runId", "sessionId", "attemptId", "issuedActionId", "actionKind", "stage", "fact",
        } or any(type(value) is not str or not value for value in fact.values()):
            raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence producer fact is invalid")
    outcome = document["outcome"]
    if type(outcome) is not dict or set(outcome) != {"stopReason", "diagnostics", "state"}:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence outcome is invalid")
    if outcome["stopReason"] is not None and (type(outcome["stopReason"]) is not str or not outcome["stopReason"]):
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence stop reason is invalid")
    if type(outcome["diagnostics"]) is not list or type(outcome["state"]) is not dict:
        raise EvidenceError("EVIDENCE-SHAPE-ERROR", "evidence outcome records are invalid")
    if checkpoint:
        prefix = document["checkpoint"]
        if type(prefix) is not dict or set(prefix) != {"prefixRounds", "sourceMaximumRounds", "status"}:
            raise EvidenceError("CHECKPOINT-SHAPE-ERROR", "checkpoint boundary is invalid")
        if (
            type(prefix["prefixRounds"]) is not int
            or prefix["prefixRounds"] < 1
            or type(prefix["sourceMaximumRounds"]) is not int
            or prefix["sourceMaximumRounds"] < 2
            or prefix["prefixRounds"] >= prefix["sourceMaximumRounds"]
            or prefix["status"] != "OPEN-PREFIX"
        ):
            raise EvidenceError("CHECKPOINT-SHAPE-ERROR", "checkpoint progress fields are invalid")


def validate_evidence_bytes(raw: bytes, *, sources: EvidenceSources) -> dict[str, Any]:
    """Decode once, then run structural and production relation validation."""

    return validate_evidence_document(load_evidence_bytes(raw), sources=sources)


def validate_checkpoint_document(document: object, *, sources: EvidenceSources) -> VerifiedCheckpoint:
    """Validate a durable prefix and rebuild a typed continuation boundary.

    The document supplies only a bounded declaration and its observed
    projection.  The returned state/environment come from a new actual run of
    the explicit Git sources through exactly the declared prefix; no evidence
    JSON is deserialised into runtime objects.
    """

    if type(document) is not dict:
        raise EvidenceError("CHECKPOINT-SHAPE-ERROR", "checkpoint must be a JSON object")
    _reject_floats(document)
    _validate_evidence_shape(document, checkpoint=True)
    _validate_integrity(document)
    if (
        document.get("artifactType") != CHECKPOINT_ARTIFACT_TYPE
        or document.get("schemaVersion") != CHECKPOINT_SCHEMA_VERSION
    ):
        raise EvidenceError("CHECKPOINT-VERSION-ERROR", "checkpoint artifact type or schema version is unsupported")
    actual_inputs = document.get("inputs")
    expected_inputs = sources.identities()
    if _first_difference(actual_inputs, expected_inputs, "$.inputs"):
        raise EvidenceError("EVIDENCE-SOURCE-MISMATCH", "checkpoint source identities differ from the explicit Git inputs")
    prefix = document["checkpoint"]
    assert type(prefix) is dict  # established by the closed shape gate above.
    rebuilt = create_checkpoint(sources, prefix_rounds=prefix["prefixRounds"])
    expected = checkpoint_document(rebuilt)
    actual_payload = {key: value for key, value in document.items() if key != "integrity"}
    expected_payload = {key: value for key, value in expected.items() if key != "integrity"}
    path = _first_difference(actual_payload, expected_payload)
    if path:
        raise EvidenceError("CHECKPOINT-RELATION-MISMATCH", f"checkpoint does not match the rebuilt finite prefix at {path}")
    return _verified_checkpoint(rebuilt)


def validate_checkpoint_bytes(raw: bytes, *, sources: EvidenceSources) -> VerifiedCheckpoint:
    """Decode a canonical checkpoint once, then rebuild its trusted prefix."""

    return validate_checkpoint_document(load_checkpoint_bytes(raw), sources=sources)


def _validate_integrity(document: dict[str, Any]) -> None:
    integrity = document.get("integrity")
    if type(integrity) is not dict or set(integrity) != {"canonicalPayloadSha256"}:
        raise EvidenceError("EVIDENCE-INTEGRITY-ERROR", "evidence integrity record is invalid")
    digest = integrity.get("canonicalPayloadSha256")
    if type(digest) is not str or len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise EvidenceError("EVIDENCE-INTEGRITY-ERROR", "evidence integrity digest is invalid")
    payload = {key: value for key, value in document.items() if key != "integrity"}
    expected = sha256(canonical_json_bytes(payload)).hexdigest()
    if digest != expected:
        raise EvidenceError("EVIDENCE-INTEGRITY-ERROR", "evidence integrity digest does not match its canonical payload")


def _first_difference(actual: object, expected: object, path: str = "$") -> str:
    """Return a stable, bounded diagnostic location for a relation mismatch."""

    if type(actual) is not type(expected):
        return path
    if isinstance(actual, dict):
        keys = sorted(set(actual) | set(expected))
        for key in keys:
            if key not in actual or key not in expected:
                return f"{path}.{key}"
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return ""
    if isinstance(actual, list):
        if len(actual) != len(expected):
            return f"{path}.length"
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            difference = _first_difference(left, right, f"{path}[{index}]")
            if difference:
                return difference
        return ""
    return "" if actual == expected else path


def publish_run(run: EvidenceRun, *, output: Path, replace_fn: Callable[[Path, Path], None] = os.replace) -> dict[str, Any]:
    """Stage, revalidate, then transactionally publish a generated evidence file."""

    document = evidence_document(run)
    encoded = canonical_json_bytes(document)

    def stage_validator(raw: bytes) -> None:
        validate_evidence_bytes(raw, sources=run.sources)

    _publish_bytes(encoded, output=output, sources=run.sources, validator=stage_validator, replace_fn=replace_fn)
    return document


def publish_checkpoint(
    checkpoint: CheckpointRun,
    *,
    output: Path,
    replace_fn: Callable[[Path, Path], None] = os.replace,
) -> VerifiedCheckpoint:
    """Atomically publish and validate an open prefix before it can continue."""

    checkpoint = _require_checkpoint_run(checkpoint)
    document = checkpoint_document(checkpoint)
    encoded = canonical_json_bytes(document)

    def stage_validator(raw: bytes) -> None:
        validate_checkpoint_bytes(raw, sources=checkpoint.sources)

    _publish_bytes(
        encoded,
        output=output,
        sources=checkpoint.sources,
        validator=stage_validator,
        replace_fn=replace_fn,
    )
    # The staged package has been independently rebuilt and compared before
    # any target replacement.  Retain the original live prefix for the
    # "same" continuation case; a caller that rereads the file receives a
    # separate fresh reconstruction through ``validate_checkpoint_bytes``.
    return _verified_checkpoint(checkpoint)


def _publish_bytes(
    raw: bytes,
    *,
    output: Path,
    sources: EvidenceSources,
    validator: Callable[[bytes], None],
    replace_fn: Callable[[Path, Path], None] = os.replace,
) -> None:
    """Publish only a fully validated staged file, with byte-preserving rollback."""

    target = _safe_output_target(output, sources.repository)
    parent = target.parent
    stage = parent / f".{target.name}.staging-{uuid4().hex}"
    backup = parent / f".{target.name}.backup-{uuid4().hex}"
    moved_old = False
    try:
        with stage.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        # This is intentionally a real file round trip before any target move.
        validator(stage.read_bytes())
        if target.exists():
            _assert_owned_target(target, validator=validator)
            replace_fn(target, backup)
            moved_old = True
        replace_fn(stage, target)
    except EvidenceError:
        raise
    except OSError as exc:
        if moved_old and backup.exists() and not target.exists():
            try:
                replace_fn(backup, target)
            except OSError as rollback_exc:
                raise EvidenceError("EVIDENCE-ROLLBACK-ERROR", "evidence replacement failed and rollback did not complete") from rollback_exc
        raise EvidenceError("EVIDENCE-PUBLISH-ERROR", "evidence publication could not complete") from exc
    finally:
        if stage.exists():
            stage.unlink()
    if backup.exists():
        backup.unlink()


def _safe_output_target(output: Path, repository: Path) -> Path:
    """Reject source overlap, links and broad/repository targets before staging."""

    if not isinstance(output, Path) or not output.name or output.name in {".", ".."}:
        raise EvidenceError("UNSAFE-OUTPUT-PATH", "evidence output path is invalid")
    try:
        # Resolve only after checking the requested path components.  Calling
        # ``resolve`` on the final name first would erase the evidence that an
        # attacker supplied a symlink to an otherwise ordinary file.
        requested_parent = output.parent.absolute()
        if not requested_parent.is_dir() or any(
            component.is_symlink() for component in (requested_parent, *requested_parent.parents)
        ):
            raise EvidenceError("UNSAFE-OUTPUT-PATH", "evidence output parent must be an ordinary existing directory")
        parent = requested_parent.resolve(strict=True)
        target = parent / output.name
        repo = repository.resolve(strict=True)
    except OSError as exc:
        raise EvidenceError("UNSAFE-OUTPUT-PATH", "evidence output path cannot be resolved") from exc
    # ``Path.exists`` is false for a dangling link on some platforms, so test
    # the link itself independently.  A failed first publication must not
    # turn a user-supplied link into a staging or replacement target.
    if target.is_symlink() or (target.exists() and not target.is_file()):
        raise EvidenceError("UNSAFE-OUTPUT-PATH", "evidence output target must be an ordinary file")
    try:
        target.relative_to(repo)
    except ValueError:
        return target
    raise EvidenceError("UNSAFE-OUTPUT-PATH", "evidence output must not be inside the authority repository")


def _assert_owned_target(target: Path, *, validator: Callable[[bytes], None]) -> None:
    """Do not replace arbitrary user files merely because the path exists.

    The ownership relation is artifact-specific: an evidence publisher may
    replace only a valid evidence file for the same source authority, while a
    checkpoint publisher may replace only its corresponding checkpoint.
    """

    try:
        validator(target.read_bytes())
    except (OSError, EvidenceError) as exc:
        raise EvidenceError("UNSAFE-OUTPUT-PATH", "refusing to replace a file not owned by this finite artifact publisher") from exc
