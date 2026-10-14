"""Small runtime validation for the versioned offline-evidence envelope."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Any

from jsonschema import Draft202012Validator

from .contracts import evidence_projection_errors
from .controlled_resources import ControlledResourceError, controlled_resource_json
from .events import infer_file_role
from .identity import DEVELOPMENT_CONTRACT_PATH, DEVELOPMENT_CONTRACT_SHA256


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SOURCE_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
ABSOLUTE_PATH_RE = re.compile(r"(?:^|[\s\"'])((?:[A-Za-z]:[\\/])|/(?:[^\s\"']+))")


def evidence_errors(data: object) -> list[str]:
    """Validate published evidence against the controlled schema and relations.

    JSON Schema is a runtime dependency rather than a best-effort developer
    extra: a publisher must never claim to validate a shape it does not execute.
    The semantic pass below deliberately covers cross-record parentage that a
    local JSON Schema cannot express succinctly.
    """
    schema_errors = _schema_errors(data)
    if schema_errors:
        return schema_errors
    if not isinstance(data, dict):
        return ["evidence must be an object"]
    errors: list[str] = []
    _check_counts(data, errors)
    _check_controlled_contract_identities(data, errors)
    _check_provenance(data, errors)
    _check_packet_capture_quality(data, errors)
    _check_file_length_quality(data, errors)
    _check_execution_shape(data, errors)
    errors.extend(evidence_projection_errors(data))
    rendered = _rendered_strings(data)
    if ABSOLUTE_PATH_RE.search(rendered):
        errors.append("evidence must not contain an absolute machine path")
    forbidden = {"rawPayload", "payloadBytes", "completePayloadBytes", "capturePath", "corpusRoot"}
    found = _find_forbidden_keys(data, forbidden)
    if found:
        errors.append("evidence contains forbidden payload/path field " + found[0])
    return errors


def evidence_failure_code(errors: list[str]) -> str:
    """Return a stable tool code when validation failed before interpretation."""
    for error in errors:
        code = error.split(":", 1)[0]
        if code.startswith("CONTROLLED-RESOURCE-") or code.startswith("DEVELOPMENT-CONTRACT-"):
            return code
    return "EVIDENCE-SCHEMA-ERROR"


@lru_cache(maxsize=1)
def _validator() -> Draft202012Validator:
    try:
        schema = controlled_resource_json("evidence-schema")
    except ControlledResourceError as exc:  # pragma: no cover - package/install failure boundary
        raise RuntimeError(f"{exc.code}: {exc}") from exc
    return Draft202012Validator(schema)


def _schema_errors(data: object) -> list[str]:
    try:
        errors = sorted(_validator().iter_errors(data), key=lambda item: list(item.absolute_path))
    except RuntimeError as exc:
        return [str(exc)]
    return [
        "schema " + (".".join(str(part) for part in error.absolute_path) or "$") + f": {error.message}"
        for error in errors
    ]


def _check_counts(data: dict[str, Any], errors: list[str]) -> None:
    counts = data.get("counts")
    expected = {
        "evidencePacketRefs": "packetRefs",
        "datagrams": "datagrams",
        "transfers": "transfers",
        "events": "events",
        "diagnostics": "diagnostics",
    }
    if not isinstance(counts, dict):
        errors.append("counts must be an object")
        return
    for count_name, list_name in expected.items():
        value = counts.get(count_name)
        records = data.get(list_name)
        if not isinstance(value, int) or value < 0:
            errors.append(f"counts.{count_name} is invalid")
        elif isinstance(records, list) and value != len(records):
            errors.append(f"counts.{count_name} differs from {list_name} length")
    container_packets = counts.get("containerPackets")
    if not isinstance(container_packets, int) or container_packets < 0:
        errors.append("counts.containerPackets is invalid")
    parameters = data.get("runParameters")
    container = data.get("input", {}).get("container") if isinstance(data.get("input"), dict) else None
    interfaces = container.get("interfaces") if isinstance(container, dict) else None
    if interfaces is None and data.get("executionStatus") == "FATAL-INPUT-ERROR":
        interfaces = []
    if not isinstance(parameters, dict) or not isinstance(interfaces, list):
        errors.append("runParameters or input container interfaces are unavailable for resource-bound validation")
        return
    try:
        evidence_total = len(interfaces) + sum(
            len(data[name]) for name in ("packetRefs", "datagrams", "transfers", "events", "diagnostics")
        )
        if evidence_total > parameters["maxEvidenceRecords"]:
            errors.append("published evidence exceeds runParameters.maxEvidenceRecords")
        if len(interfaces) > parameters["maxInterfaces"]:
            errors.append("published interfaces exceed runParameters.maxInterfaces")
        if len(data["packetRefs"]) > parameters["maxPacketRefs"]:
            errors.append("published packetRefs exceed runParameters.maxPacketRefs")
        if len(data["transfers"]) > parameters["maxTransferRecords"]:
            errors.append("published transfers exceed runParameters.maxTransferRecords")
        if len(data["events"]) > parameters["maxEvents"]:
            errors.append("published events exceed runParameters.maxEvents")
        if len(data["diagnostics"]) > parameters["maxDiagnostics"]:
            errors.append("published diagnostics exceed runParameters.maxDiagnostics")
    except (KeyError, TypeError):
        errors.append("runParameters cannot support resource-bound validation")


def _check_controlled_contract_identities(data: dict[str, Any], errors: list[str]) -> None:
    """Bind both producer and adapter claims to the accepted snapshot.

    The schema intentionally permits an identity-shaped value so a stale or
    tampered envelope can receive a useful semantic diagnostic.  Publication
    is nevertheless allowed only when the tool and the projection name the
    exact same controlled contract consumed by this release.
    """
    expected = [{
        "path": DEVELOPMENT_CONTRACT_PATH,
        "sha256": DEVELOPMENT_CONTRACT_SHA256,
        "version": "PR19-ACCEPTED-SNAPSHOT",
    }]
    tool = data.get("tool")
    if not isinstance(tool, dict) or tool.get("contractIdentities") != expected:
        errors.append("tool contractIdentities do not match the accepted snapshot")
    projection = data.get("contractProjection")
    if not isinstance(projection, dict) or projection.get("contractIdentity") != expected[0]:
        errors.append("contract projection identity does not match the accepted snapshot")


def _check_execution_shape(data: dict[str, Any], errors: list[str]) -> None:
    """Tie declared execution status to observable evidence, without verdicts."""
    execution = data["executionStatus"]
    diagnostics = data["diagnostics"]
    non_complete = any(item.get("status") != "COMPLETE" for item in _objects(data["datagrams"])) or any(
        item.get("reconstructionStatus") != "COMPLETE" for item in _objects(data["transfers"])
    )
    parse_issue = any(
        item.get("layer") == "PARSE-RESULT"
        and isinstance(item.get("fields"), dict)
        and item["fields"].get("parseStatus") != "PARSED"
        for item in _objects(data["events"])
        if isinstance(item, dict)
    )
    if execution == "COMPLETE" and (diagnostics or non_complete or parse_issue):
        errors.append("COMPLETE execution cannot contain controlled issues")
    if execution == "COMPLETE-WITH-CONTROLLED-ISSUES" and not (diagnostics or non_complete or parse_issue):
        errors.append("controlled-issues execution must retain a controlled issue")
    if execution == "FATAL-INPUT-ERROR":
        if any(data[key] for key in ("packetRefs", "datagrams", "transfers", "events")):
            errors.append("fatal input evidence must not publish partial reconstruction records")
        if len(diagnostics) != 1 or diagnostics[0].get("severity") != "ERROR":
            errors.append("fatal input evidence must contain exactly one ERROR diagnostic")


def _check_provenance(data: dict[str, Any], errors: list[str]) -> None:
    input_capture_id = data["input"]["captureId"]
    packet_ids = _ids(data.get("packetRefs"), "packetRefId", "packetRefs", errors)
    datagram_ids = _ids(data.get("datagrams"), "datagramId", "datagrams", errors)
    transfer_ids = _ids(data.get("transfers"), "transferId", "transfers", errors)
    _ids(data.get("events"), "eventId", "events", errors)
    for item in _objects(data.get("datagrams")):
        if not isinstance(item, dict):
            continue
        if item.get("captureId") != input_capture_id:
            errors.append("datagram captureId differs from input captureId")
        _require_known_ids(item.get("packetRefIds"), packet_ids, "datagram packetRefIds", errors)
        status = item.get("status")
        payload_length = item.get("payloadLength")
        if status == "COMPLETE" and (not isinstance(payload_length, int) or payload_length < 0):
            errors.append("complete datagram must declare a nonnegative payloadLength")
        if status != "COMPLETE" and payload_length is not None:
            errors.append("non-complete datagram must not publish a payloadLength")
    for item in _objects(data.get("transfers")):
        if not isinstance(item, dict):
            continue
        if item.get("captureId") != input_capture_id:
            errors.append("transfer captureId differs from input captureId")
        _require_known_ids(item.get("packetRefIds"), packet_ids, "transfer packetRefIds", errors)
        _require_known_ids(item.get("datagramIds"), datagram_ids, "transfer datagramIds", errors)
        _check_transfer_source_witness(item, packet_ids, datagram_ids, data.get("datagrams"), errors)
        block = item.get("blockSize")
        if not isinstance(block, dict):
            errors.append("transfer blockSize must be an object")
            continue
        option_status = block.get("status")
        value = block.get("value")
        if option_status == "DEFAULTED" and value != 512:
            errors.append("DEFAULTED transfer blockSize must be 512")
        if option_status == "UNKNOWN" and value is not None:
            errors.append("UNKNOWN transfer blockSize must be null")
        if option_status == "ACCEPTED" and (not isinstance(value, int) or value < 1):
            errors.append("ACCEPTED transfer blockSize must be a positive integer")
        complete_length = item.get("completePayloadLength")
        if item.get("reconstructionStatus") == "COMPLETE" and (
            not isinstance(complete_length, int) or complete_length < 0
        ):
            errors.append("complete transfer must declare a nonnegative completePayloadLength")
        if item.get("reconstructionStatus") != "COMPLETE" and complete_length is not None:
            errors.append("non-complete transfer must not publish completePayloadLength")
    for item in _objects(data.get("events")):
        if not isinstance(item, dict):
            continue
        transfer_id = item.get("transferId")
        if not isinstance(transfer_id, str) or transfer_id not in transfer_ids:
            errors.append("event transferId does not reference a known transfer")
        _require_known_ids(item.get("sourceDatagramIds"), datagram_ids, "event sourceDatagramIds", errors)
        _require_known_ids(item.get("sourcePacketRefIds"), packet_ids, "event sourcePacketRefIds", errors)
        if isinstance(transfer_id, str) and transfer_id in transfer_ids:
            parent = next(candidate for candidate in _objects(data.get("transfers")) if candidate.get("transferId") == transfer_id)
            if item.get("sourceDatagramIds") != parent.get("datagramIds"):
                errors.append("event sourceDatagramIds do not exactly retain transfer ancestry")
            if item.get("sourcePacketRefIds") != parent.get("packetRefIds"):
                errors.append("event sourcePacketRefIds do not exactly retain transfer ancestry")
    for item in _objects(data.get("packetRefs")):
        if isinstance(item, dict) and item.get("captureId") != input_capture_id:
            errors.append("packetRef captureId differs from input captureId")
    for item in _objects(data.get("diagnostics")):
        if not isinstance(item, dict):
            continue
        packet_ref_id = item.get("packetRefId")
        if packet_ref_id is not None and packet_ref_id not in packet_ids:
            errors.append("diagnostic packetRefId does not reference a known packetRef")


def _ids(value: object, key: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(value, list):
        return set()
    result: set[str] = set()
    for item in value:
        if not isinstance(item, dict) or not isinstance(item.get(key), str) or not item[key]:
            errors.append(f"{label} contains an item without {key}")
            continue
        if item[key] in result:
            errors.append(f"{label} has repeated {key}")
            continue
        result.add(item[key])
    return result


def _require_known_ids(value: object, known: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return
    for item in value:
        if not isinstance(item, str) or item not in known:
            errors.append(f"{label} contains an unknown reference")
            return


def _check_transfer_source_witness(
    transfer: dict[str, Any], packet_ids: set[str], datagram_ids: set[str],
    datagrams: object, errors: list[str],
) -> None:
    """Validate exact provenance retained for a derived transfer projection."""
    witness = transfer.get("sourceWitness")
    packet_refs = transfer.get("packetRefIds")
    datagram_refs = transfer.get("datagramIds")
    if not isinstance(witness, dict):
        errors.append("transfer sourceWitness must be an object")
        return
    if witness.get("packetRefIds") != packet_refs:
        errors.append("transfer sourceWitness packetRefIds differ from transfer packetRefIds")
    if witness.get("datagramIds") != datagram_refs:
        errors.append("transfer sourceWitness datagramIds differ from transfer datagramIds")
    if not isinstance(packet_refs, list) or not isinstance(datagram_refs, list):
        return
    request = witness.get("requestPacketRefId")
    request_datagram = witness.get("requestDatagramId")
    if request is None or request_datagram is None:
        errors.append("transfer sourceWitness lacks its request packet/datagram pair")
    if request is not None and (not isinstance(request, str) or request not in packet_refs or request not in packet_ids):
        errors.append("transfer sourceWitness requestPacketRefId is not a known transfer packet")
    if request_datagram is not None and (
        not isinstance(request_datagram, str)
        or request_datagram not in datagram_refs
        or request_datagram not in datagram_ids
    ):
        errors.append("transfer sourceWitness requestDatagramId is not a known transfer datagram")
    blocks = witness.get("blockPacketRefIds")
    block_datagrams = witness.get("blockDatagramIds")
    if not isinstance(blocks, dict):
        errors.append("transfer sourceWitness blockPacketRefIds must be an object")
    else:
        for block, packet_ref_id in blocks.items():
            if not isinstance(block, str) or not isinstance(packet_ref_id, str) or packet_ref_id not in packet_refs or packet_ref_id not in packet_ids:
                errors.append("transfer sourceWitness blockPacketRefIds contains an unknown transfer packet")
                break
    if not isinstance(block_datagrams, dict):
        errors.append("transfer sourceWitness blockDatagramIds must be an object")
    else:
        for block, datagram_id in block_datagrams.items():
            if (
                not isinstance(block, str)
                or not isinstance(datagram_id, str)
                or datagram_id not in datagram_refs
                or datagram_id not in datagram_ids
            ):
                errors.append("transfer sourceWitness blockDatagramIds contains an unknown transfer datagram")
                break
    completion = witness.get("completionPacketRefId")
    completion_datagram = witness.get("completionDatagramId")
    if completion is not None and (not isinstance(completion, str) or completion not in packet_refs or completion not in packet_ids):
        errors.append("transfer sourceWitness completionPacketRefId is not a known transfer packet")
    if completion_datagram is not None and (
        not isinstance(completion_datagram, str)
        or completion_datagram not in datagram_refs
        or completion_datagram not in datagram_ids
    ):
        errors.append("transfer sourceWitness completionDatagramId is not a known transfer datagram")
    if any(not isinstance(value, str) or value not in datagram_ids for value in datagram_refs):
        errors.append("transfer datagramIds contains an unknown reference")
        return
    if isinstance(datagrams, list):
        rows = {
            item.get("datagramId"): item
            for item in datagrams if isinstance(item, dict) and isinstance(item.get("datagramId"), str)
        }
        source_packets: set[str] = set()
        for datagram_id in datagram_refs:
            row = rows.get(datagram_id)
            refs = row.get("packetRefIds") if isinstance(row, dict) else None
            if not isinstance(refs, list):
                errors.append("transfer source datagram lacks packet provenance")
                return
            source_packets.update(ref for ref in refs if isinstance(ref, str))
        if source_packets != set(packet_refs):
            errors.append("transfer packetRefIds do not exactly match its datagram ancestry")
        _check_transfer_witness_roles(
            transfer, witness, rows, blocks, block_datagrams, request, request_datagram,
            completion, completion_datagram, errors,
        )
    if transfer.get("reconstructionStatus") == "COMPLETE":
        terminal = transfer.get("terminalBlock")
        if (
            not isinstance(terminal, int)
            or terminal < 1
            or not isinstance(blocks, dict)
            or not isinstance(block_datagrams, dict)
        ):
            errors.append("complete transfer lacks terminal block source evidence")
            return
        expected_blocks = {str(number) for number in range(1, terminal + 1)}
        if set(blocks) != expected_blocks:
            errors.append("complete transfer block evidence does not cover the terminal range")
        if set(block_datagrams) != expected_blocks:
            errors.append("complete transfer block datagram evidence does not cover the terminal range")
        if completion != blocks.get(str(terminal)):
            errors.append("complete transfer completion evidence is not its terminal DATA source")
        if completion_datagram != block_datagrams.get(str(terminal)):
            errors.append("complete transfer completion datagram is not its terminal DATA source")


def _check_transfer_witness_roles(
    transfer: dict[str, Any],
    witness: dict[str, Any],
    datagrams: dict[str, dict[str, Any]],
    blocks: object,
    block_datagrams: object,
    request_packet: object,
    request_datagram: object,
    completion_packet: object,
    completion_datagram: object,
    errors: list[str],
) -> None:
    """Bind every projected TFTP role to the actual packet-bearing datagram.

    A transfer's broad ancestry is deliberately not a substitute for its
    request/DATA roles: a request packet may be associated with a completed
    session but can never be substituted for a DATA source.  The envelope
    contains no payload bytes, so this check uses the independently retained
    transport endpoints and datagram membership as the source-bound boundary.
    """
    client = transfer.get("clientEndpoint")
    server = transfer.get("serverEndpoint")
    request_kind = transfer.get("requestKind")
    if (
        not isinstance(client, dict)
        or not isinstance(server, dict)
        or not isinstance(client.get("address"), str)
        or not isinstance(server.get("address"), str)
        or request_kind not in {"RRQ", "WRQ"}
    ):
        return
    transfer_datagram_refs = transfer.get("datagramIds")
    if request_packet is not None or request_datagram is not None:
        if not _witness_packet_in_datagram(request_packet, request_datagram, datagrams):
            errors.append("transfer request source packet is not carried by its request datagram")
        elif not _datagram_has_direction(
            datagrams.get(request_datagram), client["address"], server["address"]
        ):
            errors.append("transfer request source datagram has the wrong endpoint direction")
        elif (
            not isinstance(transfer_datagram_refs, list)
            or not transfer_datagram_refs
            or request_datagram != transfer_datagram_refs[0]
        ):
            errors.append("transfer request source datagram is not the first retained transfer datagram")
        elif not _is_terminal_packet_of_datagram(request_packet, request_datagram, datagrams):
            errors.append("transfer request source packet is not the terminal packet of its request datagram")
        elif not _datagram_has_tftp_role(datagrams.get(request_datagram), request_kind):
            errors.append("transfer request source datagram does not retain its request TFTP role")
    if not isinstance(blocks, dict) or not isinstance(block_datagrams, dict):
        return
    expected_source, expected_destination = (
        (server["address"], client["address"])
        if request_kind == "RRQ"
        else (client["address"], server["address"])
    )
    for block, packet_ref in blocks.items():
        datagram_id = block_datagrams.get(block)
        block_number = _block_number(block)
        if block_number is None:
            errors.append("transfer DATA source block key is not a valid TFTP block number")
            break
        if not _witness_packet_in_datagram(packet_ref, datagram_id, datagrams):
            errors.append("transfer DATA source packet is not carried by its block datagram")
            break
        if not _datagram_has_direction(datagrams.get(datagram_id), expected_source, expected_destination):
            errors.append("transfer DATA source datagram has the wrong endpoint direction")
            break
        if (
            not isinstance(transfer_datagram_refs, list)
            or not isinstance(request_datagram, str)
            or not isinstance(datagram_id, str)
            or datagram_id not in transfer_datagram_refs
            or request_datagram not in transfer_datagram_refs
            or transfer_datagram_refs.index(datagram_id) <= transfer_datagram_refs.index(request_datagram)
        ):
            errors.append("transfer DATA source datagram does not follow its request datagram")
            break
        if not _is_terminal_packet_of_datagram(packet_ref, datagram_id, datagrams):
            errors.append("transfer DATA source packet is not the terminal packet of its block datagram")
            break
        if not _datagram_has_tftp_role(datagrams.get(datagram_id), "DATA", block_number):
            errors.append("transfer DATA source datagram does not retain its DATA block role")
            break
    if completion_packet is not None or completion_datagram is not None:
        if not _witness_packet_in_datagram(completion_packet, completion_datagram, datagrams):
            errors.append("transfer completion source packet is not carried by its completion datagram")
        elif not _datagram_has_direction(
            datagrams.get(completion_datagram), expected_source, expected_destination
        ):
            errors.append("transfer completion source datagram has the wrong endpoint direction")
        elif not _is_terminal_packet_of_datagram(completion_packet, completion_datagram, datagrams):
            errors.append("transfer completion source packet is not the terminal packet of its completion datagram")
        else:
            completion_blocks = [
                block
                for block, packet_ref in blocks.items()
                if packet_ref == completion_packet and block_datagrams.get(block) == completion_datagram
            ]
            if len(completion_blocks) != 1:
                errors.append("transfer completion source does not identify exactly one DATA block")
            else:
                block_number = _block_number(completion_blocks[0])
                if block_number is None or not _datagram_has_tftp_role(
                    datagrams.get(completion_datagram), "DATA", block_number,
                ):
                    errors.append("transfer completion source datagram does not retain its terminal DATA block role")


def _witness_packet_in_datagram(
    packet_ref: object, datagram_id: object, datagrams: dict[str, dict[str, Any]],
) -> bool:
    if not isinstance(packet_ref, str) or not isinstance(datagram_id, str):
        return False
    datagram = datagrams.get(datagram_id)
    return isinstance(datagram, dict) and packet_ref in datagram.get("packetRefIds", [])


def _datagram_has_direction(datagram: object, source: str, destination: str) -> bool:
    return (
        isinstance(datagram, dict)
        and datagram.get("source") == source
        and datagram.get("destination") == destination
    )


def _datagram_has_tftp_role(
    datagram: object, expected_kind: str, expected_block: int | None = None,
) -> bool:
    """Check the decoder summary independently retained on a datagram row."""
    if not isinstance(datagram, dict):
        return False
    summary = datagram.get("tftpMessage")
    if not isinstance(summary, dict) or summary.get("kind") != expected_kind:
        return False
    return summary.get("blockNumber") == expected_block


def _block_number(value: object) -> int | None:
    """Parse the JSON-object spelling of one legal, nonzero TFTP DATA block."""
    if not isinstance(value, str) or not value.isascii() or not value.isdigit():
        return None
    number = int(value, 10)
    return number if 1 <= number <= 65_535 and str(number) == value else None


def _is_terminal_packet_of_datagram(
    packet_ref: object, datagram_id: object, datagrams: dict[str, dict[str, Any]],
) -> bool:
    if not isinstance(packet_ref, str) or not isinstance(datagram_id, str):
        return False
    datagram = datagrams.get(datagram_id)
    refs = datagram.get("packetRefIds") if isinstance(datagram, dict) else None
    return isinstance(refs, list) and bool(refs) and refs[-1] == packet_ref


def _check_packet_capture_quality(data: dict[str, Any], errors: list[str]) -> None:
    """Cross-check packet snap-length claims against their container interface."""
    container = data.get("input", {}).get("container")
    interfaces = container.get("interfaces") if isinstance(container, dict) else None
    packets = [item for item in _objects(data.get("packetRefs")) if isinstance(item, dict)]
    if not packets:
        return
    if not isinstance(interfaces, list):
        errors.append("packetRefs require an input container interfaces array")
        return
    snap_lengths: dict[tuple[int, int], int] = {}
    for interface in interfaces:
        if not isinstance(interface, dict):
            errors.append("input container interfaces contains an invalid row")
            continue
        section_id, interface_id, snap_length = (
            interface.get("sectionId"), interface.get("interfaceId"), interface.get("snapLength"),
        )
        if (
            not isinstance(section_id, int)
            or section_id < 0
            or not isinstance(interface_id, int)
            or interface_id < 0
            or not isinstance(snap_length, int)
            or snap_length < 0
        ):
            errors.append("input container interface metadata is invalid")
            continue
        key = (section_id, interface_id)
        if key in snap_lengths:
            errors.append("input container interfaces has a repeated section/interface identity")
            continue
        snap_lengths[key] = snap_length
    for packet in packets:
        section_id, interface_id = packet.get("sectionId"), packet.get("interfaceId")
        if not isinstance(section_id, int) or not isinstance(interface_id, int):
            errors.append("packetRef has an invalid section/interface identity")
            continue
        interface_key = (section_id, interface_id)
        if interface_key not in snap_lengths:
            errors.append("packetRef does not resolve to an input container interface")
            continue
        expected_snap = snap_lengths[interface_key]
        actual_snap = packet.get("captureSnapLength")
        if not isinstance(actual_snap, int) or actual_snap < 0 or actual_snap != expected_snap:
            errors.append("packetRef captureSnapLength differs from its input container interface")
            continue
        caplen = packet.get("capturedLength")
        quality = packet.get("qualityCodes")
        exceeds = isinstance(caplen, int) and isinstance(actual_snap, int) and actual_snap > 0 and caplen > actual_snap
        has_code = isinstance(quality, list) and "CAPLEN-EXCEEDS-SNAPLEN" in quality
        if exceeds != has_code:
            errors.append("packetRef CAPLEN-EXCEEDS-SNAPLEN quality code disagrees with capture lengths")


def _check_file_length_quality(data: dict[str, Any], errors: list[str]) -> None:
    """Keep bounded file-header parse claims tied to the transfer payload size."""
    transfers = {
        item.get("transferId"): item
        for item in _objects(data.get("transfers"))
        if isinstance(item, dict) and isinstance(item.get("transferId"), str)
    }
    headers: dict[str, list[dict[str, Any]]] = {}
    applications: dict[str, list[dict[str, Any]]] = {}
    container = data.get("input", {}).get("container")
    event_retention_truncated = any(
        isinstance(item, dict) and item.get("code") == "RESOURCE-EVENT-LIMIT"
        for item in _objects(data.get("diagnostics"))
    ) or (
        isinstance(container, dict)
        and container.get("scanStatus") == "STOPPED-RESOURCE-LIMIT"
    )
    for event in _objects(data.get("events")):
        if not isinstance(event, dict) or not isinstance(event.get("transferId"), str):
            continue
        if event.get("eventType") == "FIRST-SLICE-FILE-HEADER":
            headers.setdefault(event["transferId"], []).append(event)
        if event.get("layer") == "APPLICATION":
            applications.setdefault(event["transferId"], []).append(event)
    for transfer_id, transfer in transfers.items():
        if (
            transfer.get("reconstructionStatus") != "COMPLETE"
            or transfer.get("mode") != "octet"
            or infer_file_role(transfer.get("filename")) is None
        ):
            continue
        matching_headers = headers.get(transfer_id, [])
        if len(matching_headers) != 1:
            if not event_retention_truncated:
                errors.append("complete supported transfer must retain exactly one first-slice header parse witness")
            continue
        header = matching_headers[0]
        fields = header.get("fields")
        decoded = fields.get("decodedFields") if isinstance(fields, dict) else None
        if not isinstance(fields, dict) or not isinstance(decoded, dict):
            errors.append("first-slice header parse witness lacks decoded field evidence")
            continue
        observed = decoded.get("observedFileLength")
        if not isinstance(observed, int) or observed != transfer.get("completePayloadLength"):
            errors.append("file-header observedFileLength differs from its complete transfer payload length")
            continue
        parse_status = fields.get("parseStatus")
        declared = decoded.get("declaredFileLength")
        related_applications = applications.get(transfer_id, [])
        if parse_status == "PARSED":
            if not isinstance(declared, int) or declared != observed:
                errors.append("parsed first-slice header does not retain a matching declared/observed file length")
            if (
                not event_retention_truncated
                and (
                    len(related_applications) != 1
                    or related_applications[0].get("fields", {}).get("headerEventId") != header.get("eventId")
                )
            ):
                errors.append("parsed first-slice header must retain exactly one linked APPLICATION event")
        else:
            if related_applications:
                errors.append("non-parsed first-slice header must not publish an APPLICATION event")
            if fields.get("reason") == "DECLARED-FILE-LENGTH-MISMATCH":
                if not isinstance(declared, int) or declared == observed or parse_status != "MALFORMED":
                    errors.append("declared/observed file-length mismatch is not retained as a controlled malformed parse")


def _objects(value: object) -> list[object]:
    return value if isinstance(value, list) else []


def _rendered_strings(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "\n".join(_rendered_strings(item) for item in value.values())
    if isinstance(value, list):
        return "\n".join(_rendered_strings(item) for item in value)
    return ""


def _find_forbidden_keys(value: object, forbidden: set[str]) -> list[str]:
    if isinstance(value, dict):
        result = [key for key in value if key in forbidden]
        for child in value.values():
            result.extend(_find_forbidden_keys(child, forbidden))
        return result
    if isinstance(value, list):
        result: list[str] = []
        for child in value:
            result.extend(_find_forbidden_keys(child, forbidden))
        return result
    return []
