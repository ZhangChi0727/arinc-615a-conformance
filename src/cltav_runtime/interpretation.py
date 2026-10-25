"""Bounded ownership and timing interpretation for the reference runtime.

The public environment owns only raw observation material.  The session owns
the immutable interpretation contract: trigger/response encoding, ownership
policy, measurement domain, error basis, and any deadline authority.  Keeping
those two inputs separate prevents a synthetic fixture from self-certifying a
deadline or changing how its own events are interpreted.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from types import MappingProxyType
from typing import Mapping

from .kernel import Interval, KernelDiagnostic


_EVENT_KINDS = frozenset({"REQUEST", "RESPONSE", "CANCEL", "SUPERSEDE"})
_POLICIES = frozenset({"UNIQUE-KEY", "FIFO", "MOST-RECENT"})
_DEADLINE_AUTHORITIES = frozenset({"REVIEWED", "METHOD-ONLY", "UNRESOLVED"})


@dataclass(frozen=True)
class OwnershipEvent:
    """One ordered public event.  Validation occurs at the public adapter."""

    event_id: object
    sequence: object
    kind: object
    key: object
    event_type: object
    timestamp: object
    target_request_id: object | None = None


@dataclass(frozen=True)
class OwnershipOrderBoundary:
    """Immutable high-water mark for an already processed ownership prefix.

    The scalar high-water values fence new controlled events; the retained
    identity set preserves the distinct handling of an old terminal receipt.
    It is not a substitute for the retained ACTIVE-request seed: the seed
    determines who may own a new response, whereas this boundary prevents a
    newly disclosed controlled event from being inserted before an already
    processed response or termination.
    """

    sequence: object
    timestamp: object
    retained_event_ids: object = frozenset()


@dataclass(frozen=True)
class InterpretationContract:
    """Controlled method contract consumed by one bounded session.

    ``METHOD-ONLY`` may carry a finite teaching boundary, but it cannot create
    a scored protocol no-response conclusion in :class:`ReferenceSession`.
    The runtime has no registry of reviewed protocol deadlines in this slice,
    so a session rejects ``REVIEWED`` contracts rather than letting a fixture
    manufacture that authority.
    """

    contract_id: object
    trigger_event_type: object
    response_event_type: object
    key: object
    policy: object
    concurrent_same_key: object
    cancellation_event_type: object
    supersession_event_type: object
    physical_domain: object
    requirement_window: object
    clock_identity: object
    uncertainty_identity: object
    error_budget_identity: object
    unit: object
    clock_valid: object = True
    error_budget_valid: object = True
    deadline_authority: object = "METHOD-ONLY"
    deadline_identity: object | None = None
    upper_bound: object | None = None
    upper_closed: object = True


@dataclass(frozen=True)
class ObservationInput:
    """Raw public material attached to one execution record.

    The declaration parser leaves the last six identity fields ``None``.  A
    synthetic environment binds them from the actual issued execution record
    just before returning it; a session then verifies that binding before any
    ownership or timing conclusion can affect its evidence ledger.
    """

    events: object
    trigger_event_id: object
    response_id: object | None
    measurement_interval: object | None
    observation_end_qualified: object
    earliest_elapsed: object | None
    clock_identity: object
    unit: object
    execution_attempt_id: object | None = None
    action_id: object | None = None
    evidence_ref: object | None = None
    measurement_tick: object | None = None
    uncertainty_identity: object | None = None


@dataclass(frozen=True)
class OwnershipResolution:
    """One response result from one complete replay."""

    response_id: str
    status: str
    owner_request_id: str | None
    candidate_request_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    diagnostics: tuple[KernelDiagnostic, ...] = ()


@dataclass(frozen=True)
class OwnershipReplay:
    """Frozen single-replay ownership output shared by T5 and silence."""

    contract_id: str | None
    request_dispositions: Mapping[str, str]
    termination_refs: Mapping[str, str]
    response_resolutions: Mapping[str, OwnershipResolution]
    event_refs: Mapping[str, OwnershipEvent]
    diagnostics: tuple[KernelDiagnostic, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_dispositions", MappingProxyType(dict(self.request_dispositions)))
        object.__setattr__(self, "termination_refs", MappingProxyType(dict(self.termination_refs)))
        object.__setattr__(self, "response_resolutions", MappingProxyType(dict(self.response_resolutions)))
        object.__setattr__(self, "event_refs", MappingProxyType(dict(self.event_refs)))
        object.__setattr__(self, "diagnostics", tuple(self.diagnostics))


@dataclass(frozen=True)
class ObservationAssessment:
    """Typed, replayable four-valued timing assessment.

    ``verdict`` is always in ``PASS/FAIL/INCONCLUSIVE/ERROR``.  Whether a
    result is a scored answer, a pending deadline, a cancelled obligation, or
    an engineering-only witness is represented solely by ``score_disposition``
    and ``kind``; pending/administrative states never leak into the verdict
    vocabulary.
    """

    kind: str
    verdict: str
    score_disposition: str
    answered: bool
    reason: str
    contract_id: str | None
    execution_attempt_id: str | None
    action_id: str | None
    evidence_ref: str | None
    trigger_event_id: str | None
    response_id: str | None
    ownership: OwnershipResolution | None
    # The complete replay is retained with the selected assessment.  A TEST
    # record may name one response while its finite trace contains other
    # response/termination facts; the session ledger must consume that whole
    # checked replay, not only the selected response ID.
    replay: OwnershipReplay | None
    measurement_interval: Interval | None
    physical_interval: Interval | None
    requirement_window: Interval | None
    clock_identity: str | None
    uncertainty_identity: str | None
    error_budget_identity: str | None
    unit: str | None
    deadline_identity: str | None
    evidence_refs: tuple[str, ...]
    diagnostics: tuple[KernelDiagnostic, ...] = ()


def observation_input_from_mapping(value: object) -> ObservationInput:
    """Decode raw synthetic material and reject an injected interpretation.

    Deliberately absent are policy, deadline, physical domain, requirement
    window, clock-valid flag, error-budget validity, and expected verdict.
    Those are controlled by :class:`InterpretationContract`, not by an
    environment declaration.
    """

    required = {
        "events", "triggerEventId", "responseId", "measurementInterval",
        "observationEndQualified", "earliestElapsed", "clockIdentity", "unit",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise ValueError("synthetic observation material uses unknown or missing fields")
    if not isinstance(value["events"], list):
        raise ValueError("synthetic observation events must be an array")
    events: list[OwnershipEvent] = []
    for item in value["events"]:
        if not isinstance(item, Mapping) or not set(item) <= {
            "id", "sequence", "kind", "key", "eventType", "timestamp", "targetRequestId",
        } or not {"id", "sequence", "kind", "key", "eventType", "timestamp"} <= set(item):
            raise ValueError("synthetic ownership event uses unknown or missing fields")
        events.append(OwnershipEvent(
            item["id"], item["sequence"], item["kind"], item["key"], item["eventType"],
            _fraction_from_public(item["timestamp"]), item.get("targetRequestId"),
        ))
    interval = value["measurementInterval"]
    return ObservationInput(
        tuple(events), value["triggerEventId"], value["responseId"],
        None if interval is None else _interval_from_public(interval),
        value["observationEndQualified"],
        None if value["earliestElapsed"] is None else _fraction_from_public(value["earliestElapsed"]),
        value["clockIdentity"], value["unit"],
    )


def bind_observation_input(
    value: ObservationInput,
    *,
    execution_attempt_id: str,
    action_id: str,
    evidence_ref: str,
    measurement_tick: Fraction | None,
    uncertainty_identity: str | None,
) -> ObservationInput:
    """Bind raw material to the actual public execution record exactly once."""

    if type(value) is not ObservationInput:
        raise ValueError("observation material must be an ObservationInput")
    return replace(
        value,
        execution_attempt_id=execution_attempt_id,
        action_id=action_id,
        evidence_ref=evidence_ref,
        measurement_tick=measurement_tick,
        uncertainty_identity=uncertainty_identity,
    )


def replay_ownership(
    events: object,
    contract: object,
    *,
    prior_active_requests: Mapping[str, OwnershipEvent] | None = None,
    prior_order_boundary: OwnershipOrderBoundary | None = None,
) -> OwnershipReplay:
    """Replay one finite public trace under one controlled contract.

    Each matching request event creates exactly one logical obligation instance;
    a fixture cannot register two IDs for one request or choose a different
    policy for the same response.  Ordering is both trace-order and monotonic
    virtual-clock order, so a cancellation cannot target a future request.

    ``prior_active_requests`` is a session-derived finite context, not raw
    trace material.  It permits a legal incremental next observation to omit
    already retained terminal receipts while still making every new ownership
    decision against the live obligations.  ``prior_order_boundary`` is a
    separately derived high-water mark from the verified retained ledger:
    exact reappearance of a seeded ACTIVE request is confirmation only, but
    every newly introduced controlled request, response, or termination must
    be globally later than that processed prefix.  The returned ``event_refs``
    stays raw-delta-only; request dispositions include the seeded ACTIVE
    instances so a session can advance its persistent ledger without
    inventing history.
    """

    parsed_events, event_errors = _parse_events(events)
    parsed_contract, contract_errors = _parse_contract(contract)
    diagnostics = list(event_errors) + list(contract_errors)
    event_refs = {event.event_id: event for event in parsed_events}
    contract_id = parsed_contract.contract_id if parsed_contract is not None else None
    prior_active: dict[str, OwnershipEvent] = {}
    order_boundary: OwnershipOrderBoundary | None = None
    controlled_request_ids: set[str] = set()
    seeded_identifiers = frozenset()
    if parsed_contract is not None:
        prior_active, seed_errors = _parse_active_seed(prior_active_requests, parsed_contract)
        diagnostics.extend(seed_errors)
        order_boundary, boundary_errors = _parse_order_boundary(
            prior_order_boundary,
            prior_active,
        )
        diagnostics.extend(boundary_errors)
        for event in parsed_events:
            retained = prior_active.get(event.event_id)
            if retained is not None and (
                event.kind != "REQUEST" or not _strict_event_equal(event, retained)
            ):
                diagnostics.append(KernelDiagnostic(
                    "OWNERSHIP-SEED-EVENT-CONFLICT",
                    "raw trace reuses a retained active request identity with a different public event",
                ))
        # Even when one raw item is malformed, every successfully parsed
        # event remains a proposed public fact.  Check those values against
        # the retained high-water boundary before returning the parse error;
        # otherwise an invalid item could mask an earlier backfill and let the
        # session retain it through its ordinary S7 ledger path.
        controlled_request_ids = set(prior_active) | {
            event.event_id
            for event in parsed_events
            if _request_matches_contract(event, parsed_contract)
        }
        seeded_identifiers = frozenset(prior_active)
        if not seed_errors and not boundary_errors:
            for event in parsed_events:
                retained = prior_active.get(event.event_id)
                exact_active_confirmation = (
                    retained is not None
                    and event.kind == "REQUEST"
                    and _strict_event_equal(event, retained)
                )
                if (
                    order_boundary is not None
                    and event.event_id in order_boundary.retained_event_ids
                    and not exact_active_confirmation
                ):
                    diagnostics.append(KernelDiagnostic(
                        "RETAINED-OWNERSHIP-EVENT-REPLAY",
                        "a retained terminal ownership event cannot be introduced again in a later delta",
                    ))
                    continue
                if (
                    order_boundary is not None
                    and not exact_active_confirmation
                    and _is_order_controlled_event(
                        event,
                        parsed_contract,
                        controlled_request_ids,
                    )
                    and (
                        event.sequence <= order_boundary.sequence
                        or event.timestamp < order_boundary.timestamp
                    )
                ):
                    diagnostics.append(KernelDiagnostic(
                        "INSUFFICIENT-OWNERSHIP-CONTEXT",
                        "a newly introduced controlled event precedes the retained global ownership order frontier",
                    ))
    if diagnostics or parsed_contract is None:
        return OwnershipReplay(contract_id, {}, {}, {}, event_refs, tuple(diagnostics))

    active: set[str] = set(prior_active)
    dispositions: dict[str, str] = {identifier: "ACTIVE" for identifier in prior_active}
    termination_refs: dict[str, str] = {}
    resolutions: dict[str, OwnershipResolution] = {}
    known_requests: dict[str, OwnershipEvent] = dict(prior_active)
    # An other-key termination is normally irrelevant to this controlled
    # request/response contract.  Decide that only after seeing the complete
    # finite raw trace: otherwise a foreign cancellation placed *before* a
    # later matching request with the same target ID could be silently
    # discarded and the future controlled request would escape validation.
    # ``controlled_request_ids`` was derived before the early-return gate so
    # the same complete parsed trace supplies the order preflight above and
    # the semantic replay below.  It deliberately contains only contract
    # requests (plus the retained ACTIVE seed), so a fully unrelated
    # transaction remains admissible.

    for event in parsed_events:
        if event.kind == "REQUEST":
            if not _request_matches_contract(event, parsed_contract):
                continue
            prior = known_requests.get(event.event_id)
            if prior is not None:
                if event.event_id in seeded_identifiers and _strict_event_equal(event, prior):
                    # A complete cumulative trace may repeat a retained
                    # ACTIVE request verbatim.  It is context confirmation,
                    # not a second obligation instance.
                    continue
                diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-TRACE", "matching request identity is duplicated"))
                continue
            if event.target_request_id is not None:
                terminated = _terminate_request(
                    event.target_request_id, event, active, dispositions, termination_refs,
                    known_requests, parsed_contract, diagnostics, "SUPERSEDED",
                    require_active=True,
                )
                # A replacement request may establish a non-concurrent
                # successor only by actually terminating its declared live
                # predecessor.  A stale/cancelled/discharged target is not a
                # harmless no-op admission token.
                if not terminated:
                    continue
            if not parsed_contract.concurrent_same_key and active:
                diagnostics.append(KernelDiagnostic(
                    "IMPLICIT-OWNERSHIP-SUPERSESSION",
                    "a non-concurrent request requires an explicit supersession target",
                ))
                continue
            known_requests[event.event_id] = event
            active.add(event.event_id)
            dispositions[event.event_id] = "ACTIVE"
            continue

        if event.kind in {"CANCEL", "SUPERSEDE"}:
            # Events for another contract key may form a complete, valid
            # transaction in the same raw capture.  They are outside this
            # contract's ownership replay unless they claim to terminate one
            # of its retained requests; in that case keep validating the
            # cross-key attempt instead of silently ignoring it.  The target
            # can occur later in this same trace, so use the complete
            # controlled request set rather than only the requests replayed
            # so far.
            if event.key != parsed_contract.key:
                if event.target_request_id not in controlled_request_ids:
                    continue
            expected_type = (
                parsed_contract.cancellation_event_type
                if event.kind == "CANCEL" else parsed_contract.supersession_event_type
            )
            if event.event_type != expected_type:
                diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-TERMINATION", "termination event type is outside the controlled contract"))
                continue
            assert isinstance(event.target_request_id, str)
            _terminate_request(
                event.target_request_id, event, active, dispositions, termination_refs,
                known_requests, parsed_contract, diagnostics,
                "CANCELLED" if event.kind == "CANCEL" else "SUPERSEDED",
            )
            continue

        if event.kind != "RESPONSE":
            continue
        candidates = tuple(sorted(
            (identifier for identifier in active if _response_matches(event, known_requests[identifier], parsed_contract)),
            key=lambda identifier: known_requests[identifier].sequence,
        ))
        if not candidates:
            resolutions[event.event_id] = OwnershipResolution(event.event_id, "UNMATCHED", None, (), (event.event_id,), ())
            continue
        refs = (event.event_id,) + candidates
        if parsed_contract.policy == "UNIQUE-KEY" and len(candidates) > 1:
            diagnostic = KernelDiagnostic("AMBIGUOUS-OWNERSHIP", "more than one active request remains under UNIQUE-KEY")
            resolutions[event.event_id] = OwnershipResolution(event.event_id, "AMBIGUOUS", None, candidates, refs, (diagnostic,))
            for identifier in candidates:
                dispositions[identifier] = "AMBIGUOUS"
                termination_refs[identifier] = event.event_id
                active.remove(identifier)
            continue
        owner = candidates[-1] if parsed_contract.policy == "MOST-RECENT" else candidates[0]
        resolutions[event.event_id] = OwnershipResolution(event.event_id, "UNIQUE", owner, candidates, refs, ())
        dispositions[owner] = "DISCHARGED"
        termination_refs[owner] = event.event_id
        active.remove(owner)

    return OwnershipReplay(contract_id, dispositions, termination_refs, resolutions, event_refs, tuple(diagnostics))


def assess_observation(
    value: object,
    contract: object,
    *,
    prior_active_requests: Mapping[str, OwnershipEvent] | None = None,
    prior_order_boundary: OwnershipOrderBoundary | None = None,
) -> ObservationAssessment:
    """Assess raw material against a controlled, immutable contract.

    This public entry never throws for malformed nested values: malformed
    intervals, bool/int substitutions, unit mismatches, malformed clocks and
    trace errors all become a named ``ERROR`` assessment.
    """

    parsed_contract, contract_errors = _parse_contract(contract)
    if parsed_contract is None:
        return _error_assessment("INVALID-INTERPRETATION-CONTRACT", "interpretation contract is invalid", diagnostics=contract_errors)
    if type(value) is not ObservationInput:
        return _error_assessment("INVALID-OBSERVATION-INPUT", "observation input is not a typed ObservationInput", contract=parsed_contract)
    # Ownership is independently replayable even when a later input-domain
    # validation fails.  Retaining that typed replay prevents a malformed
    # clock/unit/measurement field from reopening a response or request that
    # has already appeared in the public trace.
    replay = replay_ownership(
        value.events,
        parsed_contract,
        prior_active_requests=prior_active_requests,
        prior_order_boundary=prior_order_boundary,
    )
    # The same normalized finite seed is used only to resolve a retained
    # active trigger and its timestamp.  It is deliberately not copied into
    # ``replay.event_refs``: that mapping remains the raw evidence delta.
    active_seed, _seed_errors = _parse_active_seed(
        prior_active_requests,
        parsed_contract,
    )
    input_error = _input_error(value, parsed_contract)
    if input_error is not None:
        return _error_assessment(
            input_error.code, input_error.message, contract=parsed_contract,
            input_value=value, replay=replay, diagnostics=replay.diagnostics,
        )
    if replay.diagnostics:
        return _error_assessment(
            "INVALID-OWNERSHIP-TRACE", "ownership trace is invalid", contract=parsed_contract,
            input_value=value, replay=replay, diagnostics=replay.diagnostics,
            evidence_refs=tuple(replay.event_refs),
        )
    assert isinstance(value.trigger_event_id, str)
    trigger = replay.event_refs.get(value.trigger_event_id)
    if trigger is None:
        trigger = active_seed.get(value.trigger_event_id)
    if trigger is None or not _request_matches_contract(trigger, parsed_contract):
        return _error_assessment(
            "UNKNOWN-TRIGGER", "observation does not name a contract-matching request event",
            contract=parsed_contract, input_value=value, replay=replay,
            evidence_refs=tuple(replay.event_refs),
        )
    if value.response_id is None:
        # A raw declaration of silence cannot discard an already visible,
        # contract-matching response.  This is deliberately checked before the
        # deadline-authority branch: a METHOD-ONLY boundary may make a genuine
        # silence inconclusive, but it must never mask malformed material.
        if any(
            resolution.status == "UNIQUE"
            and resolution.owner_request_id == value.trigger_event_id
            for resolution in replay.response_resolutions.values()
        ):
            return _error_assessment(
                "RESPONSE-PRESENT-DECLARED-SILENCE",
                "no-response material contains a response owned by its selected trigger",
                contract=parsed_contract,
                input_value=value,
                replay=replay, evidence_refs=tuple(replay.event_refs),
            )
        return _assess_no_response(
            value,
            replay,
            parsed_contract,
            prior_active_requests=active_seed,
        )
    assert isinstance(value.response_id, str)
    resolution = replay.response_resolutions.get(value.response_id)
    if resolution is None:
        return _error_assessment(
            "UNKNOWN-RESPONSE", "assessment response identity is absent from the replay",
            contract=parsed_contract, input_value=value, replay=replay,
            evidence_refs=tuple(replay.event_refs),
        )
    if resolution.status != "UNIQUE" or resolution.owner_request_id != value.trigger_event_id:
        return _error_assessment(
            "OWNERSHIP-ERROR", "response is not uniquely owned by the selected trigger",
            contract=parsed_contract, input_value=value, ownership=resolution,
            replay=replay, evidence_refs=resolution.evidence_refs,
        )
    return _assess_t5(
        value,
        parsed_contract,
        resolution,
        replay,
        prior_active_requests=active_seed,
    )


def _assess_t5(
    value: ObservationInput,
    contract: InterpretationContract,
    ownership: OwnershipResolution,
    replay: OwnershipReplay,
    *,
    prior_active_requests: Mapping[str, OwnershipEvent] | None = None,
) -> ObservationAssessment:
    if contract.clock_valid is not True:
        return _error_assessment("INVALID-CLOCK-CHAIN", "owned response has no valid controlled clock chain", contract=contract, input_value=value, ownership=ownership, replay=replay, evidence_refs=ownership.evidence_refs)
    if contract.error_budget_valid is not True:
        return _error_assessment("INVALID-ERROR-BUDGET", "owned response has no valid controlled error basis", contract=contract, input_value=value, ownership=ownership, replay=replay, evidence_refs=ownership.evidence_refs)
    measurement, measurement_error = _validated_interval(value.measurement_interval)
    if measurement_error is not None or measurement is None:
        return _error_assessment("INVALID-MEASUREMENT-INTERVAL", "T5 requires one nonempty exact measurement interval", contract=contract, input_value=value, ownership=ownership, replay=replay, evidence_refs=ownership.evidence_refs)
    assert isinstance(value.measurement_tick, Fraction)
    if not _interval_contains(measurement, value.measurement_tick):
        return _error_assessment("MEASUREMENT-TICK-MISMATCH", "record measurement tick is outside its public measurement interval", contract=contract, input_value=value, ownership=ownership, replay=replay, evidence_refs=ownership.evidence_refs)
    trigger = replay.event_refs.get(ownership.owner_request_id)
    if trigger is None and prior_active_requests is not None:
        trigger = prior_active_requests.get(ownership.owner_request_id)
    response = replay.event_refs.get(ownership.response_id)
    if type(trigger) is not OwnershipEvent or type(response) is not OwnershipEvent:
        return _error_assessment(
            "MEASUREMENT-EVENT-DELTA-MISMATCH",
            "owned response has no complete timestamped trigger/response evidence",
            contract=contract,
            input_value=value,
            ownership=ownership,
            replay=replay,
            evidence_refs=ownership.evidence_refs,
        )
    if value.measurement_tick != response.timestamp - trigger.timestamp:
        return _error_assessment(
            "MEASUREMENT-EVENT-DELTA-MISMATCH",
            "record measurement tick does not equal the owned response-minus-trigger event delta",
            contract=contract,
            input_value=value,
            ownership=ownership,
            replay=replay,
            evidence_refs=ownership.evidence_refs,
        )
    physical = measurement.intersect(contract.physical_domain)
    if physical is None:
        return _error_assessment("EMPTY-PHYSICAL-MEASUREMENT-DOMAIN", "measurement interval has no physical-domain intersection", contract=contract, input_value=value, ownership=ownership, replay=replay, measurement_interval=measurement, evidence_refs=ownership.evidence_refs)
    overlap = physical.intersect(contract.requirement_window)
    if _contains(contract.requirement_window, physical):
        verdict, reason = "PASS", "measurement interval is wholly contained in the requirement interval"
    elif overlap is None:
        verdict, reason = "FAIL", "measurement interval is separated from the requirement interval"
    else:
        verdict, reason = "INCONCLUSIVE", "measurement interval overlaps a requirement boundary"
    # ``answered`` is not a synonym for “the interpreter returned a value”.
    # It denotes a scored protocol answer and therefore cannot be true for an
    # interval that straddles a boundary.  METHOD-ONLY contracts are retained
    # only as engineering witnesses even when they calculate PASS or FAIL.
    answered = contract.deadline_authority == "REVIEWED" and verdict in {"PASS", "FAIL"}
    return _assessment(
        kind="T5", verdict=verdict,
        score_disposition=(
            "ANSWERED" if answered else (
                "INCONCLUSIVE" if contract.deadline_authority == "REVIEWED" else "ENGINEERING-WITNESS"
            )
        ),
        answered=answered, reason=reason, contract=contract, input_value=value, ownership=ownership,
        measurement_interval=measurement, physical_interval=physical,
        requirement_window=contract.requirement_window, replay=replay,
        evidence_refs=ownership.evidence_refs,
    )


def _assess_no_response(
    value: ObservationInput,
    replay: OwnershipReplay,
    contract: InterpretationContract,
    *,
    prior_active_requests: Mapping[str, OwnershipEvent] | None = None,
) -> ObservationAssessment:
    assert isinstance(value.trigger_event_id, str)
    disposition = replay.request_dispositions.get(value.trigger_event_id)
    refs = [value.trigger_event_id]
    termination = replay.termination_refs.get(value.trigger_event_id)
    if termination is not None:
        refs.append(termination)
    # Even an administrative cancellation/supersession uses timestamped
    # evidence to decide whether it can end a reviewed obligation.  Validate
    # the controlled time/error basis before any disposition may turn that
    # question into NOT-APPLICABLE; otherwise an invalid chain could silently
    # hide a boundary-dependent no-response conclusion.
    if contract.clock_valid is not True:
        return _error_assessment("INVALID-CLOCK-CHAIN", "no-response horizon has no valid controlled clock chain", contract=contract, input_value=value, replay=replay, evidence_refs=tuple(refs))
    if contract.error_budget_valid is not True:
        return _error_assessment("INVALID-ERROR-BUDGET", "no-response horizon has no valid controlled error basis", contract=contract, input_value=value, replay=replay, evidence_refs=tuple(refs))
    earliest = _fraction_or_none(value.earliest_elapsed)
    # ``None`` means that no elapsed-horizon observation has been made yet;
    # it is not an invalid reading. A supplied negative reading, however, is
    # malformed even if a later administrative disposition makes it
    # irrelevant to a deadline conclusion.
    if value.earliest_elapsed is not None and (earliest is None or earliest < 0):
        return _error_assessment("INVALID-ELAPSED-HORIZON", "earliest admissible elapsed horizon is invalid", contract=contract, input_value=value, replay=replay, evidence_refs=tuple(refs))
    # A cancellation/supersession only ends a reviewed obligation if it happens
    # no later than its controlled deadline.  A post-deadline administrative
    # event cannot retroactively hide an otherwise established no-response
    # failure.  In a METHOD-ONLY contract no protocol expiry is asserted, so
    # the trace disposition remains an engineering-only administrative result.
    timely_termination = True
    if (
        disposition in {"CANCELLED", "SUPERSEDED"}
        and contract.deadline_authority == "REVIEWED"
        and contract.upper_bound is not None
    ):
        # An incremental no-response delta legitimately contains only the
        # administrative terminal event.  The retained ACTIVE request is a
        # verified input to this replay, so use it only to recover the
        # controlled trigger timestamp; ``event_refs`` itself remains the raw
        # evidence delta and must not be silently widened.
        trigger = replay.event_refs.get(value.trigger_event_id)
        if trigger is None and prior_active_requests is not None:
            trigger = prior_active_requests.get(value.trigger_event_id)
        terminating_event = replay.event_refs.get(termination) if termination is not None else None
        if trigger is None or terminating_event is None:
            return _error_assessment(
                "INVALID-OWNERSHIP-TERMINATION",
                "terminated obligation has no complete supporting event references",
                contract=contract,
                input_value=value,
                replay=replay,
                evidence_refs=tuple(refs),
            )
        elapsed_at_termination = terminating_event.timestamp - trigger.timestamp
        timely_termination = (
            elapsed_at_termination <= contract.upper_bound
            if contract.upper_closed else elapsed_at_termination < contract.upper_bound
        )
    if disposition in {"CANCELLED", "SUPERSEDED", "DISCHARGED"} and timely_termination:
        return _assessment(
            kind="NO-RESPONSE", verdict="INCONCLUSIVE", score_disposition="NOT-APPLICABLE", answered=False,
            reason=f"obligation is {disposition.lower()} and cannot receive a no-response failure", replay=replay,
            contract=contract, input_value=value, evidence_refs=tuple(refs),
        )
    if disposition in {"CANCELLED", "SUPERSEDED"} and not timely_termination:
        # Preserve the original obligation for no-response expiry when the
        # administrative termination happened too late to affect it.
        disposition = "ACTIVE"
    if disposition == "AMBIGUOUS":
        return _error_assessment("AMBIGUOUS-OWNERSHIP", "ambiguous ownership prevents a no-response conclusion", contract=contract, input_value=value, replay=replay, evidence_refs=tuple(refs))
    if disposition != "ACTIVE":
        return _error_assessment("INVALID-OBLIGATION-STATE", "no-response assessment has no active contract request", contract=contract, input_value=value, replay=replay, evidence_refs=tuple(refs))
    if value.observation_end_qualified is not True:
        return _assessment(
            kind="NO-RESPONSE", verdict="INCONCLUSIVE", score_disposition="PENDING-HORIZON", answered=False,
            reason="observation horizon is not qualified as complete", contract=contract, input_value=value,
            replay=replay, evidence_refs=tuple(refs),
        )
    if contract.deadline_authority != "REVIEWED" or contract.upper_bound is None:
        return _assessment(
            kind="NO-RESPONSE", verdict="INCONCLUSIVE", score_disposition="PENDING-DEADLINE", answered=False,
            reason="no reviewed protocol deadline is available for this obligation", replay=replay,
            contract=contract, input_value=value, evidence_refs=tuple(refs),
        )
    if earliest is None:
        return _error_assessment(
            "INVALID-ELAPSED-HORIZON",
            "qualified reviewed no-response material has no earliest admissible elapsed horizon",
            contract=contract,
            input_value=value,
            replay=replay,
            evidence_refs=tuple(refs),
        )
    assert isinstance(contract.upper_bound, Fraction)
    expired = earliest > contract.upper_bound if contract.upper_closed else earliest >= contract.upper_bound
    return _assessment(
        kind="NO-RESPONSE", verdict="FAIL" if expired else "INCONCLUSIVE",
        score_disposition="ANSWERED" if expired else "PENDING-HORIZON", answered=expired,
        reason=("earliest admissible elapsed horizon exceeds the declared deadline boundary" if expired else "earliest admissible elapsed horizon does not establish expiry"),
        contract=contract, input_value=value, replay=replay, evidence_refs=tuple(refs),
    )


def _parse_events(value: object) -> tuple[tuple[OwnershipEvent, ...], tuple[KernelDiagnostic, ...]]:
    if type(value) is not tuple or not value:
        return (), (KernelDiagnostic("INVALID-OWNERSHIP-TRACE", "events must be a nonempty tuple"),)
    parsed: list[OwnershipEvent] = []
    diagnostics: list[KernelDiagnostic] = []
    seen_ids: set[str] = set()
    previous_sequence: int | None = None
    previous_timestamp: Fraction | None = None
    for item in value:
        if type(item) is not OwnershipEvent:
            diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "trace contains a non-OwnershipEvent value"))
            continue
        if not _nonblank(item.event_id) or item.event_id in seen_ids:
            diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "event identifiers must be unique nonblank strings"))
            continue
        if type(item.sequence) is not int or item.sequence < 0:
            diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "event sequence must be a nonnegative integer"))
            continue
        if previous_sequence is not None and item.sequence <= previous_sequence:
            diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "event sequence must be strictly increasing"))
            continue
        if (
            type(item.kind) is not str
            or item.kind not in _EVENT_KINDS
            or not _nonblank(item.key)
            or not _nonblank(item.event_type)
        ):
            diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "event kind, key, or event type is invalid"))
            continue
        timestamp = _fraction_or_none(item.timestamp)
        if timestamp is None:
            diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "event timestamp must be an exact rational value"))
            continue
        if previous_timestamp is not None and timestamp < previous_timestamp:
            diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "event timestamps must be nondecreasing in trace order"))
            continue
        target_required = item.kind in {"CANCEL", "SUPERSEDE"}
        if target_required and not _nonblank(item.target_request_id):
            diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "cancellation or supersession requires a target request identity"))
            continue
        if not target_required and item.target_request_id is not None:
            if item.kind != "REQUEST" or not _nonblank(item.target_request_id):
                diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-EVENT", "only a request may carry a nonblank supersession target"))
                continue
        parsed.append(OwnershipEvent(str(item.event_id), item.sequence, str(item.kind), str(item.key), str(item.event_type), timestamp, None if item.target_request_id is None else str(item.target_request_id)))
        seen_ids.add(str(item.event_id))
        previous_sequence = item.sequence
        previous_timestamp = timestamp
    return tuple(parsed), tuple(diagnostics)


def _parse_active_seed(
    value: Mapping[str, OwnershipEvent] | None,
    contract: InterpretationContract,
) -> tuple[dict[str, OwnershipEvent], tuple[KernelDiagnostic, ...]]:
    """Validate the finite ACTIVE context supplied by a session ledger.

    This is deliberately narrower than a second raw trace parser: the seed is
    already-established contract context, so it contains only currently ACTIVE
    matching requests.  Its ordering still has to be explicit and typed; an
    adapter cannot inject a locally-renumbered predecessor and make a later
    response choose a different owner.
    """

    if value is None:
        return {}, ()
    if not isinstance(value, Mapping):
        return {}, (KernelDiagnostic(
            "INVALID-OWNERSHIP-SEED",
            "retained active ownership context must be a mapping",
        ),)
    parsed: dict[str, OwnershipEvent] = {}
    diagnostics: list[KernelDiagnostic] = []
    for identifier, event in value.items():
        if type(identifier) is not str or not identifier or type(event) is not OwnershipEvent:
            diagnostics.append(KernelDiagnostic(
                "INVALID-OWNERSHIP-SEED",
                "retained active ownership context has an invalid identifier or event",
            ))
            continue
        candidate, event_errors = _parse_events((event,))
        if event_errors or len(candidate) != 1:
            diagnostics.append(KernelDiagnostic(
                "INVALID-OWNERSHIP-SEED",
                "retained active ownership context has an invalid typed event",
            ))
            continue
        normalized = candidate[0]
        if normalized.event_id != identifier or not _request_matches_contract(normalized, contract):
            diagnostics.append(KernelDiagnostic(
                "INVALID-OWNERSHIP-SEED",
                "retained active ownership context must contain matching request events",
            ))
            continue
        parsed[identifier] = normalized
    if diagnostics:
        return {}, tuple(diagnostics)
    previous_sequence: int | None = None
    previous_timestamp: Fraction | None = None
    for event in sorted(parsed.values(), key=lambda item: item.sequence):
        if previous_sequence is not None and event.sequence <= previous_sequence:
            diagnostics.append(KernelDiagnostic(
                "INVALID-OWNERSHIP-SEED",
                "retained active request sequences must be strictly ordered",
            ))
            break
        if previous_timestamp is not None and event.timestamp < previous_timestamp:
            diagnostics.append(KernelDiagnostic(
                "INVALID-OWNERSHIP-SEED",
                "retained active request timestamps must be nondecreasing",
            ))
            break
        previous_sequence = event.sequence
        previous_timestamp = event.timestamp
    return ({} if diagnostics else parsed), tuple(diagnostics)


def _parse_order_boundary(
    value: OwnershipOrderBoundary | None,
    prior_active: Mapping[str, OwnershipEvent],
) -> tuple[OwnershipOrderBoundary | None, tuple[KernelDiagnostic, ...]]:
    """Validate one retained-ledger high-water boundary.

    Direct callers that supply only ``prior_active`` retain the historical
    finite-seed behaviour: the active requests provide the minimum known
    prefix.  A :class:`ReferenceSession` always supplies the stronger ledger
    boundary reconstructed from its checked evidence, including terminal
    requests and consumed responses.
    """

    if value is None:
        if not prior_active:
            return None, ()
        return OwnershipOrderBoundary(
            max(event.sequence for event in prior_active.values()),
            max(event.timestamp for event in prior_active.values()),
            frozenset(prior_active),
        ), ()
    if (
        type(value) is not OwnershipOrderBoundary
        or type(value.sequence) is not int
        or value.sequence < 0
        or type(value.timestamp) is not Fraction
        or type(value.retained_event_ids) is not frozenset
        or any(type(identifier) is not str or not identifier for identifier in value.retained_event_ids)
    ):
        return None, (KernelDiagnostic(
            "INVALID-OWNERSHIP-ORDER-BOUNDARY",
            "retained ownership order boundary must contain a nonnegative sequence, exact rational timestamp, and retained event identities",
        ),)
    if any(
        event.sequence > value.sequence or event.timestamp > value.timestamp
        for event in prior_active.values()
    ):
        return None, (KernelDiagnostic(
            "INVALID-OWNERSHIP-ORDER-BOUNDARY",
            "retained ownership order boundary cannot precede a seeded active request",
        ),)
    return OwnershipOrderBoundary(
        value.sequence,
        value.timestamp,
        frozenset(value.retained_event_ids),
    ), ()


def _is_order_controlled_event(
    event: OwnershipEvent,
    contract: InterpretationContract,
    controlled_request_ids: set[str],
) -> bool:
    """Whether an event can affect this contract's retained ownership facts."""

    if _request_matches_contract(event, contract):
        return True
    if (
        event.kind == "RESPONSE"
        and event.key == contract.key
        and event.event_type == contract.response_event_type
    ):
        return True
    return (
        event.kind in {"CANCEL", "SUPERSEDE"}
        and (
            event.key == contract.key
            or (
                type(event.target_request_id) is str
                and event.target_request_id in controlled_request_ids
            )
        )
    )


