"""Run the frozen SIMULATED-IUT confirmatory grid.  Does not edit configs."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Mapping

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from a615a_sim.algorithm.hypothesis_model import map_to_parent_hypotheses  # noqa: E402
from a615a_sim.evaluator import issue_truth_capability, new_independent_truth_store  # noqa: E402
from a615a_sim.evaluator.guard import deny_algorithm_truth_access  # noqa: E402
from a615a_sim.evaluator.pipeline import orchestrator as orchestrator_mod  # noqa: E402
from a615a_sim.evaluator.pipeline.orchestrator import execute_live_attempt  # noqa: E402
from a615a_sim.faults.injector import inject, overlay_declared_fault  # noqa: E402

REGISTRATION_PATH = ROOT / "configs/research/cltav_confirmatory_registration_v1.json"
DESIGN_PATH = ROOT / "configs/research/cltav_confirmatory_design_draft_v1.json"
OUT_DIR = ROOT / "artifacts" / "confirmatory"
RAW_PATH = OUT_DIR / "cltav_confirmatory_attempts_v1.jsonl"
LABEL = "CONFIRMATORY / SIMULATED-IUT"
NORMAL_TRUTH = frozenset({"h_normal", "h-normal"})


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_head(cwd: Path = ROOT) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=cwd, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def git_porcelain(cwd: Path = ROOT) -> str:
    return subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=cwd, text=True
    )


def load_registration(path: Path = REGISTRATION_PATH) -> dict[str, Any]:
    return load_json(path)


def load_design(path: Path = DESIGN_PATH) -> dict[str, Any]:
    return load_json(path)


def design_cells(design: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [dict(cell) for cell in design["cells"]]


def planned_cell_count(design: Mapping[str, Any] | None = None) -> int:
    payload = design if design is not None else load_design()
    return len(design_cells(payload))


def preflight_errors(
    *,
    registration: Mapping[str, Any] | None = None,
    design: Mapping[str, Any] | None = None,
    registration_path: Path | None = None,
    design_path: Path | None = None,
    root: Path | None = None,
    raw_path: Path | None = None,
    porcelain: str | None = None,
) -> list[str]:
    errors: list[str] = []
    root = ROOT if root is None else root
    registration_path = REGISTRATION_PATH if registration_path is None else registration_path
    design_path = DESIGN_PATH if design_path is None else design_path
    raw_path = RAW_PATH if raw_path is None else raw_path
    if porcelain is None:
        porcelain = git_porcelain(root)
    if porcelain.strip():
        errors.append("git worktree is not clean")
    payload = dict(registration) if registration is not None else load_registration(registration_path)
    design_payload = dict(design) if design is not None else load_design(design_path)
    expected_hashes = payload.get("configHashes") or {}
    for relative in payload.get("hashedFiles") or []:
        path = root / str(relative)
        digest = sha256_file(path)
        want = expected_hashes.get(str(relative))
        if digest != want:
            errors.append(f"hash mismatch for {relative}")
    cells = design_cells(design_payload)
    want_count = int((payload.get("cells") or {}).get("cellCount") or 0)
    if len(cells) != want_count:
        errors.append(f"cell count {len(cells)} != registration {want_count}")
    want_arms = list((payload.get("cells") or {}).get("arms") or [])
    have_arms = list(design_payload.get("arms") or [])
    if have_arms != want_arms:
        errors.append("arms do not match registration")
    if raw_path.exists():
        errors.append(f"{raw_path.name} already exists")
    return errors


def run_preflight(**kwargs: Any) -> None:
    errors = preflight_errors(**kwargs)
    if errors:
        for item in errors:
            print(item, file=sys.stderr)
        raise SystemExit(2)


@contextmanager
def apply_unit_parameter_vector(parameters: Mapping[str, Any] | None) -> Iterator[None]:
    """Install the unit parameter vector on inject and overlay (S1 interval visibility)."""

    params = dict(parameters or {})

    def run_inject(target, *, scene_id, fault_id, attempt_id=None, confirm=True):
        deny_algorithm_truth_access(operation="e1-inject")
        return inject(
            target,
            scene_id=scene_id,
            fault_id=fault_id,
            attempt_id=attempt_id,
            confirm=confirm,
            truth_store=None,
            truth_capability=None,
            parameters=params,
        )

    def overlay(target, **kwargs):
        kwargs = dict(kwargs)
        kwargs["parameters"] = params
        return overlay_declared_fault(target, **kwargs)

    original_run_inject = orchestrator_mod.run_inject
    original_overlay = orchestrator_mod.overlay_declared_fault
    orchestrator_mod.run_inject = run_inject
    orchestrator_mod.overlay_declared_fault = overlay
    try:
        yield
    finally:
        orchestrator_mod.run_inject = original_run_inject
        orchestrator_mod.overlay_declared_fault = original_overlay


def _truth_parent(row: Mapping[str, Any] | None) -> str | None:
    if not row:
        return None
    raw = (row.get("truthReference") or {}).get("truthHypothesis")
    if raw is None:
        return None
    mapped = map_to_parent_hypotheses([str(raw)])
    return mapped[0] if mapped else str(raw)


def _candidate_set(live: Mapping[str, Any], row: Mapping[str, Any] | None) -> list[str]:
    hypotheses = list((live.get("runRecord") or {}).get("finalHypotheses") or [])
    if not hypotheses and row is not None:
        hypotheses = list(row.get("finalHypotheses") or [])
    return list(map_to_parent_hypotheses(hypotheses))


def _rounds_consumed(live: Mapping[str, Any], remaining: int) -> int | None:
    run = live.get("runRecord") or {}
    leftover = (run.get("traceRef") or {}).get("resourceRemaining")
    if leftover is None:
        return None
    return int(remaining) - int(leftover)


def _ok_record(
    *,
    cell: Mapping[str, Any],
    live: Mapping[str, Any],
    git_sha: str | None,
    config_hashes: Mapping[str, str],
    remaining: int,
) -> dict[str, Any]:
    row = live.get("attemptRow")
    return {
        "label": LABEL,
        "cellId": cell["cellId"],
        "unitId": cell["unitId"],
        "arm": cell.get("armId") or cell.get("arm"),
        "truthParentHypothesis": _truth_parent(row),
        "verdict": None if row is None else row.get("outcome"),
        "finalCandidateSet": _candidate_set(live, row),
        "stopClass": (live.get("runRecord") or {}).get("stopClass")
        if live.get("runRecord")
        else (None if row is None else row.get("stopClass")),
        "roundsConsumed": _rounds_consumed(live, remaining),
        "status": "OK",
        "gitHead": git_sha,
        "configHashes": dict(config_hashes),
    }


def _missing_record(
    *,
    cell: Mapping[str, Any],
    git_sha: str | None,
    config_hashes: Mapping[str, str],
    detail: str,
) -> dict[str, Any]:
    return {
        "label": LABEL,
        "cellId": cell["cellId"],
        "unitId": cell["unitId"],
        "arm": cell.get("armId") or cell.get("arm"),
        "truthParentHypothesis": None,
        "verdict": None,
        "finalCandidateSet": [],
        "stopClass": None,
        "roundsConsumed": None,
        "status": "MISSING",
        "gitHead": git_sha,
        "configHashes": dict(config_hashes),
        "infrastructureDetail": detail,
    }


def _undefined_record(
    *,
    cell: Mapping[str, Any],
    live: Mapping[str, Any],
    git_sha: str | None,
    config_hashes: Mapping[str, str],
    remaining: int,
) -> dict[str, Any]:
    row = live.get("attemptRow")
    run = live.get("runRecord") or {}
    return {
        "label": LABEL,
        "cellId": cell["cellId"],
        "unitId": cell["unitId"],
        "arm": cell.get("armId") or cell.get("arm"),
        "truthParentHypothesis": _truth_parent(row),
        "verdict": None,
        "finalCandidateSet": _candidate_set(live, row),
        "stopClass": run.get("stopClass"),
        "roundsConsumed": _rounds_consumed(live, remaining),
        "status": "UNDEFINED-OUTCOME",
        "undefinedDetectionOutcome": str(live.get("undefinedDetectionOutcome")),
        "gitHead": git_sha,
        "configHashes": dict(config_hashes),
    }


def _record_from_live(
    *,
    cell: Mapping[str, Any],
    live: Mapping[str, Any],
    git_sha: str | None,
    config_hashes: Mapping[str, str],
    remaining: int,
) -> dict[str, Any]:
    if live.get("attemptRow") is None and live.get("undefinedDetectionOutcome"):
        return _undefined_record(
            cell=cell,
            live=live,
            git_sha=git_sha,
            config_hashes=config_hashes,
            remaining=remaining,
        )
    return _ok_record(
        cell=cell,
        live=live,
        git_sha=git_sha,
        config_hashes=config_hashes,
        remaining=remaining,
    )


def execute_one_cell(
    cell: Mapping[str, Any],
    *,
    remaining: int,
    git_sha: str | None,
    config_hashes: Mapping[str, str],
) -> dict[str, Any]:
    parameters = dict(cell.get("parameters") or {})
    attempt_id = f"A-{cell['cellId']}"
    pairing_id = f"PAIR-{cell['cellId']}"

    def once() -> dict[str, Any]:
        store = new_independent_truth_store()
        capability = issue_truth_capability()
        with apply_unit_parameter_vector(parameters):
            return execute_live_attempt(
                scene_id=cell["sceneId"],
                fault_id=cell["faultId"],
                arm_id=str(cell.get("armId") or cell.get("arm")),
                resource_mode="ROUNDS",
                remaining=int(remaining),
                capability=capability,
                store=store,
                confirm=True,
                pairing_id=pairing_id,
                attempt_id=attempt_id,
            )

    try:
        live = once()
    except Exception as exc:
        try:
            live = once()
        except Exception as retry_exc:
            return _missing_record(
                cell=cell,
                git_sha=git_sha,
                config_hashes=config_hashes,
                detail=f"{type(exc).__name__}: {exc}; retry {type(retry_exc).__name__}: {retry_exc}",
            )
    return _record_from_live(
        cell=cell,
        live=live,
        git_sha=git_sha,
        config_hashes=config_hashes,
        remaining=remaining,
    )


def run_cells(
    *,
    design: Mapping[str, Any],
    registration: Mapping[str, Any],
    raw_path: Path = RAW_PATH,
) -> list[dict[str, Any]]:
    remaining = int((design.get("resourceMode") or {}).get("remainingPerCell") or 8)
    git_sha = git_head()
    config_hashes = dict(registration.get("configHashes") or {})
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    if raw_path.exists():
        raise SystemExit(2)
    written: list[dict[str, Any]] = []
    with raw_path.open("w", encoding="utf-8") as handle:
        for cell in design_cells(design):
            record = execute_one_cell(
                cell,
                remaining=remaining,
                git_sha=git_sha,
                config_hashes=config_hashes,
            )
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            written.append(record)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Confirmatory runner (no interim look).")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Pre-flight only; print planned cell count; execute nothing.",
    )
    args = parser.parse_args(argv)
    registration = load_registration()
    design = load_design()
    run_preflight(registration=registration, design=design)
    planned = planned_cell_count(design)
    if args.dry_run:
        print(json.dumps({"dryRun": True, "plannedCells": planned, "executed": 0}))
        return 0
    rows = run_cells(design=design, registration=registration)
    print(json.dumps({"dryRun": False, "plannedCells": planned, "written": len(rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
