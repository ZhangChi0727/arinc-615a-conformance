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


def _normal_aliases() -> tuple[str, ...]:
    normal = load_catalogue()["normal"]
    return (str(normal["id"]), str(normal["hypothesisId"]))


def entry_by_id(fault_id: str) -> Mapping[str, Any]:
    catalogue = load_catalogue()
    if fault_id in _normal_aliases():
        return catalogue["normal"]
    for group in ("hSingle", "evaluatorConstructionsNotInHSingle"):
        for entry in catalogue[group]:
            if entry["id"] == fault_id or entry.get("hypothesisId") == fault_id:
                return entry
    raise KeyError(fault_id)


def canonical_fault_id(fault_id: str) -> str:
    return str(entry_by_id(fault_id)["id"])


def declared_signature(fault_id: str) -> str:
    return str(entry_by_id(fault_id)["observableSignature"])


def applicable_scenes(fault_id: str) -> frozenset[str]:
    scenes = entry_by_id(fault_id).get("applicableScenes") or []
    return frozenset(str(scene) for scene in scenes)


def is_applicable(scene_id: str, fault_id: str) -> bool:
    return scene_id in applicable_scenes(fault_id)


def locate_scenes() -> frozenset[str]:
    return frozenset(str(scene) for scene in load_catalogue()["locateScenes"])


def in_domain_hypotheses_for_scene(scene_id: str) -> tuple[str, ...]:
    """h_normal plus applicable H_single ids (evaluator constructions excluded)."""

    ids = ["H-NORMAL"]
    for entry in h_single_entries():
        if scene_id in (entry.get("applicableScenes") or []):
            ids.append(str(entry["id"]))
    return tuple(ids)


def evaluator_fault_plan() -> tuple[tuple[str, str], ...]:
    """Evaluator-only (sceneId, faultId|h_normal) rows.  Not an injector schedule."""

    catalogue = load_catalogue()
    rows: list[tuple[str, str]] = []
    scenes = set(catalogue["locateScenes"]) | set(catalogue["detectAblationOnlyScenes"])
    for scene in sorted(scenes):
        for fault_id in in_domain_hypotheses_for_scene(scene):
            rows.append((scene, fault_id))
        for entry in catalogue["evaluatorConstructionsNotInHSingle"]:
            if scene in (entry.get("applicableScenes") or []):
                rows.append((scene, str(entry["id"])))
    return tuple(rows)


def parameter_axes() -> tuple[Mapping[str, Any], ...]:
    axes = load_catalogue().get("parameterAxes") or []
    return tuple(axes)


def harder_cases() -> tuple[Mapping[str, Any], ...]:
    cases = load_catalogue().get("harderCases") or []
    return tuple(cases)


def require_applicable(scene_id: str, fault_id: str) -> Mapping[str, Any]:
    entry = entry_by_id(fault_id)
    if not is_applicable(scene_id, fault_id):
        raise ValueError(f"inapplicable (sceneId, faultId): {scene_id}, {canonical_fault_id(fault_id)}")
    return entry
