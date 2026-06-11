"""Track B (Domain) — input parsing tests (TD-01)."""

import pytest

E_FMT = "Invalid format. Use unit:value (ex: meter:2.5)"
E_NUM = "Invalid number: {value_str}"
E_NEG = "Negative value not allowed"


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
