"""Validated access to the accepted development-contract snapshot."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from .controlled_resources import ControlledResourceError, controlled_resource_json, controlled_resource_sha256
from .identity import DEVELOPMENT_CONTRACT_SHA256
from .record_contract import validate_record_instance


@lru_cache(maxsize=1)
def development_contract_snapshot() -> dict[str, Any]:
    """Load and validate the exact, accepted contract snapshot for this adapter."""
    actual_sha256 = controlled_resource_sha256("development-contract")
    if actual_sha256 != DEVELOPMENT_CONTRACT_SHA256:
        raise ControlledResourceError(
            "DEVELOPMENT-CONTRACT-IDENTITY-MISMATCH",
            "controlled development-contract resource does not match the accepted snapshot identity",
        )
    contract = controlled_resource_json("development-contract")
    schema = controlled_resource_json("development-contract-schema")
    try:
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(contract), key=lambda error: list(error.absolute_path))
    except SchemaError as exc:
        raise ControlledResourceError(
            "DEVELOPMENT-CONTRACT-SCHEMA-INVALID", "controlled development-contract schema is invalid"
        ) from exc
    if errors:
        raise ControlledResourceError(
            "DEVELOPMENT-CONTRACT-INVALID",
            "controlled development-contract snapshot violates its schema: " + errors[0].message,
        )
    records = contract.get("recordContracts")
    if not isinstance(records, list) or not all(isinstance(record, dict) for record in records):
        raise ControlledResourceError(
            "DEVELOPMENT-CONTRACT-INVALID", "controlled development-contract lacks typed record contracts"
        )
    identifiers = [record.get("id") for record in records]
    if len(identifiers) != len(set(identifiers)) or not all(isinstance(item, str) and item for item in identifiers):
        raise ControlledResourceError(
            "DEVELOPMENT-CONTRACT-INVALID", "controlled development-contract has non-unique record identifiers"
        )
    return contract


def accepted_record_contracts() -> dict[str, dict[str, Any]]:
    snapshot = development_contract_snapshot()
    return {record["id"]: record for record in snapshot["recordContracts"]}


def record_instance_errors(record_type: str, payload: object) -> list[tuple[str, tuple[object, ...], str]]:
    """Validate an instance using the same public controlled record rules."""
    record = accepted_record_contracts().get(record_type)
    if record is None:
        return [("RC-RECORD-TYPE", (), f"unknown controlled record type {record_type!r}")]
    return validate_record_instance(record, payload)

