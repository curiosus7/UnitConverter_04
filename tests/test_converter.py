"""Track B (Domain) — parsing, conversion, registry tests (TD-01~03)."""

import pytest

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
