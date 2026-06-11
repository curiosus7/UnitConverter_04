"""Track B (Domain) — parsing, conversion, registry tests (TD-01~03)."""

import pytest

E_FMT = "Invalid format. Use unit:value (ex: meter:2.5)"
E_NUM = "Invalid number: {value_str}"
E_NEG = "Negative value not allowed"
YARD_PER_METER = 1.09361


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