def _retained_ownership_order_boundary(
    event_refs: Mapping[str, OwnershipEvent],
    contract: InterpretationContract,
) -> OwnershipOrderBoundary | None:
    """Derive the controlled global high-water mark from a checked ledger.

    A session ledger also retains unrelated other-key facts so it can detect
    identity reuse.  Those facts deliberately do not advance this contract's
    ownership frontier *or* enter this contract's retained-receipt identity
    set unless a termination targets one of this contract's requests.  The
    function is private because callers must obtain the ledger from verified
    session evidence rather than fabricate an authority value.
    """

    controlled_request_ids = {
        identifier
        for identifier, event in event_refs.items()
        if type(identifier) is str
        and type(event) is OwnershipEvent
        and _request_matches_contract(event, contract)
    }
    relevant = tuple(
        event
        for event in event_refs.values()
        if type(event) is OwnershipEvent
        and _is_order_controlled_event(event, contract, controlled_request_ids)
    )
    if not relevant:
        return None
    return OwnershipOrderBoundary(
        max(event.sequence for event in relevant),
        max(event.timestamp for event in relevant),
        frozenset(event.event_id for event in relevant),
    )


def _parse_contract(value: object) -> tuple[InterpretationContract | None, tuple[KernelDiagnostic, ...]]:
    if type(value) is not InterpretationContract:
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "contract is not a typed InterpretationContract"),)
    fields = (
        value.contract_id, value.trigger_event_type, value.response_event_type, value.key,
        value.cancellation_event_type, value.supersession_event_type, value.clock_identity,
        value.uncertainty_identity, value.error_budget_identity, value.unit,
    )
    if not all(_nonblank(field) for field in fields):
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "contract identity, event encoding, clock, uncertainty, error basis, and unit must be nonblank strings"),)
    if (
        type(value.policy) is not str
        or value.policy not in _POLICIES
        or type(value.concurrent_same_key) is not bool
        or type(value.upper_closed) is not bool
    ):
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "contract ownership policy or Boolean topology is invalid"),)
    if type(value.clock_valid) is not bool or type(value.error_budget_valid) is not bool:
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "contract clock and error-budget validity must be Boolean"),)
    if type(value.deadline_authority) is not str or value.deadline_authority not in _DEADLINE_AUTHORITIES:
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "contract deadline authority is invalid"),)
    if value.deadline_identity is not None and not _nonblank(value.deadline_identity):
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "optional deadline identity must be absent or a nonblank exact string"),)
    physical, physical_error = _validated_interval(value.physical_domain)
    requirement, requirement_error = _validated_interval(value.requirement_window)
    if physical_error is not None or requirement_error is not None or physical is None or requirement is None:
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "contract physical and requirement intervals must be nonempty exact intervals"),)
    upper = None if value.upper_bound is None else _fraction_or_none(value.upper_bound)
    if value.upper_bound is not None and (upper is None or upper < 0):
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "contract deadline upper bound must be a nonnegative exact rational"),)
    if value.deadline_authority == "REVIEWED" and (upper is None or not _nonblank(value.deadline_identity)):
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "reviewed deadline requires a boundary and stable identity"),)
    if value.deadline_authority == "UNRESOLVED" and (upper is not None or value.deadline_identity is not None):
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "unresolved deadline cannot claim a boundary or identity"),)
    if value.deadline_authority == "METHOD-ONLY" and upper is not None and not _nonblank(value.deadline_identity):
        return None, (KernelDiagnostic("INVALID-INTERPRETATION-CONTRACT", "method-only teaching boundary requires a stable method identity"),)
    if upper is not None and (
        upper != requirement.upper or value.upper_closed != requirement.upper_closed
    ):
        return None, (KernelDiagnostic(
            "INVALID-INTERPRETATION-CONTRACT",
            "deadline boundary must be derived from the requirement interval upper endpoint and closure",
        ),)
    return InterpretationContract(
        str(value.contract_id), str(value.trigger_event_type), str(value.response_event_type), str(value.key),
        str(value.policy), value.concurrent_same_key, str(value.cancellation_event_type), str(value.supersession_event_type),
        physical, requirement, str(value.clock_identity), str(value.uncertainty_identity), str(value.error_budget_identity), str(value.unit),
        value.clock_valid, value.error_budget_valid, str(value.deadline_authority),
        None if value.deadline_identity is None else str(value.deadline_identity), upper, value.upper_closed,
    ), ()


