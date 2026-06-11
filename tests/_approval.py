"""Golden Master (Approval Test) helpers."""

from __future__ import annotations

import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def golden_path(golden_id: str) -> Path:
    return GOLDEN_DIR / f"{golden_id}.approved.txt"


def assert_matches_golden(actual: str, golden_id: str) -> None:
    """Compare actual text to golden file. Set UPDATE_GOLDEN=1 to refresh baseline."""
    path = golden_path(golden_id)
    normalized = actual.rstrip() + "\n"

    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized, encoding="utf-8")
        return

    if not path.is_file():
        raise AssertionError(f"golden missing: {path} (run UPDATE_GOLDEN=1 pytest …)")

    expected = path.read_text(encoding="utf-8")
    if normalized != expected:
        raise AssertionError(
            f"golden mismatch: {path}\n--- expected ---\n{expected}--- actual ---\n{normalized}"
        )
