"""Track A (Boundary) — PyQt GUI tests (TD-10, EXT-04)."""

import pytest

pytest.importorskip("PyQt6")

from PyQt6.QtWidgets import QApplication

from tests._approval import assert_matches_golden
from unit_converter.ui.main_window import MainWindow

E_NEG = "Negative value not allowed"
E_FMT = "Invalid format. Use unit:value (ex: meter:2.5)"

GM_METER_25 = "GM-METER-25"
GM_FMT_TABLE = "GM-FMT-TABLE"
GM_FMT_JSON = "GM-FMT-JSON"
GM_FMT_CSV = "GM-FMT-CSV"
GM_FEET_10 = "GM-FEET-10"
GM_METER_NEG = "GM-METER-NEG"


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def window(qapp):
    win = MainWindow()
    yield win
    win.close()


def _select_combo(combo, text: str) -> None:
    index = combo.findText(text)
    assert index >= 0
    combo.setCurrentIndex(index)


def _gui_output(window) -> str:
    return window.result_view.toPlainText()


def test_u_gui_01_convert_table_output(window):
    """U-GUI-01 | EXT-04 | format=table → Golden Master table"""
    _select_combo(window.unit_combo, "meter")
    _select_combo(window.format_combo, "table")
    window.value_input.setText("2.5")
    window.convert_button.click()

    assert_matches_golden(_gui_output(window) + "\n", GM_FMT_TABLE)


def test_u_gui_02_convert_json_output(window):
    """U-GUI-02 | EXT-04 | format=json → Golden Master JSON"""
    _select_combo(window.unit_combo, "meter")
    _select_combo(window.format_combo, "json")
    window.value_input.setText("2.5")
    window.convert_button.click()

    assert_matches_golden(_gui_output(window) + "\n", GM_FMT_JSON)


def test_u_gui_03_reject_negative_value(window):
    """U-GUI-03 | EXT-04 | value=-1 → Golden Master E-NEG"""
    _select_combo(window.unit_combo, "meter")
    window.value_input.setText("-1")
    window.convert_button.click()

    assert_matches_golden(_gui_output(window) + "\n", GM_METER_NEG)


def test_u_gui_04_reject_invalid_number(window):
    """U-GUI-04 | EXT-04 | value=abc → Invalid number"""
    _select_combo(window.unit_combo, "meter")
    window.value_input.setText("abc")
    window.convert_button.click()

    assert "Invalid number:" in window.result_view.toPlainText()


def test_u_gui_05_convert_csv_output(window):
    """U-GUI-05 | EXT-04 | format=csv → Golden Master CSV"""
    _select_combo(window.unit_combo, "meter")
    _select_combo(window.format_combo, "csv")
    window.value_input.setText("2.5")
    window.convert_button.click()

    assert_matches_golden(_gui_output(window) + "\n", GM_FMT_CSV)


def test_u_gui_06_default_format_is_table(window):
    """U-GUI-06 | EXT-04 | format 미변경 → table 기본 (Golden Master)"""
    assert window.format_combo.currentText() == "table"
    _select_combo(window.unit_combo, "meter")
    window.value_input.setText("2.5")
    window.convert_button.click()

    assert_matches_golden(_gui_output(window) + "\n", GM_FMT_TABLE)


def test_u_gui_07_reject_empty_value(window):
    """U-GUI-07 | EXT-04 | value='' → E-FMT"""
    _select_combo(window.unit_combo, "meter")
    window.value_input.setText("")
    window.convert_button.click()

    assert E_FMT in window.result_view.toPlainText()


def test_u_gui_08_convert_feet_input(window):
    """U-GUI-08 | EXT-04 | unit=feet, value=10 → Golden Master I-02"""
    _select_combo(window.unit_combo, "feet")
    _select_combo(window.format_combo, "table")
    window.value_input.setText("10")
    window.convert_button.click()

    assert_matches_golden(_gui_output(window) + "\n", GM_FEET_10)