def _input_error(value: ObservationInput, contract: InterpretationContract) -> KernelDiagnostic | None:
    if type(value.events) is not tuple:
        return KernelDiagnostic("INVALID-OBSERVATION-INPUT", "observation events must be a tuple")
    if not _nonblank(value.trigger_event_id):
        return KernelDiagnostic("INVALID-OBSERVATION-INPUT", "observation trigger identity must be nonblank")
    if value.response_id is not None and not _nonblank(value.response_id):
        return KernelDiagnostic("INVALID-OBSERVATION-INPUT", "response identity must be absent or nonblank")
    if type(value.observation_end_qualified) is not bool:
        return KernelDiagnostic("INVALID-OBSERVATION-INPUT", "observation-end qualification must be Boolean")
    if value.earliest_elapsed is not None and _fraction_or_none(value.earliest_elapsed) is None:
        return KernelDiagnostic("INVALID-OBSERVATION-INPUT", "earliest elapsed horizon must be an exact rational")
    if not all(_nonblank(field) for field in (value.execution_attempt_id, value.action_id, value.evidence_ref, value.clock_identity, value.unit)):
        return KernelDiagnostic("INVALID-OBSERVATION-BINDING", "raw material is not bound to one execution/action/evidence/clock/unit identity")
    if value.clock_identity != contract.clock_identity or value.unit != contract.unit:
        return KernelDiagnostic("OBSERVATION-CLOCK-UNIT-MISMATCH", "observation clock identity or unit differs from its controlled contract")
    if value.response_id is None:
        if value.measurement_interval is not None or value.measurement_tick is not None or value.uncertainty_identity is not None:
            return KernelDiagnostic("INVALID-NO-RESPONSE-MATERIAL", "no-response material cannot carry a response measurement or uncertainty identity")
    else:
        interval, interval_error = _validated_interval(value.measurement_interval)
        if interval_error is not None or interval is None:
            return KernelDiagnostic("INVALID-MEASUREMENT-INTERVAL", "response material must carry a nonempty exact measurement interval")
        if type(value.measurement_tick) is not Fraction:
            return KernelDiagnostic("INVALID-MEASUREMENT-INTERVAL", "response material must bind one exact record measurement tick")
        if not _nonblank(value.uncertainty_identity) or value.uncertainty_identity != contract.uncertainty_identity:
            return KernelDiagnostic("OBSERVATION-UNCERTAINTY-MISMATCH", "response material uncertainty identity differs from its controlled contract")
    return None


