"""F-A: the status surface derives the current CRS inventory from the package.

The governed README block must not carry a second hand-filled coverage or
requirement count. It is generated from the controlled CRS package declared in
the source register, and the derived value is checked against the package
``inventorySummary``. All tests exercise the production generator path.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sync = _load("sync_project_overview", ROOT / "scripts/sync_project_overview.py")
baseline = _load("check_repo_baseline", ROOT / "scripts/check_repo_baseline.py")

CRS_RELATIVE = "configs/requirements/arinc_615a3_m1_crs.json"
HAND_COUNT_RE = re.compile(r"\d+\s*coverage\s*/\s*\d+\s*requirements", re.IGNORECASE)


def _package() -> dict:
    return json.loads((ROOT / CRS_RELATIVE).read_text(encoding="utf-8"))


def _sources() -> dict:
    return copy.deepcopy(baseline.CONTROLLED_SOURCES)


def _fixture_root(tmp_path: Path, package: dict) -> dict:
    """Write *package* under a repository-shaped temp root and point the register at it."""
    target = tmp_path / CRS_RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(package), encoding="utf-8")
    sources = _sources()
    sources["requirementsControl"]["packagePath"] = CRS_RELATIVE
    return sources


def test_derived_inventory_matches_the_authoritative_package() -> None:
    inventory = sync.crs_inventory(baseline.CONTROLLED_SOURCES)
    package = _package()
    assert inventory["coverage"] == len(package["coverageLedger"])
    assert inventory["requirements"] == len(package["requirements"])
    assert inventory["coverage"] == package["inventorySummary"]["coverageCount"]
    assert inventory["requirements"] == package["inventorySummary"]["requirementCount"]
    assert inventory["artifactId"] == package["artifactId"]
    assert inventory["artifactVersion"] == package["artifactVersion"]


def test_status_narrative_no_longer_carries_a_hand_filled_count() -> None:
    increment = baseline.STATUS["currentIncrement"]
    for field in ("summary", "summaryZh", "stateChanges", "stateChangesZh"):
        joined = " ".join(increment[field])
        assert not HAND_COUNT_RE.search(joined), field


def test_rendered_readme_carries_the_derived_inventory_in_both_languages() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    inventory = sync.crs_inventory(baseline.CONTROLLED_SOURCES)
    row_en = (
        f"| Current CRS inventory | `{inventory['artifactId']}` / "
        f"`{inventory['artifactVersion']}` / coverage {inventory['coverage']} / "
        f"requirements {inventory['requirements']} |"
    )
    row_zh = (
        f"| 当前 CRS 清单 | `{inventory['artifactId']}` / "
        f"`{inventory['artifactVersion']}` / coverage {inventory['coverage']} / "
        f"requirements {inventory['requirements']} |"
    )
    assert row_en in readme
    assert row_zh in readme


def test_adding_one_package_row_changes_both_languages_without_code_change(tmp_path: Path) -> None:
    package = _package()
    package["coverageLedger"].append(copy.deepcopy(package["coverageLedger"][-1]))
    package["requirements"].append(copy.deepcopy(package["requirements"][-1]))
    package["inventorySummary"]["coverageCount"] = len(package["coverageLedger"])
    package["inventorySummary"]["requirementCount"] = len(package["requirements"])
    sources = _fixture_root(tmp_path, package)
    inventory = sync.crs_inventory(sources, root=tmp_path)
    assert inventory["coverage"] == len(package["coverageLedger"])
    rendered = sync.render_status_block(baseline.STATUS, sources, root=tmp_path)
    expected = f"coverage {inventory['coverage']} / requirements {inventory['requirements']}"
    assert expected in rendered
    assert rendered.count(expected) >= 2


def test_removing_one_package_row_changes_both_languages_without_code_change(tmp_path: Path) -> None:
    package = _package()
    package["coverageLedger"].pop()
    package["requirements"].pop()
    package["inventorySummary"]["coverageCount"] = len(package["coverageLedger"])
    package["inventorySummary"]["requirementCount"] = len(package["requirements"])
    sources = _fixture_root(tmp_path, package)
    inventory = sync.crs_inventory(sources, root=tmp_path)
    rendered = sync.render_status_block(baseline.STATUS, sources, root=tmp_path)
    expected = f"coverage {inventory['coverage']} / requirements {inventory['requirements']}"
    assert rendered.count(expected) >= 2


def test_stale_hand_count_in_readme_fails_the_check() -> None:
    data = baseline.STATUS
    sources = baseline.CONTROLLED_SOURCES
    current = (ROOT / "README.md").read_text(encoding="utf-8")
    stale = re.sub(
        r"coverage \d+ / requirements \d+",
        "coverage 3152 / requirements 862",
        current,
        count=1,
    )
    assert stale != current
    # The generator overrides a hand-edited count; --check therefore reports drift.
    errors = baseline.governed_status_errors(data, stale, sources)
    assert any("README governed block differs" in error for error in errors)


def test_inventory_summary_disagreement_fails_closed(tmp_path: Path) -> None:
    package = _package()
    package["inventorySummary"]["coverageCount"] = len(package["coverageLedger"]) + 1
    sources = _fixture_root(tmp_path, package)
    with pytest.raises(sync.StatusError):
        sync.crs_inventory(sources, root=tmp_path)


def test_missing_package_file_fails_closed(tmp_path: Path) -> None:
    sources = _sources()
    sources["requirementsControl"]["packagePath"] = CRS_RELATIVE
    with pytest.raises(sync.StatusError):
        sync.crs_inventory(sources, root=tmp_path)


def test_unsafe_package_path_fails_closed(tmp_path: Path) -> None:
    windows_absolute = "C" + ":" + "/" + "Windows/system32/cmd.exe"
    for invalid in ("/etc/passwd", "../../README.md", windows_absolute):
        sources = _sources()
        sources["requirementsControl"]["packagePath"] = invalid
        with pytest.raises(sync.StatusError):
            sync.crs_inventory(sources, root=tmp_path)


def test_invalid_package_shape_fails_closed(tmp_path: Path) -> None:
    package = _package()
    package.pop("coverageLedger", None)
    sources = _fixture_root(tmp_path, package)
    with pytest.raises(sync.StatusError):
        sync.crs_inventory(sources, root=tmp_path)
    package = _package()
    package["inventorySummary"] = []
    sources = _fixture_root(tmp_path, package)
    with pytest.raises(sync.StatusError):
        sync.crs_inventory(sources, root=tmp_path)


def test_missing_requirements_control_fails_closed() -> None:
    sources = _sources()
    del sources["requirementsControl"]
    with pytest.raises(sync.StatusError):
        sync.crs_inventory(sources)
