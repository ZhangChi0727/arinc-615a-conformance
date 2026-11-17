"""Declared single-fault catalogue H_single for the simulated IUT."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files
from typing import Any, Mapping


@lru_cache(maxsize=1)
def load_catalogue() -> Mapping[str, Any]:
    payload = files("a615a_sim.resources").joinpath("fault_catalogue.json").read_text(encoding="utf-8")
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("fault catalogue must be an object")
    return data


def h_single_entries() -> tuple[Mapping[str, Any], ...]:
    entries = load_catalogue()["hSingle"]
    return tuple(entries)


def entry_by_id(fault_id: str) -> Mapping[str, Any]:
    catalogue = load_catalogue()
    if catalogue["normal"]["id"] == fault_id:
        return catalogue["normal"]
    for group in ("hSingle", "evaluatorConstructionsNotInHSingle"):
        for entry in catalogue[group]:
            if entry["id"] == fault_id:
                return entry
    raise KeyError(fault_id)


def declared_signature(fault_id: str) -> str:
    return str(entry_by_id(fault_id)["observableSignature"])
