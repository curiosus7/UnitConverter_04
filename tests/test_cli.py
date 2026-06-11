"""Track A (Boundary) — CLI input/output tests (TD-01, TD-04, TD-09)."""

import json
import subprocess
import sys

from tests._approval import assert_matches_golden

E_FMT = "Invalid format. Use unit:value (ex: meter:2.5)"
E_NEG = "Negative value not allowed"
E_UNIT = "Unknown unit: cubit"
E_REG = "Invalid register format. Use: 1 cubit = 0.4572 meter"
E_FMT_OPT = "Invalid format option. Use: csv, json, table"

GM_METER_25 = "GM-METER-25"
GM_METER_NEG = "GM-METER-NEG"
GM_FMT_TABLE = "GM-FMT-TABLE"
GM_FMT_JSON = "GM-FMT-JSON"
GM_FMT_CSV = "GM-FMT-CSV"
GM_FEET_10 = "GM-FEET-10"
GM_REG_CUBIT_1 = "GM-REG-CUBIT-1"
GM_REG_CUBIT_2 = "GM-REG-CUBIT-2"
GM_FMT_OPT_ERR = "GM-FMT-OPT-ERR"
GM_REG_ERR = "GM-REG-ERR"
GM_UNIT_CUBIT_ERR = "GM-UNIT-CUBIT-ERR"


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


# --- REFACTOR: Golden Master (Approval Test — tests/golden/*.approved.txt) ---


def test_golden_master_meter_25_stdout():
    """Golden Master | GM-METER-25 | meter:2.5 → 전체 stdout 스냅샷"""
    result = _run_cli("meter:2.5")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_METER_25)


def test_golden_master_negative_value_stdout():
    """Golden Master | GM-METER-NEG | meter:-1 → E-NEG 정확 출력"""
    result = _run_cli("meter:-1")
    assert_matches_golden(result.stdout, GM_METER_NEG)


# --- TD-04: CLI output contract (FR-02) ---


def test_u_out_01_meter_conversion_multi_line_output():
    """U-OUT-01 | FR-02 | meter:2.5 → box table, 소수 4자리 환산"""
    result = _run_cli("meter:2.5")
    output = result.stdout

    assert "┌" in output
    assert "unit" in output and "input" in output and "result" in output
    assert "8.2021" in output
    assert "2.7340" in output
    assert "2.5" in output


# --- TD-09: output format (EXT-03) ---


def test_u_fmt_01_json_output():
    """U-FMT-01 | EXT-03 | --format json → Golden Master JSON"""
    result = _run_cli("meter:2.5", "--format", "json")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_FMT_JSON)
    data = json.loads(result.stdout)
    assert data["input"]["unit"] == "meter"


def test_u_fmt_02_csv_output():
    """U-FMT-02 | EXT-03 | --format csv → Golden Master CSV"""
    result = _run_cli("meter:2.5", "--format", "csv")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_FMT_CSV)


def test_u_fmt_03_table_output():
    """U-FMT-03 | EXT-03 | --format table → Golden Master table"""
    result = _run_cli("meter:2.5", "--format", "table")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_FMT_TABLE)


def test_u_fmt_04_default_format_omitted():
    """U-FMT-04 | EXT-03 | --format 생략 → table 기본 (Golden Master)"""
    result = _run_cli("meter:2.5")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_METER_25)


def test_u_fmt_05_reject_invalid_format_option():
    """U-FMT-05 | EXT-03 | --format xml → Golden Master 포맷 오류"""
    result = _run_cli("meter:2.5", "--format", "xml")
    assert_matches_golden(_combined_output(result), GM_FMT_OPT_ERR)


def test_u_fmt_06_format_flag_without_value_uses_default():
    """U-FMT-06 | EXT-03 | --format 값 없음(맨 끝) → table 기본 유지"""
    result = _run_cli("meter:2.5", "--format")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_METER_25)


# --- TD-07: units file CLI boundary (EXT-01) ---


def test_u_cfg_01_cli_reject_broken_units_file(tmp_path):
    """U-CFG-01 | EXT-01 | --units-file 깨진 JSON → ConfigError"""
    broken = tmp_path / "broken.json"
    broken.write_text("{not valid", encoding="utf-8")
    result = _run_cli("meter:2.5", "--units-file", str(broken))
    output = _combined_output(result)
    assert "Expecting" in output or "JSON" in output.lower() or "json" in output.lower()


def test_u_cfg_02_cli_load_valid_units_file(tmp_path):
    """U-CFG-02 | EXT-01 | --units-file 유효 JSON → 변환 성공"""
    units_file = tmp_path / "units.json"
    units_file.write_text(
        '{"meter": 1.0, "feet": 3.28084, "yard": 1.09361}',
        encoding="utf-8",
    )
    result = _run_cli("meter:2.5", "--units-file", str(units_file))
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_METER_25)


def test_u_cfg_03_cli_reject_missing_units_file():
    """U-CFG-03 | EXT-01 | --units-file 없는 경로 → ConfigError"""
    result = _run_cli("meter:2.5", "--units-file", "nope-does-not-exist.json")
    assert "No such file" in _combined_output(result)


def test_u_cfg_04_units_file_flag_without_value_uses_default():
    """U-CFG-04 | EXT-01 | --units-file 값 없음 → 기본 registry"""
    result = _run_cli("meter:2.5", "--units-file")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_METER_25)


def test_u_cfg_05_cli_project_units_json():
    """U-CFG-05 | EXT-01 | 루트 units.json → Golden Master table"""
    result = _run_cli("meter:2.5", "--units-file", "units.json")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_METER_25)


def test_golden_master_feet_10_stdout():
    """Golden Master | GM-FEET-10 | feet:10 → lecture I-02 stdout"""
    result = _run_cli("feet:10")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_FEET_10)


# --- TD-08: dynamic register CLI boundary (EXT-02) ---


def test_u_reg_01_cli_register_cubit_and_convert():
    """U-REG-01 | EXT-02 | --register 후 cubit:1 → Golden Master"""
    result = _run_cli(
        "cubit:1",
        "--register",
        "1 cubit = 0.4572 meter",
    )
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_REG_CUBIT_1)


def test_u_reg_02_cli_reject_invalid_register_expression():
    """U-REG-02 | EXT-02 | --register 잘못된 형식 → Golden Master 오류"""
    result = _run_cli("meter:2.5", "--register", "bad format")
    assert_matches_golden(_combined_output(result), GM_REG_ERR)


def test_u_reg_03_register_flag_without_value_ignored():
    """U-REG-03 | EXT-02 | --register 값 없음 → 등록 생략·기본 변환"""
    result = _run_cli("meter:2.5", "--register")
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_METER_25)


def test_u_reg_04_cli_units_file_and_register_combined(tmp_path):
    """U-REG-04 | EXT-02 | --units-file + --register 조합"""
    units_file = tmp_path / "units.json"
    units_file.write_text('{"meter": 1.0, "feet": 3.28084}', encoding="utf-8")
    result = _run_cli(
        "cubit:2",
        "--units-file",
        str(units_file),
        "--register",
        "1 cubit = 0.4572 meter",
    )
    assert result.returncode == 0
    assert_matches_golden(result.stdout, GM_REG_CUBIT_2)


# --- lecture I-05: unknown unit CLI boundary (FR-03) ---


def test_u_in_05_reject_unknown_unit_cubit():
    """U-IN-05 | FR-03 | cubit:1 (미등록) → Golden Master E-UNIT"""
    result = _run_cli("cubit:1")
    assert_matches_golden(_combined_output(result), GM_UNIT_CUBIT_ERR)