def _terminate_request(
    target: str,
    event: OwnershipEvent,
    active: set[str],
    dispositions: dict[str, str],
    termination_refs: dict[str, str],
    known_requests: Mapping[str, OwnershipEvent],
    contract: InterpretationContract,
    diagnostics: list[KernelDiagnostic],
    disposition: str,
    *,
    require_active: bool = False,
) -> bool:
    """Terminate one current obligation and report whether it really closed.

    Administrative cancellation/supersession keeps its idempotent treatment
    for an already terminal target.  A *new REQUEST* that uses a replacement
    target is different: it must demonstrate an actual current termination or
    it could create a second non-concurrent obligation through a stale ID.
    """

    target_event = known_requests.get(target)
    if target_event is None:
        diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-TERMINATION", "termination target does not name an already observed contract request"))
        return False
    if target_event.key != event.key or target_event.event_type != contract.trigger_event_type:
        diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-TERMINATION", "termination target does not match the controlled request encoding"))
        return False
    if event.sequence <= target_event.sequence or event.timestamp < target_event.timestamp:
        diagnostics.append(KernelDiagnostic("INVALID-OWNERSHIP-TERMINATION", "termination does not occur after its target request"))
        return False
    if target in active:
        active.remove(target)
        dispositions[target] = disposition
        termination_refs[target] = event.event_id
        return True
    if require_active:
        diagnostics.append(KernelDiagnostic(
            "INVALID-OWNERSHIP-TERMINATION",
            "replacement request targets an obligation that is no longer active",
        ))
        return False
    return True


