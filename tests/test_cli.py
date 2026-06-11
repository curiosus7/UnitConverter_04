"""Track A (Boundary) — CLI input/output tests (TD-01, TD-04, TD-09)."""

import json
import subprocess
import sys

E_FMT = "Invalid format. Use unit:value (ex: meter:2.5)"
E_NEG = "Negative value not allowed"

GOLDEN_METER_25_STDOUT = (
    "2.5 meter = 2.5000 meter\n"
    "2.5 meter = 8.2021 feet\n"
    "2.5 meter = 2.7340 yard\n"
)


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


# --- REFACTOR: Golden Master (behavior lock before SRP split) ---


def test_golden_master_meter_25_stdout():
    """Golden Master | meter:2.5 → 전체 stdout 스냅샷"""
    result = _run_cli("meter:2.5")
    assert result.stdout == GOLDEN_METER_25_STDOUT
    assert result.returncode == 0


def test_golden_master_negative_value_stdout():
    """Golden Master | meter:-1 → E-NEG 정확 출력"""
    result = _run_cli("meter:-1")
    assert result.stdout == f"{E_NEG}\n"


# --- TD-04: CLI output contract (FR-02) ---


def test_u_out_01_meter_conversion_multi_line_output():
    """U-OUT-01 | FR-02 | meter:2.5 → 3줄 이상, 소수 4자리 환산"""
    result = _run_cli("meter:2.5")
    output = result.stdout

    lines = [line for line in output.strip().splitlines() if line.strip()]
    assert len(lines) >= 3
    assert "8.2021" in output
    assert "2.7340" in output
    assert "2.5000" in output


# --- TD-09: output format (EXT-03) ---


def test_u_fmt_01_json_output():
    """U-FMT-01 | EXT-03 | --format json → 유효 JSON"""
    result = _run_cli("meter:2.5", "--format", "json")
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["input"]["unit"] == "meter"
    assert data["input"]["value"] == 2.5
    assert data["results"]["feet"] == 8.2021


def test_u_fmt_02_csv_output():
    """U-FMT-02 | EXT-03 | --format csv → CSV 헤더·행"""
    result = _run_cli("meter:2.5", "--format", "csv")
    assert result.returncode == 0
    lines = result.stdout.strip().splitlines()
    assert lines[0] == "unit,value"
    assert any("feet,8.2021" in line for line in lines)


def test_u_fmt_03_table_output():
    """U-FMT-03 | EXT-03 | --format table → 줄 단위 출력"""
    result = _run_cli("meter:2.5", "--format", "table")
    assert result.returncode == 0
    assert result.stdout == GOLDEN_METER_25_STDOUT
