"""Read-only G4 bridge from bounded offline evidence to structural replay.

The bounded offline intake package deliberately stops at reconstruction
evidence.  This module adds the next, still deliberately narrow boundary:
it rebuilds a persisted PR22 intake envelope from its capture bytes, consumes
the already validated controlled projection, and presents a *structural*
ownership replay through the public runtime entry point.

It is not a :class:`cltav_runtime.session.ReferenceSession` execution.  An
offline capture has no issued action, execution attempt, reset confirmation,
qualified measurement chain, or independent deadline authority.  The bridge
therefore records ``OFFLINE-REPLAY`` and ``NOT-SCORED`` only.  In particular it
never creates a protocol PASS/FAIL, an IUT finding, a history update, or a
charge merely because a passive capture contains a request and a terminal TFTP
data packet.
"""

from __future__ import annotations

import json
import os
import uuid
from copy import deepcopy
from dataclasses import dataclass, field
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable, Mapping

from cltav_runtime.interpretation import (
    InterpretationContract,
    OwnershipEvent,
    OwnershipReplay,
    replay_ownership,
)
from cltav_runtime.kernel import Interval

from .evidence import evidence_errors
from .pipeline import IntakeConfig, IntakeError, run_capture, validate_source_commit


OFFLINE_REPLAY_ARTIFACT_TYPE = "CLTAV-OFFLINE-REPLAY-BRIDGE"
OFFLINE_REPLAY_SCHEMA_VERSION = "1.0"
_RUN_TOKEN = object()