def _request_matches_contract(event: OwnershipEvent, contract: InterpretationContract) -> bool:
    return event.kind == "REQUEST" and event.key == contract.key and event.event_type == contract.trigger_event_type


def _response_matches(response: OwnershipEvent, trigger: OwnershipEvent, contract: InterpretationContract) -> bool:
    return response.key == contract.key and response.event_type == contract.response_event_type and response.sequence > trigger.sequence and response.timestamp >= trigger.timestamp


def _assessment(*, kind: str, verdict: str, score_disposition: str, answered: bool, reason: str, contract: InterpretationContract, input_value: ObservationInput, ownership: OwnershipResolution | None = None, replay: OwnershipReplay | None = None, measurement_interval: Interval | None = None, physical_interval: Interval | None = None, requirement_window: Interval | None = None, evidence_refs: tuple[str, ...] = (), diagnostics: tuple[KernelDiagnostic, ...] = ()) -> ObservationAssessment:
    # Keep the public boolean derived from controlled outcome fields.  In
    # particular, a pending/administrative INCONCLUSIVE result can never be
    # represented as an answered protocol verdict merely because a caller
    # supplied ``answered=True`` to this internal constructor.
    answered = score_disposition == "ANSWERED" and verdict in {"PASS", "FAIL"}
    return ObservationAssessment(
        kind, verdict, score_disposition, answered, reason, contract.contract_id,
        input_value.execution_attempt_id if isinstance(input_value.execution_attempt_id, str) else None,
        input_value.action_id if isinstance(input_value.action_id, str) else None,
        input_value.evidence_ref if isinstance(input_value.evidence_ref, str) else None,
        input_value.trigger_event_id if isinstance(input_value.trigger_event_id, str) else None,
        input_value.response_id if isinstance(input_value.response_id, str) else None,
        ownership, replay, measurement_interval, physical_interval, requirement_window,
        contract.clock_identity, input_value.uncertainty_identity if isinstance(input_value.uncertainty_identity, str) else None,
        contract.error_budget_identity, contract.unit,
        contract.deadline_identity if isinstance(contract.deadline_identity, str) else None,
        tuple(evidence_refs), tuple(diagnostics),
    )


