"""Track B (Domain) — parsing, conversion, registry tests (TD-01~03, TD-05~06)."""

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _module_source(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _imported_modules(source: str) -> set[str]:
    tree = ast.parse(source)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules

E_FMT = "Invalid format. Use unit:value (ex: meter:2.5)"
E_NUM = "Invalid number: {value_str}"
E_NEG = "Negative value not allowed"
E_UNIT = "Unknown unit: {unit}"

YARD_PER_METER = 1.09361
INCH_PER_METER = 39.37007874


def test_d_par_01_parse_valid_input():
    """D-PAR-01 | FR-01 | meter:2.5 → unit=meter, value=2.5"""
    from unit_converter.app.input_parser import parse

    unit, value = parse("meter:2.5")
    assert unit == "meter"
    assert value == 2.5


def test_d_par_02_reject_negative_value():
    """D-PAR-02 | FR-04 | meter:-1 → E-NEG"""
    from unit_converter.app.input_parser import ParseError, parse

    with pytest.raises(ParseError, match=E_NEG):
        parse("meter:-1")


def test_d_par_03_reject_invalid_number():
    """D-PAR-03 | FR-05 | meter:abc → E-NUM"""
    from unit_converter.app.input_parser import ParseError, parse

    with pytest.raises(ParseError, match=E_NUM.format(value_str="abc")):
        parse("meter:abc")


# --- TD-02: meter-based conversion (FR-02, NFR-03) ---


def test_d_cnv_01_feet_to_meter():
    """D-CNV-01 | NFR-03 | 1 feet → 0.3048 m (±0.0001)"""
    from unit_converter.domain.converter import to_meter

    assert to_meter("feet", 1) == pytest.approx(0.3048, abs=0.0001)


def test_d_cnv_02_convert_all_from_meter():
    """D-CNV-02 | FR-02 | 2.5 m → feet=8.2021 (4자리)"""
    from unit_converter.domain.converter import convert_all

    results = convert_all("meter", 2.5)
    assert results["feet"] == pytest.approx(8.2021, abs=0.00005)


def test_d_cnv_03_feet_to_yard_via_meter():
    """D-CNV-03 | FR-02 | feet→yard 환산은 meter 경유와 일치"""
    from unit_converter.domain.converter import convert_all, to_meter

    feet_value = 10.0
    results = convert_all("feet", feet_value)
    meter_value = to_meter("feet", feet_value)
    expected_yard = round(meter_value * YARD_PER_METER, 4)

    assert results["yard"] == pytest.approx(expected_yard, abs=0.0001)


# --- TD-03: unit registry / OCP (FR-03, NFR-01) ---


def test_d_reg_01_reject_unknown_unit():
    """D-REG-01 | FR-03 | cubit 미등록 → E-UNIT"""
    from unit_converter.domain.converter import convert_all
    from unit_converter.domain.unit_registry import UnknownUnitError

    with pytest.raises(UnknownUnitError, match=E_UNIT.format(unit="cubit")):
        convert_all("cubit", 1)


def test_d_reg_02_register_inch_without_converter_change():
    """D-REG-02 | NFR-01 | inch 등록 후 Converter 핵심 비수정으로 환산"""
    from unit_converter.domain.converter import convert_all
    from unit_converter.domain.unit_registry import UnitRegistry

    registry = UnitRegistry.default()
    registry.register("inch", INCH_PER_METER)

    results = convert_all("meter", 1.0, registry=registry)
    assert results["inch"] == pytest.approx(39.3701, abs=0.0001)


# --- TD-05~06: SRP package structure (NFR-02, D-STR-01~04) ---


def test_d_str_01_input_parser_module():
    """D-STR-01 | NFR-02 | input_parser 모듈·파싱 책임만"""
    path = ROOT / "unit_converter/app/input_parser.py"
    assert path.is_file()

    from unit_converter.app.input_parser import parse

    assert callable(parse)

    imports = _imported_modules(_module_source("unit_converter/app/input_parser.py"))
    forbidden = {
        "unit_converter.domain.converter",
        "unit_converter.app.output_formatter",
        "unit_converter.cli",
    }
    assert imports.isdisjoint(forbidden)


def test_d_str_02_unit_registry_module():
    """D-STR-02 | NFR-02 | unit_registry 모듈·등록·조회 책임만"""
    path = ROOT / "unit_converter/domain/unit_registry.py"
    assert path.is_file()

    from unit_converter.domain.unit_registry import UnitRegistry

    assert callable(UnitRegistry.default)

    imports = _imported_modules(_module_source("unit_converter/domain/unit_registry.py"))
    forbidden = {
        "unit_converter.domain.converter",
        "unit_converter.app.input_parser",
        "unit_converter.app.output_formatter",
        "unit_converter.cli",
    }
    assert imports.isdisjoint(forbidden)


def test_d_str_03_converter_module():
    """D-STR-03 | NFR-02 | converter 모듈·환산 책임만"""
    path = ROOT / "unit_converter/domain/converter.py"
    assert path.is_file()

    from unit_converter.domain.converter import convert_all, to_meter

    assert callable(to_meter)
    assert callable(convert_all)

    imports = _imported_modules(_module_source("unit_converter/domain/converter.py"))
    forbidden = {
        "unit_converter.app.input_parser",
        "unit_converter.app.output_formatter",
        "unit_converter.cli",
    }
    assert imports.isdisjoint(forbidden)


def test_d_str_04_output_formatter_module():
    """D-STR-04 | NFR-02 | output_formatter 모듈·출력 포맷 책임만"""
    path = ROOT / "unit_converter/app/output_formatter.py"
    assert path.is_file()

    from unit_converter.app.output_formatter import format_conversion_output

    output = format_conversion_output("meter", 2.5, {"meter": 2.5, "feet": 8.2021})
    assert "2.5 meter = 2.5000 meter" in output
    assert "8.2021 feet" in output

    imports = _imported_modules(_module_source("unit_converter/app/output_formatter.py"))
    forbidden = {
        "unit_converter.domain.converter",
        "unit_converter.domain.unit_registry",
        "unit_converter.app.input_parser",
        "unit_converter.cli",
    }
    assert imports.isdisjoint(forbidden)