class OfflineReplayError(ValueError):
    """A named, controlled rejection at the offline bridge boundary."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class OfflineReplayRun:
    """One source-rebuilt, non-scoring offline replay result.

    The raw intake bytes remain private input for staged verification and are
    never emitted as a host path.  The JSON envelope itself contains only the
    bounded PR22 evidence records, which remain safe to retain in the bridge
    artifact for independent relation reconstruction.
    """

    capture_path: Path = field(repr=False, compare=False)
    evidence_path: Path | None = field(repr=False, compare=False)
    _offline_evidence_raw: bytes = field(repr=False, compare=False)
    _offline_evidence: dict[str, Any] = field(repr=False, compare=False)
    _records: tuple[dict[str, Any], ...] = field(repr=False, compare=False)
    _token: object | None = field(default=None, init=False, repr=False, compare=False)
    _snapshot_digest: str | None = field(default=None, init=False, repr=False, compare=False)

    @property
    def offline_evidence_raw(self) -> bytes:
        """Return immutable source bytes retained by the source-rebuilt run."""

        return self._offline_evidence_raw

    @property
    def offline_evidence(self) -> dict[str, Any]:
        """Return a defensive copy; callers cannot alter bridge provenance."""

        return deepcopy(self._offline_evidence)

    @property
    def records(self) -> tuple[dict[str, Any], ...]:
        """Return defensive record copies; replay results remain non-scoring."""

        return tuple(deepcopy(record) for record in self._records)


def canonical_json_bytes(value: object) -> bytes:
    """Encode a finite bridge value in one unambiguous UTF-8 form."""

    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise OfflineReplayError("OFFLINE-BRIDGE-ENCODING-ERROR", str(exc) or type(exc).__name__) from exc
    return rendered.encode("utf-8") + b"\n"


def load_offline_evidence_bytes(raw: bytes) -> dict[str, Any]:
    """Decode a UTF-8 intake envelope without accepting duplicate JSON keys."""

    if type(raw) is not bytes:
        raise OfflineReplayError("OFFLINE-EVIDENCE-READ-ERROR", "offline evidence must be supplied as bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise OfflineReplayError("OFFLINE-EVIDENCE-ENCODING-ERROR", "offline evidence must be UTF-8") from exc

    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise OfflineReplayError("OFFLINE-EVIDENCE-SHAPE-ERROR", f"offline evidence repeats JSON key {key!r}")
            result[key] = value
        return result

    try:
        value = json.loads(text, object_pairs_hook=no_duplicates, parse_constant=_reject_json_constant)
    except OfflineReplayError:
        raise
    except json.JSONDecodeError as exc:
        raise OfflineReplayError("OFFLINE-EVIDENCE-JSON-ERROR", "offline evidence is not valid JSON") from exc
    if type(value) is not dict:
        raise OfflineReplayError("OFFLINE-EVIDENCE-SHAPE-ERROR", "offline evidence root must be an object")
    _reject_floats(value)
    return value


def adapt_offline_evidence_bytes(
    raw: bytes,
    *,
    capture_path: Path,
    evidence_path: Path | None = None,
) -> OfflineReplayRun:
    """Rebuild one real intake envelope, then adapt its finite projection.

    The producer envelope is not trusted merely because it carries a hash or
    a well-formed projection.  It must pass the PR22 production validators and
    be exactly reproducible from the caller-supplied capture path before the
    bridge consumes any request/terminal witness.
    """

    source = load_offline_evidence_bytes(raw)
    _validate_source_evidence(source)
    capture = _resolved_regular_file(capture_path, code="OFFLINE-CAPTURE-READ-ERROR")
    resolved_evidence = (
        None
        if evidence_path is None
        else _resolved_regular_file(evidence_path, code="OFFLINE-EVIDENCE-READ-ERROR")
    )
    if resolved_evidence is not None:
        try:
            on_disk_evidence = resolved_evidence.read_bytes()
        except OSError as exc:
            raise OfflineReplayError(
                "OFFLINE-EVIDENCE-READ-ERROR", "offline evidence file cannot be read",
            ) from exc
        if on_disk_evidence != raw:
            raise OfflineReplayError(
                "OFFLINE-EVIDENCE-IDENTITY-MISMATCH",
                "offline evidence bytes differ from the declared evidence file",
            )
    rebuilt = _rebuild_source_evidence(source, capture)
    difference = _first_difference(source, rebuilt, "$.offlineEvidence")
    if difference:
        raise OfflineReplayError(
            "OFFLINE-SOURCE-MISMATCH",
            f"offline evidence does not match the rebuilt decoder/projection at {difference}",
        )
    records = tuple(deepcopy(record) for record in _adapt_records(source))
    run = OfflineReplayRun(
        capture_path=capture,
        evidence_path=resolved_evidence,
        _offline_evidence_raw=raw,
        _offline_evidence=deepcopy(source),
        _records=records,
    )
    object.__setattr__(run, "_snapshot_digest", _snapshot_digest(run))
    object.__setattr__(run, "_token", _RUN_TOKEN)
    return run


def offline_replay_document(run: OfflineReplayRun) -> dict[str, Any]:
    """Render the closed, non-scoring bridge envelope for one verified run."""

    run = _require_run(run)
    source = run.offline_evidence
    input_value = _mapping(source.get("input"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "offline evidence input")
    tool = _mapping(source.get("tool"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "offline evidence tool")
    projection = _mapping(
        source.get("contractProjection"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "offline evidence contract projection",
    )
    payload: dict[str, Any] = {
        "artifactType": OFFLINE_REPLAY_ARTIFACT_TYPE,
        "schemaVersion": OFFLINE_REPLAY_SCHEMA_VERSION,
        "mode": "OFFLINE-REPLAY",
        "boundary": {
            "purpose": "EXPLORATORY-DEVELOPMENT-ONLY",
            "statement": (
                "This is a passive, non-scoring structural replay of bounded offline intake evidence. "
                "It does not issue an action, charge a cost, reset a session, update history, "
                "claim a protocol verdict, or attribute an IUT failure."
            ),
            "conformanceVerdict": "NOT-EVALUATED",
            "integrity": "NOT-EVALUATED",
        },
        "source": {
            "offlineEvidenceSha256": sha256(run.offline_evidence_raw).hexdigest(),
            "captureIdentity": {
                "captureId": input_value.get("captureId"),
                "byteCount": input_value.get("byteCount"),
                "sha256": input_value.get("sha256"),
            },
            "tool": deepcopy(tool),
            "contractProjectionIdentity": deepcopy(projection.get("contractIdentity")),
        },
        # Keeping the bounded, payload-free producer envelope gives the
        # validator a complete relation to rebuild.  It is not a new source of
        # truth: validation always re-runs the PR22 decoder/projection first.
        "offlineEvidence": deepcopy(source),
        "records": [deepcopy(record) for record in run.records],
        "activeExecution": {
            "issuedActionCount": 0,
            "chargedCost": 0,
            "attemptCount": 0,
            "resetApplied": False,
            "historyUpdated": False,
            "activeFeedbackApplied": False,
        },
    }
    payload["integrity"] = {"canonicalPayloadSha256": sha256(canonical_json_bytes(payload)).hexdigest()}
    return payload


def offline_replay_bytes(run: OfflineReplayRun) -> bytes:
    """Return canonical bytes for a source-rebuilt offline replay artifact."""

    return canonical_json_bytes(offline_replay_document(run))


def validate_offline_replay_bytes(
    raw: bytes,
    *,
    capture_path: Path,
    offline_evidence_raw: bytes,
    evidence_path: Path | None = None,
) -> dict[str, Any]:
    """Validate a persisted bridge artifact against the actual capture chain."""

    document = _load_bridge_bytes(raw)
    return validate_offline_replay_document(
        document,
        capture_path=capture_path,
        offline_evidence_raw=offline_evidence_raw,
        evidence_path=evidence_path,
    )


def validate_offline_replay_document(
    document: object,
    *,
    capture_path: Path,
    offline_evidence_raw: bytes,
    evidence_path: Path | None = None,
) -> dict[str, Any]:
    """Rebuild the bounded source and require exact bridge relation equality."""

    if type(document) is not dict:
        raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay artifact must be an object")
    _reject_floats(document)
    _validate_bridge_shape(document)
    _validate_bridge_integrity(document)
    source = _mapping(document["source"], "OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay source")
    actual_source_sha = sha256(offline_evidence_raw).hexdigest()
    if source.get("offlineEvidenceSha256") != actual_source_sha:
        raise OfflineReplayError("OFFLINE-EVIDENCE-IDENTITY-MISMATCH", "offline replay does not name the supplied evidence bytes")
    run = adapt_offline_evidence_bytes(
        offline_evidence_raw,
        capture_path=capture_path,
        evidence_path=evidence_path,
    )
    expected = offline_replay_document(run)
    actual_payload = {key: value for key, value in document.items() if key != "integrity"}
    expected_payload = {key: value for key, value in expected.items() if key != "integrity"}
    difference = _first_difference(actual_payload, expected_payload, "$")
    if difference:
        raise OfflineReplayError(
            "OFFLINE-BRIDGE-RELATION-MISMATCH",
            f"offline replay does not match the rebuilt source relation at {difference}",
        )
    return expected


def publish_offline_replay(
    run: OfflineReplayRun,
    *,
    output: Path,
    replace_fn: Callable[[Path, Path], None] = os.replace,
) -> dict[str, Any]:
    """Atomically stage, relation-validate, and publish a replay artifact."""

    run = _require_run(run)
    target = _safe_output_target(output, run)
    document = offline_replay_document(run)
    encoded = canonical_json_bytes(document)
    target.parent.mkdir(parents=True, exist_ok=True)
    stage = target.parent / f".{target.name}.staging-{uuid.uuid4().hex}"
    backup = target.parent / f".{target.name}.backup-{uuid.uuid4().hex}"
    moved_old = False
    published = False
    preserve_backup = False

    def validator(candidate: bytes) -> None:
        validate_offline_replay_bytes(
            candidate,
            capture_path=run.capture_path,
            offline_evidence_raw=run.offline_evidence_raw,
            evidence_path=run.evidence_path,
        )

    try:
        _write_private_stage(stage, encoded)
        validator(stage.read_bytes())
        if target.exists():
            _assert_owned_target(target, validator)
            replace_fn(target, backup)
            moved_old = True
        replace_fn(stage, target)
        published = True
        validator(target.read_bytes())
        if moved_old and backup.exists():
            backup.unlink()
        return document
    except OfflineReplayError:
        try:
            _restore_after_failure(target, backup, moved_old, published, replace_fn)
        except OfflineReplayError:
            # A backup is the last recoverable copy of a previously-owned
            # artifact.  Never erase it merely because the forward publish
            # and the attempted rollback both failed.
            preserve_backup = moved_old and backup.exists()
            raise
        raise
    except OSError as exc:
        try:
            _restore_after_failure(target, backup, moved_old, published, replace_fn)
        except OfflineReplayError:
            preserve_backup = moved_old and backup.exists()
            raise
        raise OfflineReplayError("OFFLINE-BRIDGE-PUBLISH-ERROR", str(exc) or type(exc).__name__) from exc
    finally:
        _safe_unlink(stage)
        if not preserve_backup:
            _safe_unlink(backup)


def _adapt_records(source: dict[str, Any]) -> list[dict[str, Any]]:
    """Project only source-proven request/terminal witnesses into replay rows."""

    packet_refs = _id_map(source.get("packetRefs"), "packetRefId", "packetRefs")
    datagrams = _id_map(source.get("datagrams"), "datagramId", "datagrams")
    events = _id_map(source.get("events"), "eventId", "events")
    projection = _mapping(source.get("contractProjection"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "contract projection")
    projected_records = projection.get("records")
    if type(projected_records) is not list:
        raise OfflineReplayError("OFFLINE-PROJECTION-SHAPE-ERROR", "contract projection records must be an array")
    request_records: dict[str, dict[str, Any]] = {}
    for item in projected_records:
        if type(item) is not dict:
            raise OfflineReplayError("OFFLINE-PROJECTION-SHAPE-ERROR", "contract projection record must be an object")
        if item.get("recordType") != "PROTOCOL-EVENT":
            continue
        source_id = item.get("sourceId")
        if type(source_id) is not str or not source_id:
            raise OfflineReplayError("OFFLINE-PROJECTION-SHAPE-ERROR", "protocol projection must have a nonblank sourceId")
        if source_id in request_records:
            raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "projection has repeated protocol sourceId")
        request_records[source_id] = item
    non_projectable = _nonprojectable_by_source(projection.get("nonProjectable"))

    transfers = source.get("transfers")
    if type(transfers) is not list:
        raise OfflineReplayError("OFFLINE-EVIDENCE-SHAPE-ERROR", "offline evidence transfers must be an array")
    results: list[dict[str, Any]] = []
    transfer_datagram_ids: set[str] = set()
    for transfer in transfers:
        transfer_mapping = _mapping(transfer, "OFFLINE-EVIDENCE-SHAPE-ERROR", "transfer")
        transfer_id = _nonblank_string(transfer_mapping.get("transferId"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transferId")
        request_projection_id = f"event-request-{transfer_id}"
        request_projection = request_records.get(request_projection_id)
        if request_projection is None:
            # A valid bounded intake may have enough source lineage to retain
            # a partial transfer but not enough contract data to project its
            # request event.  Preserve that producer-declared limit as a
            # non-scoring quality row; do not turn it into a fake ownership
            # error or pretend it supplies a qualified request.
            results.append(
                _adapt_nonprojectable_transfer(
                    source,
                    transfer_mapping,
                    packet_refs=packet_refs,
                    datagrams=datagrams,
                    events=events,
                    reasons=non_projectable.get(transfer_id, ()),
                )
            )
        else:
            results.append(
                _adapt_transfer(
                    source,
                    transfer_mapping,
                    request_projection,
                    packet_refs=packet_refs,
                    datagrams=datagrams,
                    events=events,
                )
            )
        transfer_datagram_ids.update(_string_list(
            transfer_mapping.get("datagramIds"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transfer datagramIds",
        ))
    # A bounded capture can truthfully stop at reassembly without yielding a
    # TFTP transfer.  Preserve that GAPPED/CONFLICT quality in a replay
    # artifact instead of rejecting it merely because there is no candidate
    # request to pass to the public ownership component.
    for identifier, datagram in datagrams.items():
        if identifier in transfer_datagram_ids and datagram.get("status") == "COMPLETE":
            continue
        packet_ids = _string_list(datagram.get("packetRefIds"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "datagram packetRefIds")
        if any(packet_id not in packet_refs for packet_id in packet_ids):
            raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "datagram references an unknown packet")
        results.append({
            "datagramId": identifier,
            "sourceRefs": {
                "captureId": source.get("input", {}).get("captureId"),
                "packetRefIds": packet_ids,
                "datagramIds": [identifier],
                "eventIds": [],
            },
            "quality": {"datagramStatus": datagram.get("status")},
            "scoring": {
                "disposition": "NOT-SCORED",
                "protocolVerdict": "NOT-EVALUATED",
                "reason": f"OFFLINE-DATAGRAM-QUALITY-{datagram.get('status')}",
            },
        })
    if not results:
        raise OfflineReplayError("OFFLINE-BRIDGE-NO-RECORD", "offline evidence has no bounded record available for replay")
    return results


def _nonprojectable_by_source(value: object) -> dict[str, tuple[dict[str, str], ...]]:
    """Return source-proven non-projectable dispositions by exact source ID."""

    if type(value) is not list:
        raise OfflineReplayError("OFFLINE-PROJECTION-SHAPE-ERROR", "contract nonProjectable must be an array")
    result: dict[str, list[dict[str, str]]] = {}
    for item in value:
        mapping = _mapping(item, "OFFLINE-PROJECTION-SHAPE-ERROR", "nonProjectable record")
        if set(mapping) != {"sourceType", "sourceId", "reason"}:
            raise OfflineReplayError("OFFLINE-PROJECTION-SHAPE-ERROR", "nonProjectable record uses unknown or missing fields")
        source_type = _nonblank_string(mapping.get("sourceType"), "OFFLINE-PROJECTION-SHAPE-ERROR", "nonProjectable sourceType")
        source_id = _nonblank_string(mapping.get("sourceId"), "OFFLINE-PROJECTION-SHAPE-ERROR", "nonProjectable sourceId")
        reason = _nonblank_string(mapping.get("reason"), "OFFLINE-PROJECTION-SHAPE-ERROR", "nonProjectable reason")
        result.setdefault(source_id, []).append({
            "sourceType": source_type,
            "sourceId": source_id,
            "reason": reason,
        })
    return {identifier: tuple(rows) for identifier, rows in result.items()}


def _adapt_nonprojectable_transfer(
    source: dict[str, Any],
    transfer: dict[str, Any],
    *,
    packet_refs: Mapping[str, dict[str, Any]],
    datagrams: Mapping[str, dict[str, Any]],
    events: Mapping[str, dict[str, Any]],
    reasons: tuple[dict[str, str], ...],
) -> dict[str, Any]:
    """Keep a producer-limited transfer visible without fabricating ownership."""

    transfer_id = _nonblank_string(transfer.get("transferId"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transferId")
    packet_ids = _string_list(transfer.get("packetRefIds"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transfer packetRefIds")
    datagram_ids = _string_list(transfer.get("datagramIds"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transfer datagramIds")
    if any(identifier not in packet_refs for identifier in packet_ids):
        raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "non-projectable transfer references an unknown packet")
    if any(identifier not in datagrams for identifier in datagram_ids):
        raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "non-projectable transfer references an unknown datagram")
    event_ids = [identifier for identifier, event in events.items() if event.get("transferId") == transfer_id]
    return {
        "transferId": transfer_id,
        "sourceRefs": {
            "captureId": source.get("input", {}).get("captureId"),
            "packetRefIds": packet_ids,
            "datagramIds": datagram_ids,
            "eventIds": event_ids,
        },
        "quality": {
            "transferReconstructionStatus": transfer.get("reconstructionStatus"),
            "datagrams": [
                {"datagramId": identifier, "status": datagrams[identifier].get("status")}
                for identifier in datagram_ids
            ],
            "events": [
                {
                    "eventId": identifier,
                    "layer": events[identifier].get("layer"),
                    "evidenceStatus": events[identifier].get("evidenceStatus"),
                }
                for identifier in event_ids
            ],
            "nonProjectable": list(reasons),
        },
        "scoring": {
            "disposition": "NOT-SCORED",
            "protocolVerdict": "NOT-EVALUATED",
            "reason": "OFFLINE-REQUEST-PROJECTION-UNAVAILABLE",
        },
    }


def _adapt_transfer(
    source: dict[str, Any],
    transfer: dict[str, Any],
    request_projection: dict[str, Any],
    *,
    packet_refs: Mapping[str, dict[str, Any]],
    datagrams: Mapping[str, dict[str, Any]],
    events: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    transfer_id = _nonblank_string(transfer.get("transferId"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transferId")
    transfer_packet_ids = _string_list(transfer.get("packetRefIds"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transfer packetRefIds")
    transfer_datagram_ids = _string_list(transfer.get("datagramIds"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transfer datagramIds")
    source_witness = _mapping(transfer.get("sourceWitness"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "transfer sourceWitness")
    request_packet_id = source_witness.get("requestPacketRefId")
    completion_packet_id = source_witness.get("completionPacketRefId")
    if type(request_packet_id) is not str or request_packet_id not in packet_refs:
        raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "transfer request witness does not name a known packet")
    if completion_packet_id is not None and (type(completion_packet_id) is not str or completion_packet_id not in packet_refs):
        raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "transfer completion witness does not name a known packet")
    if request_packet_id not in transfer_packet_ids or (
        completion_packet_id is not None and completion_packet_id not in transfer_packet_ids
    ):
        raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "transfer witness is outside transfer packet ancestry")

    projected_payload = _mapping(request_projection.get("payload"), "OFFLINE-PROJECTION-SHAPE-ERROR", "request projection payload")
    event_payload = _mapping(
        projected_payload.get("payload"), "OFFLINE-PROJECTION-SHAPE-ERROR", "request event payload",
    )
    request_kind = transfer.get("requestKind")
    if request_kind not in {"RRQ", "WRQ"} or event_payload.get("type") != request_kind:
        raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "projected request type differs from its transfer witness")
    key = _nonblank_string(projected_payload.get("correlationKey"), "OFFLINE-PROJECTION-SHAPE-ERROR", "request correlationKey")
    raw_refs = _string_list(projected_payload.get("rawRefs"), "OFFLINE-PROJECTION-SHAPE-ERROR", "request projection rawRefs")
    request_packet = packet_refs[request_packet_id]
    expected_request_ref = _contract_packet_ref(request_packet)
    if raw_refs != [expected_request_ref]:
        raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "projected request does not retain its exact request packet reference")

    related_events = [
        event_id for event_id, event in events.items()
        if event.get("transferId") == transfer_id
    ]
    datagram_quality: list[dict[str, Any]] = []
    for identifier in transfer_datagram_ids:
        item = datagrams.get(identifier)
        if item is None:
            raise OfflineReplayError("OFFLINE-PROJECTION-REFERENCE-ERROR", "transfer references an unknown datagram")
        datagram_quality.append({"datagramId": identifier, "status": item.get("status")})
    event_quality = [
        {"eventId": identifier, "layer": events[identifier].get("layer"), "evidenceStatus": events[identifier].get("evidenceStatus")}
        for identifier in related_events
    ]
    base: dict[str, Any] = {
        "transferId": transfer_id,
        "sourceRefs": {
            "captureId": source.get("input", {}).get("captureId"),
            "requestProjectionId": request_projection.get("sourceId"),
            "packetRefIds": transfer_packet_ids,
            "datagramIds": transfer_datagram_ids,
            "eventIds": related_events,
            "requestPacketRefId": request_packet_id,
            "completionPacketRefId": completion_packet_id,
        },
        "quality": {
            "transferReconstructionStatus": transfer.get("reconstructionStatus"),
            "datagrams": datagram_quality,
            "events": event_quality,
        },
        "scoring": {"disposition": "NOT-SCORED", "protocolVerdict": "NOT-EVALUATED"},
    }

    if transfer.get("reconstructionStatus") != "COMPLETE":
        return _not_scored(base, "OFFLINE-TRANSFER-NOT-COMPLETE")
    if completion_packet_id is None:
        return _not_scored(base, "OFFLINE-COMPLETION-WITNESS-UNAVAILABLE")
    if any(item["status"] != "COMPLETE" for item in datagram_quality):
        return _not_scored(base, "OFFLINE-DATAGRAM-QUALITY-NOT-COMPLETE")
    if any(item["evidenceStatus"] != "PARSED" for item in event_quality if item["layer"] == "PARSE-RESULT"):
        return _not_scored(base, "OFFLINE-PARSE-QUALITY-NOT-PARSED")

    completion_packet = packet_refs[completion_packet_id]
    timing = _structural_clock_pair(request_packet, completion_packet)
    base["clock"] = timing[0]
    if timing[1] is not None:
        return _not_scored(base, timing[1])
    request_timestamp, response_timestamp = timing[2]
    if completion_packet.get("packetIndex") <= request_packet.get("packetIndex"):
        return _not_scored(base, "OFFLINE-NONSEQUENTIAL-TRANSFER-WITNESS")

    # This is intentionally a *structural candidate*, not a qualified method
    # response.  The final DATA witness is source-proven, but the offline
    # capture lacks the execution, clock, uncertainty and deadline evidence
    # required for a scored ObservationAssessment.  We therefore expose only
    # the public ownership replay and force the result to NOT-SCORED.
    contract = _offline_structural_contract(request_kind, key, timing[0]["clockDomain"], timing[0]["unit"])
    structural_events = (
        OwnershipEvent(
            f"OFFLINE-REQUEST:{transfer_id}", 1, "REQUEST", key, request_kind, request_timestamp,
        ),
        OwnershipEvent(
            f"OFFLINE-FINAL-DATA-CANDIDATE:{transfer_id}", 2, "RESPONSE", key,
            "OFFLINE-TFTP-FINAL-DATA-CANDIDATE", response_timestamp,
        ),
    )
    replay = replay_ownership(structural_events, contract)
    base["ownershipReplay"] = _ownership_mapping(replay)
    return _not_scored(base, "OFFLINE-CLOCK-ACCURACY-UNKNOWN")


def _offline_structural_contract(request_kind: str, key: str, clock_domain: str, unit: str) -> InterpretationContract:
    """Make the fixed, explicitly unqualified structural replay contract."""

    return InterpretationContract(
        "OFFLINE-REPLAY-STRUCTURAL-1.0",
        request_kind,
        "OFFLINE-TFTP-FINAL-DATA-CANDIDATE",
        key,
        "UNIQUE-KEY",
        False,
        "OFFLINE-CANCEL-UNSUPPORTED",
        "OFFLINE-SUPERSEDE-UNSUPPORTED",
        Interval(Fraction(0), Fraction(0), True, True),
        Interval(Fraction(0), Fraction(0), True, True),
        f"OFFLINE:{clock_domain}",
        "OFFLINE-CLOCK-ACCURACY-UNKNOWN",
        "OFFLINE-ERROR-BUDGET-UNAVAILABLE",
        unit,
        False,
        False,
        "UNRESOLVED",
        None,
        None,
        True,
    )


def _structural_clock_pair(
    request_packet: dict[str, Any], completion_packet: dict[str, Any],
) -> tuple[dict[str, Any], str | None, tuple[Fraction, Fraction] | None]:
    request_timestamp = request_packet.get("timestamp")
    completion_timestamp = completion_packet.get("timestamp")
    if type(request_timestamp) is not dict or type(completion_timestamp) is not dict:
        return ({"qualification": "UNKNOWN"}, "OFFLINE-CLOCK-UNKNOWN", None)
    fields = ("ticks", "ticksPerSecond", "offsetSeconds", "clockDomain", "accuracy")
    if any(field not in request_timestamp or field not in completion_timestamp for field in fields):
        return ({"qualification": "UNKNOWN"}, "OFFLINE-CLOCK-UNKNOWN", None)
    if request_timestamp.get("accuracy") != "UNKNOWN" or completion_timestamp.get("accuracy") != "UNKNOWN":
        return ({"qualification": "UNKNOWN"}, "OFFLINE-CLOCK-ACCURACY-UNRECOGNISED", None)
    if (
        request_timestamp.get("clockDomain") != completion_timestamp.get("clockDomain")
        or request_timestamp.get("ticksPerSecond") != completion_timestamp.get("ticksPerSecond")
        or request_timestamp.get("offsetSeconds") != completion_timestamp.get("offsetSeconds")
    ):
        return (
            {
                "requestClockDomain": request_timestamp.get("clockDomain"),
                "responseClockDomain": completion_timestamp.get("clockDomain"),
                "qualification": "CROSS-DOMAIN-UNPROVEN",
            },
            "OFFLINE-CLOCK-DOMAIN-UNPROVEN",
            None,
        )
    ticks_per_second = request_timestamp.get("ticksPerSecond")
    request_ticks = request_timestamp.get("ticks")
    response_ticks = completion_timestamp.get("ticks")
    if (
        type(ticks_per_second) is not int or ticks_per_second <= 0
        or type(request_ticks) is not int or type(response_ticks) is not int
    ):
        return ({"qualification": "UNKNOWN"}, "OFFLINE-CLOCK-UNKNOWN", None)
    clock_domain = request_timestamp["clockDomain"]
    return (
        {
            "clockDomain": clock_domain,
            "accuracy": "UNKNOWN",
            "ticksPerSecond": ticks_per_second,
            "offsetSeconds": request_timestamp["offsetSeconds"],
            "unit": f"ticks/{ticks_per_second}",
            "qualification": "UNQUALIFIED",
        },
        None,
        (Fraction(request_ticks, ticks_per_second), Fraction(response_ticks, ticks_per_second)),
    )


def _ownership_mapping(value: OwnershipReplay) -> dict[str, Any]:
    return {
        "contractId": value.contract_id,
        "requestDispositions": dict(value.request_dispositions),
        "responseResolutions": [
            {
                "responseId": item.response_id,
                "status": item.status,
                "ownerRequestId": item.owner_request_id,
                "candidateRequestIds": list(item.candidate_request_ids),
                "evidenceRefs": list(item.evidence_refs),
                "diagnosticCodes": [diagnostic.code for diagnostic in item.diagnostics],
            }
            for item in value.response_resolutions.values()
        ],
        "diagnosticCodes": [diagnostic.code for diagnostic in value.diagnostics],
        "qualified": False,
    }


def _not_scored(record: dict[str, Any], reason: str) -> dict[str, Any]:
    record["scoring"]["reason"] = reason
    return record


def _validate_source_evidence(source: dict[str, Any]) -> None:
    # Reject an unsupported producer identity before running the general
    # envelope validator.  That keeps a version/projection misuse visibly
    # distinct from an ordinary malformed evidence record at the bridge
    # boundary.
    if source.get("artifactType") != "CLTAV-OFFLINE-INTAKE-EVIDENCE" or source.get("schemaVersion") != "1.0":
        raise OfflineReplayError("OFFLINE-EVIDENCE-VERSION-ERROR", "offline evidence artifact type or schema version is unsupported")
    errors = evidence_errors(source)
    if errors:
        raise OfflineReplayError("OFFLINE-EVIDENCE-INVALID", "; ".join(errors))


def _rebuild_source_evidence(source: dict[str, Any], capture_path: Path) -> dict[str, Any]:
    input_value = _mapping(source.get("input"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "offline evidence input")
    tool = _mapping(source.get("tool"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "offline evidence tool")
    capture_id = _nonblank_string(input_value.get("captureId"), "OFFLINE-EVIDENCE-SHAPE-ERROR", "captureId")
    source_commit = validate_source_commit(tool.get("sourceCommit"))
    config = _config_from_mapping(source.get("runParameters"))
    try:
        rebuilt = run_capture(capture_path, capture_id=capture_id, config=config).to_dict(source_commit=source_commit)
    except IntakeError as exc:
        raise OfflineReplayError("OFFLINE-SOURCE-REBUILD-ERROR", f"{exc.code}: {exc}") from exc
    errors = evidence_errors(rebuilt)
    if errors:
        raise OfflineReplayError("OFFLINE-SOURCE-REBUILD-ERROR", "; ".join(errors))
    return rebuilt


def _config_from_mapping(value: object) -> IntakeConfig:
    mapping = _mapping(value, "OFFLINE-EVIDENCE-SHAPE-ERROR", "runParameters")
    default = IntakeConfig().to_dict()
    if set(mapping) != set(default):
        raise OfflineReplayError("OFFLINE-EVIDENCE-SHAPE-ERROR", "runParameters use unknown or missing fields")
    if any(type(mapping[name]) is not int for name in default):
        raise OfflineReplayError("OFFLINE-EVIDENCE-SHAPE-ERROR", "runParameters must contain exact integer values")
    arguments = {
        "max_packet_bytes": mapping["maxPacketBytes"],
        "max_container_block_bytes": mapping["maxContainerBlockBytes"],
        "max_active_datagrams": mapping["maxActiveDatagrams"],
        "max_datagram_bytes": mapping["maxDatagramBytes"],
        "max_fragments_per_datagram": mapping["maxFragmentsPerDatagram"],
        "max_active_transfers": mapping["maxActiveTransfers"],
        "max_transfer_records": mapping["maxTransferRecords"],
        "max_transfer_bytes": mapping["maxTransferBytes"],
        "max_active_transfer_bytes": mapping["maxActiveTransferBytes"],
        "max_completed_payload_bytes": mapping["maxCompletedPayloadBytes"],
        "max_evidence_records": mapping["maxEvidenceRecords"],
        "max_packet_refs": mapping["maxPacketRefs"],
        "max_diagnostics": mapping["maxDiagnostics"],
        "max_events": mapping["maxEvents"],
        "max_interfaces": mapping["maxInterfaces"],
        "tftp_service_port": mapping["tftpServicePort"],
    }
    return IntakeConfig(**arguments)


def _validate_bridge_shape(document: dict[str, Any]) -> None:
    required = {
        "artifactType", "schemaVersion", "mode", "boundary", "source", "offlineEvidence",
        "records", "activeExecution", "integrity",
    }
    if set(document) != required:
        raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay has unknown or missing top-level fields")
    if document.get("artifactType") != OFFLINE_REPLAY_ARTIFACT_TYPE or document.get("schemaVersion") != OFFLINE_REPLAY_SCHEMA_VERSION:
        raise OfflineReplayError("OFFLINE-BRIDGE-VERSION-ERROR", "offline replay artifact type or schema version is unsupported")
    if document.get("mode") != "OFFLINE-REPLAY":
        raise OfflineReplayError("OFFLINE-BRIDGE-MODE-ERROR", "offline replay mode is invalid")
    boundary = _mapping(document["boundary"], "OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay boundary")
    if boundary.get("conformanceVerdict") != "NOT-EVALUATED" or boundary.get("integrity") != "NOT-EVALUATED":
        raise OfflineReplayError("OFFLINE-BRIDGE-BOUNDARY-ERROR", "offline replay cannot claim conformance or integrity evaluation")
    source = _mapping(document["source"], "OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay source")
    if set(source) != {"offlineEvidenceSha256", "captureIdentity", "tool", "contractProjectionIdentity"}:
        raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay source uses unknown or missing fields")
    if type(source["offlineEvidenceSha256"]) is not str or len(source["offlineEvidenceSha256"]) != 64:
        raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay source hash is invalid")
    if type(document["offlineEvidence"]) is not dict or type(document["records"]) is not list:
        raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay evidence or records are invalid")
    active = _mapping(document["activeExecution"], "OFFLINE-BRIDGE-SHAPE-ERROR", "offline active execution")
    if active != {
        "issuedActionCount": 0,
        "chargedCost": 0,
        "attemptCount": 0,
        "resetApplied": False,
        "historyUpdated": False,
        "activeFeedbackApplied": False,
    }:
        raise OfflineReplayError("OFFLINE-BRIDGE-MODE-ERROR", "offline replay cannot declare active execution side effects")


def _validate_bridge_integrity(document: dict[str, Any]) -> None:
    integrity = _mapping(document.get("integrity"), "OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay integrity")
    if set(integrity) != {"canonicalPayloadSha256"} or type(integrity["canonicalPayloadSha256"]) is not str:
        raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay integrity is invalid")
    payload = {key: value for key, value in document.items() if key != "integrity"}
    actual = sha256(canonical_json_bytes(payload)).hexdigest()
    if integrity["canonicalPayloadSha256"] != actual:
        raise OfflineReplayError("OFFLINE-BRIDGE-INTEGRITY-ERROR", "offline replay canonical payload hash differs")


def _load_bridge_bytes(raw: bytes) -> dict[str, Any]:
    if type(raw) is not bytes:
        raise OfflineReplayError("OFFLINE-BRIDGE-READ-ERROR", "offline replay must be supplied as bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise OfflineReplayError("OFFLINE-BRIDGE-ENCODING-ERROR", "offline replay must be UTF-8") from exc
    try:
        value = json.loads(text, object_pairs_hook=_no_duplicate_object, parse_constant=_reject_json_constant)
    except OfflineReplayError:
        raise
    except json.JSONDecodeError as exc:
        raise OfflineReplayError("OFFLINE-BRIDGE-JSON-ERROR", "offline replay is not valid JSON") from exc
    if type(value) is not dict:
        raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", "offline replay root must be an object")
    _reject_floats(value)
    if canonical_json_bytes(value) != raw:
        raise OfflineReplayError("OFFLINE-BRIDGE-NONCANONICAL-ENCODING", "offline replay must use canonical UTF-8 sorted-key encoding")
    return value


def _no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", f"offline replay repeats JSON key {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise OfflineReplayError("OFFLINE-BRIDGE-JSON-ERROR", f"offline replay uses unsupported JSON constant {value}")


def _reject_floats(value: object) -> None:
    if type(value) is float:
        raise OfflineReplayError("OFFLINE-BRIDGE-SHAPE-ERROR", "offline bridge does not accept floating-point values")
    if type(value) is dict:
        for nested in value.values():
            _reject_floats(nested)
    elif type(value) is list:
        for nested in value:
            _reject_floats(nested)


def _id_map(value: object, key: str, label: str) -> dict[str, dict[str, Any]]:
    if type(value) is not list:
        raise OfflineReplayError("OFFLINE-EVIDENCE-SHAPE-ERROR", f"{label} must be an array")
    result: dict[str, dict[str, Any]] = {}
    for item in value:
        mapping = _mapping(item, "OFFLINE-EVIDENCE-SHAPE-ERROR", label)
        identifier = _nonblank_string(mapping.get(key), "OFFLINE-EVIDENCE-SHAPE-ERROR", key)
        if identifier in result:
            raise OfflineReplayError("OFFLINE-EVIDENCE-REFERENCE-ERROR", f"{label} repeats {key}")
        result[identifier] = mapping
    return result


def _mapping(value: object, code: str, label: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise OfflineReplayError(code, f"{label} must be an object")
    return value


def _nonblank_string(value: object, code: str, label: str) -> str:
    if type(value) is not str or not value:
        raise OfflineReplayError(code, f"{label} must be a nonblank string")
    return value


def _string_list(value: object, code: str, label: str) -> list[str]:
    if type(value) is not list or any(type(item) is not str or not item for item in value):
        raise OfflineReplayError(code, f"{label} must be an array of nonblank strings")
    return list(value)


def _contract_packet_ref(packet: Mapping[str, Any]) -> str:
    return f"{packet.get('captureId')}:{packet.get('sectionId')}:{packet.get('interfaceId')}:{packet.get('packetIndex')}"


def _first_difference(actual: object, expected: object, path: str) -> str | None:
    if type(actual) is not type(expected):
        return path
    if type(actual) is dict:
        actual_keys = set(actual)
        expected_keys = set(expected)
        if actual_keys != expected_keys:
            missing = sorted(expected_keys - actual_keys)
            extra = sorted(actual_keys - expected_keys)
            return f"{path}.{(missing[0] if missing else extra[0])}"
        for key in sorted(actual):
            difference = _first_difference(actual[key], expected[key], f"{path}.{key}")
            if difference:
                return difference
        return None
    if type(actual) is list:
        if len(actual) != len(expected):
            return f"{path}[length]"
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            difference = _first_difference(left, right, f"{path}[{index}]")
            if difference:
                return difference
        return None
    return None if actual == expected else path


def _snapshot_digest(run: OfflineReplayRun) -> str:
    """Bind the opaque run to the exact source and derived bridge records."""

    try:
        snapshot = {
            "offlineEvidenceRawSha256": sha256(run._offline_evidence_raw).hexdigest(),
            "offlineEvidence": run._offline_evidence,
            "records": list(run._records),
        }
        return sha256(canonical_json_bytes(snapshot)).hexdigest()
    except OfflineReplayError as exc:
        raise OfflineReplayError(
            "OFFLINE-BRIDGE-PROVENANCE-ERROR",
            "offline replay run contains a noncanonical or altered source snapshot",
        ) from exc


def _require_run(value: object) -> OfflineReplayRun:
    if type(value) is not OfflineReplayRun or value._token is not _RUN_TOKEN:
        raise OfflineReplayError("OFFLINE-BRIDGE-PROVENANCE-ERROR", "offline replay run was not source-rebuilt by the bridge")
    if value._snapshot_digest != _snapshot_digest(value):
        raise OfflineReplayError("OFFLINE-BRIDGE-PROVENANCE-ERROR", "offline replay run changed after source rebuild")
    return value


def _resolved_regular_file(path: Path, *, code: str) -> Path:
    if path.is_symlink():
        raise OfflineReplayError(code, "offline bridge input must not be a symbolic link")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise OfflineReplayError(code, str(exc) or type(exc).__name__) from exc
    if not resolved.is_file():
        raise OfflineReplayError(code, "offline bridge input must be an ordinary file")
    return resolved


def _safe_output_target(output: Path, run: OfflineReplayRun) -> Path:
    try:
        target = output.resolve(strict=False)
    except OSError as exc:
        raise OfflineReplayError("OFFLINE-BRIDGE-OUTPUT-PATH-ERROR", str(exc) or type(exc).__name__) from exc
    forbidden = {run.capture_path}
    if run.evidence_path is not None:
        forbidden.add(run.evidence_path)
    if target in forbidden:
        raise OfflineReplayError("OFFLINE-BRIDGE-OUTPUT-PATH-ERROR", "offline replay output must not overwrite an input")
    if output.is_symlink() or (target.exists() and not target.is_file()):
        raise OfflineReplayError("OFFLINE-BRIDGE-OUTPUT-PATH-ERROR", "offline replay output must be an ordinary file")
    return target


def _write_private_stage(path: Path, raw: bytes) -> None:
    try:
        with path.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError as exc:
        raise OfflineReplayError("OFFLINE-BRIDGE-PUBLISH-ERROR", str(exc) or type(exc).__name__) from exc


def _assert_owned_target(target: Path, validator: Callable[[bytes], None]) -> None:
    try:
        validator(target.read_bytes())
    except (OSError, OfflineReplayError) as exc:
        raise OfflineReplayError("OFFLINE-BRIDGE-OUTPUT-PATH-ERROR", "refusing to replace an unowned offline replay artifact") from exc


def _restore_after_failure(
    target: Path,
    backup: Path,
    moved_old: bool,
    published: bool,
    replace_fn: Callable[[Path, Path], None],
) -> None:
    try:
        if moved_old and backup.exists():
            if published and target.exists():
                target.unlink()
            replace_fn(backup, target)
        elif published and target.exists():
            target.unlink()
    except OSError as exc:
        raise OfflineReplayError(
            "OFFLINE-BRIDGE-ROLLBACK-ERROR",
            f"rollback did not complete; prior artifact remains in {backup.name}: {str(exc) or type(exc).__name__}",
        ) from exc


def _safe_unlink(path: Path) -> None:
    try:
        if path.exists():
            path.unlink()
    except OSError:
        # Do not replace a primary relation/publish error with cleanup noise.
        pass