def _error_assessment(code: str, message: str, *, contract: InterpretationContract | None = None, input_value: ObservationInput | None = None, ownership: OwnershipResolution | None = None, replay: OwnershipReplay | None = None, measurement_interval: Interval | None = None, evidence_refs: tuple[str, ...] = (), diagnostics: tuple[KernelDiagnostic, ...] = ()) -> ObservationAssessment:
    diagnostic = KernelDiagnostic(code, message)
    if contract is not None and input_value is not None:
        return _assessment(kind="T5" if input_value.response_id is not None else "NO-RESPONSE", verdict="ERROR", score_disposition="ERROR", answered=False, reason=message, contract=contract, input_value=input_value, ownership=ownership, replay=replay, measurement_interval=measurement_interval, requirement_window=contract.requirement_window if isinstance(contract.requirement_window, Interval) else None, evidence_refs=evidence_refs, diagnostics=tuple(diagnostics) + (diagnostic,))
    return ObservationAssessment("T5", "ERROR", "ERROR", False, message, None, None, None, None, None, None, ownership, replay, measurement_interval, None, None, None, None, None, None, None, tuple(evidence_refs), tuple(diagnostics) + (diagnostic,))


def strict_observation_input_equal(actual: object, expected: object) -> bool:
    if actual is None or expected is None:
        return actual is None and expected is None
    if type(actual) is not ObservationInput or type(expected) is not ObservationInput:
        return False
    return all((
        _strict_events_equal(actual.events, expected.events), _strict_scalar_equal(actual.trigger_event_id, expected.trigger_event_id),
        _strict_scalar_equal(actual.response_id, expected.response_id), _strict_interval_equal(actual.measurement_interval, expected.measurement_interval),
        _strict_scalar_equal(actual.observation_end_qualified, expected.observation_end_qualified), _strict_scalar_equal(actual.earliest_elapsed, expected.earliest_elapsed),
        _strict_scalar_equal(actual.clock_identity, expected.clock_identity), _strict_scalar_equal(actual.unit, expected.unit),
        _strict_scalar_equal(actual.execution_attempt_id, expected.execution_attempt_id), _strict_scalar_equal(actual.action_id, expected.action_id),
        _strict_scalar_equal(actual.evidence_ref, expected.evidence_ref), _strict_scalar_equal(actual.measurement_tick, expected.measurement_tick),
        _strict_scalar_equal(actual.uncertainty_identity, expected.uncertainty_identity),
    ))


