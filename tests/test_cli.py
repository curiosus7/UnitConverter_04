"""Track A (Boundary) — CLI input/output tests (TD-01, TD-04)."""

import subprocess
import sys

E_FMT = "Invalid format. Use unit:value (ex: meter:2.5)"
E_NEG = "Negative value not allowed"


def _run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "unit_converter", *args],
        capture_output=True,
        text=True,
    )


def _combined_output(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


def test_u_in_01_reject_empty_input():
    """U-IN-01 | FR-05 | '' → E-FMT"""
    result = _run_cli("")
    assert E_FMT in _combined_output(result)


def test_u_in_02_reject_missing_colon():
    """U-IN-02 | FR-05 | meter → E-FMT"""
    result = _run_cli("meter")
    assert E_FMT in _combined_output(result)


def test_u_in_03_reject_negative_value():
    """U-IN-03 | FR-04 | meter:-1 → E-NEG"""
    result = _run_cli("meter:-1")
    assert E_NEG in _combined_output(result)


def test_u_in_04_reject_non_unit_value_format():
    """U-IN-04 | FR-05 | abc → E-FMT"""
    result = _run_cli("abc")
    assert E_FMT in _combined_output(result)
