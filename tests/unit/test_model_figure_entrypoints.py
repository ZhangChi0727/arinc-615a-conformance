from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_research_environment_runs_shared_model_validator() -> None:
    module = load("scripts/check_research_environment.py", "research_environment_for_model_figures")
    assert not [item for item in module.validate_environment(ROOT) if item.startswith("model figure:")]


def test_repository_baseline_runs_shared_model_validator() -> None:
    module = load("scripts/check_repo_baseline.py", "baseline_for_model_figures")
    assert not [item for item in module.cltav_figure_errors() if item.startswith("model redraw:")]


def test_model_validator_is_referenced_by_both_entrypoints() -> None:
    for relative in ("scripts/check_research_environment.py", "scripts/check_repo_baseline.py"):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "cltav-model-figures/scripts/model_drawio.py" in text
        assert "validate_package" in text