def strict_observation_assessment_equal(actual: object, expected: object) -> bool:
    if actual is None or expected is None:
        return actual is None and expected is None
    if type(actual) is not ObservationAssessment or type(expected) is not ObservationAssessment:
        return False
    scalar_fields = ("kind", "verdict", "score_disposition", "answered", "reason", "contract_id", "execution_attempt_id", "action_id", "evidence_ref", "trigger_event_id", "response_id", "clock_identity", "uncertainty_identity", "error_budget_identity", "unit", "deadline_identity")
    return all(_strict_scalar_equal(getattr(actual, name), getattr(expected, name)) for name in scalar_fields) and all((
        _strict_resolution_equal(actual.ownership, expected.ownership), _strict_replay_equal(actual.replay, expected.replay), _strict_interval_equal(actual.measurement_interval, expected.measurement_interval),
        _strict_interval_equal(actual.physical_interval, expected.physical_interval), _strict_interval_equal(actual.requirement_window, expected.requirement_window),
        _strict_tuple_equal(actual.evidence_refs, expected.evidence_refs), _strict_diagnostics_equal(actual.diagnostics, expected.diagnostics),
    ))


def strict_interpretation_contract_equal(actual: object, expected: object) -> bool:
    if type(actual) is not InterpretationContract or type(expected) is not InterpretationContract:
        return False
    names = ("contract_id", "trigger_event_type", "response_event_type", "key", "policy", "concurrent_same_key", "cancellation_event_type", "supersession_event_type", "clock_identity", "uncertainty_identity", "error_budget_identity", "unit", "clock_valid", "error_budget_valid", "deadline_authority", "deadline_identity", "upper_bound", "upper_closed")
    return all(_strict_scalar_equal(getattr(actual, name), getattr(expected, name)) for name in names) and _strict_interval_equal(actual.physical_domain, expected.physical_domain) and _strict_interval_equal(actual.requirement_window, expected.requirement_window)


def interpretation_contract_identity(contract: InterpretationContract) -> str:
    """Stable, complete identity for a validated controlled contract."""

    parsed, errors = _parse_contract(contract)
    if parsed is None or errors:
        raise ValueError("interpretation contract is invalid")
    payload = repr((parsed.contract_id, parsed.trigger_event_type, parsed.response_event_type, parsed.key, parsed.policy, parsed.concurrent_same_key, parsed.cancellation_event_type, parsed.supersession_event_type, parsed.physical_domain.lower, parsed.physical_domain.upper, parsed.physical_domain.lower_closed, parsed.physical_domain.upper_closed, parsed.requirement_window.lower, parsed.requirement_window.upper, parsed.requirement_window.lower_closed, parsed.requirement_window.upper_closed, parsed.clock_identity, parsed.uncertainty_identity, parsed.error_budget_identity, parsed.unit, parsed.clock_valid, parsed.error_budget_valid, parsed.deadline_authority, parsed.deadline_identity, parsed.upper_bound, parsed.upper_closed)).encode("utf-8")
    from hashlib import sha256
    return sha256(payload).hexdigest()


