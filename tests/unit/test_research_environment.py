from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_research_environment import (  # noqa: E402
    _ledger_link_errors,
    duplicate_values,
    validate_environment,
)


def test_repository_research_environment_is_valid() -> None:
    assert validate_environment(ROOT) == []


def test_duplicate_values_ignores_empty_ids_and_reports_duplicates() -> None:
    rows = [
        {"search_id": "SEARCH-001"},
        {"search_id": ""},
        {"search_id": "SEARCH-001"},
        {"search_id": "SEARCH-002"},
    ]
    assert duplicate_values(rows, "search_id") == ["SEARCH-001"]


def test_literature_ledgers_are_referentially_consistent() -> None:
    registries = {
        "screeningLedger": "configs/research/literature/screening_ledger.csv",
        "evidenceLedger": "configs/research/literature/evidence_ledger.csv",
        "claimCitationLedger": "configs/research/literature/claim_citation_ledger.csv",
    }
    assert _ledger_link_errors(ROOT, registries) == []