def _strict_events_equal(actual: object, expected: object) -> bool:
    if type(actual) is not tuple or type(expected) is not tuple or len(actual) != len(expected):
        return False
    for left, right in zip(actual, expected, strict=True):
        if type(left) is not OwnershipEvent or type(right) is not OwnershipEvent:
            return False
        if not all(_strict_scalar_equal(getattr(left, name), getattr(right, name)) for name in ("event_id", "sequence", "kind", "key", "event_type", "timestamp", "target_request_id")):
            return False
    return True


def _strict_resolution_equal(actual: object, expected: object) -> bool:
    if actual is None or expected is None:
        return actual is None and expected is None
    if type(actual) is not OwnershipResolution or type(expected) is not OwnershipResolution:
        return False
    return all((_strict_scalar_equal(actual.response_id, expected.response_id), _strict_scalar_equal(actual.status, expected.status), _strict_scalar_equal(actual.owner_request_id, expected.owner_request_id), _strict_tuple_equal(actual.candidate_request_ids, expected.candidate_request_ids), _strict_tuple_equal(actual.evidence_refs, expected.evidence_refs), _strict_diagnostics_equal(actual.diagnostics, expected.diagnostics)))


def _strict_replay_equal(actual: object, expected: object) -> bool:
    """Compare a complete replay as a closed typed evidence value."""

    if actual is None or expected is None:
        return actual is None and expected is None
    if type(actual) is not OwnershipReplay or type(expected) is not OwnershipReplay:
        return False
    if not _strict_scalar_equal(actual.contract_id, expected.contract_id):
        return False
    return all((
        _strict_string_key_mapping_equal(
            actual.request_dispositions,
            expected.request_dispositions,
            _strict_scalar_equal,
        ),
        _strict_string_key_mapping_equal(
            actual.termination_refs,
            expected.termination_refs,
            _strict_scalar_equal,
        ),
        _strict_string_key_mapping_equal(
            actual.response_resolutions,
            expected.response_resolutions,
            _strict_resolution_equal,
        ),
        _strict_string_key_mapping_equal(
            actual.event_refs,
            expected.event_refs,
            _strict_event_equal,
        ),
        _strict_diagnostics_equal(actual.diagnostics, expected.diagnostics),
    ))


def _strict_string_key_mapping_equal(actual: object, expected: object, value_equal: object) -> bool:
    """Compare a closed mapping without Python's ``str`` subclass coercion.

    The replay is public typed evidence.  Ordinary mapping/set equality treats
    a ``str`` subclass as the same key as its base ``str`` value; accepting
    that substitution would allow an evidence checkpoint to carry a value the
    parser itself could never produce.  Require exact string keys on both
    sides before comparing their closed value mapping.
    """

    if not isinstance(actual, Mapping) or not isinstance(expected, Mapping):
        return False
    if len(actual) != len(expected) or any(type(key) is not str for key in actual) or any(
        type(key) is not str for key in expected
    ):
        return False
    if set(actual) != set(expected) or not callable(value_equal):
        return False
    return all(bool(value_equal(actual[key], expected[key])) for key in actual)


def _strict_event_equal(actual: object, expected: object) -> bool:
    if type(actual) is not OwnershipEvent or type(expected) is not OwnershipEvent:
        return False
    return all(
        _strict_scalar_equal(getattr(actual, name), getattr(expected, name))
        for name in ("event_id", "sequence", "kind", "key", "event_type", "timestamp", "target_request_id")
    )


def _strict_interval_equal(actual: object, expected: object) -> bool:
    if actual is None or expected is None:
        return actual is None and expected is None
    if type(actual) is not Interval or type(expected) is not Interval:
        return False
    return all(_strict_scalar_equal(getattr(actual, name), getattr(expected, name)) for name in ("lower", "upper", "lower_closed", "upper_closed"))


def _strict_tuple_equal(actual: object, expected: object) -> bool:
    return type(actual) is tuple and type(expected) is tuple and len(actual) == len(expected) and all(_strict_scalar_equal(left, right) for left, right in zip(actual, expected, strict=True))


def _strict_diagnostics_equal(actual: object, expected: object) -> bool:
    if type(actual) is not tuple or type(expected) is not tuple or len(actual) != len(expected):
        return False
    return all(type(left) is KernelDiagnostic and type(right) is KernelDiagnostic and _strict_scalar_equal(left.code, right.code) and _strict_scalar_equal(left.message, right.message) for left, right in zip(actual, expected, strict=True))


def _strict_scalar_equal(actual: object, expected: object) -> bool:
    return type(actual) is type(expected) and actual == expected


def _contains(container: Interval, item: Interval) -> bool:
    return ((item.lower > container.lower or (item.lower == container.lower and (container.lower_closed or not item.lower_closed))) and (item.upper < container.upper or (item.upper == container.upper and (container.upper_closed or not item.upper_closed))))


def _validated_interval(value: object) -> tuple[Interval | None, KernelDiagnostic | None]:
    if type(value) is not Interval:
        return None, KernelDiagnostic("INVALID-MEASUREMENT-INTERVAL", "interval is not a typed Interval")
    if type(value.lower) is not Fraction or type(value.upper) is not Fraction or type(value.lower_closed) is not bool or type(value.upper_closed) is not bool:
        return None, KernelDiagnostic("INVALID-MEASUREMENT-INTERVAL", "interval endpoints or topology are not exact typed values")
    if value.lower > value.upper or (value.lower == value.upper and not (value.lower_closed and value.upper_closed)):
        return None, KernelDiagnostic("INVALID-MEASUREMENT-INTERVAL", "interval is empty")
    return value, None


def _interval_contains(interval: Interval, tick: Fraction) -> bool:
    return ((tick > interval.lower or (tick == interval.lower and interval.lower_closed)) and (tick < interval.upper or (tick == interval.upper and interval.upper_closed)))


def _fraction_or_none(value: object) -> Fraction | None:
    if type(value) is Fraction:
        return value
    if type(value) is int:
        return Fraction(value)
    return None


def _fraction_from_public(value: object) -> Fraction:
    if type(value) is int:
        return Fraction(value)
    if isinstance(value, Mapping) and set(value) == {"numerator", "positiveDenominator"}:
        numerator = value["numerator"]
        denominator = value["positiveDenominator"]
        if type(numerator) is int and type(denominator) is int and denominator > 0:
            return Fraction(numerator, denominator)
    raise ValueError("rational value must be an integer or canonical rational mapping")


def _interval_from_public(value: object) -> Interval:
    if not isinstance(value, Mapping) or set(value) != {"lower", "upper", "lowerClosed", "upperClosed"}:
        raise ValueError("interval uses unknown or missing fields")
    lower_closed = value["lowerClosed"]
    upper_closed = value["upperClosed"]
    if type(lower_closed) is not bool or type(upper_closed) is not bool:
        raise ValueError("interval endpoint closure must be Boolean")
    lower = _fraction_from_public(value["lower"])
    upper = _fraction_from_public(value["upper"])
    if lower > upper or (lower == upper and not (lower_closed and upper_closed)):
        raise ValueError("interval is empty")
    return Interval(lower, upper, lower_closed, upper_closed)


def _nonblank(value: object) -> bool:
    return type(value) is str and bool(value.strip())
