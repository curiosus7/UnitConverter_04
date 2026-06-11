"""Track A (Boundary) — PyQt GUI tests (TD-10, EXT-04)."""

import json

import pytest

pytest.importorskip("PyQt6")

from PyQt6.QtWidgets import QApplication

from unit_converter.ui.main_window import MainWindow

E_NEG = "Negative value not allowed"


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


def test_u_gui_01_convert_table_output(window):
    """U-GUI-01 | EXT-04 | Convert → table 형식 3줄 이상, 4자리"""
    _select_combo(window.unit_combo, "meter")
    _select_combo(window.format_combo, "table")
    window.value_input.setText("2.5")
    window.convert_button.click()

    output = window.result_view.toPlainText()
    lines = [line for line in output.strip().splitlines() if line.strip()]
    assert len(lines) >= 3
    assert "8.2021" in output
    assert "2.7340" in output


def test_u_gui_02_convert_json_output(window):
    """U-GUI-02 | EXT-04 | format=json → 유효 JSON"""
    _select_combo(window.unit_combo, "meter")
    _select_combo(window.format_combo, "json")
    window.value_input.setText("2.5")
    window.convert_button.click()

    data = json.loads(window.result_view.toPlainText())
    assert data["input"]["unit"] == "meter"
    assert data["results"]["feet"] == 8.2021


def test_u_gui_03_reject_negative_value(window):
    """U-GUI-03 | EXT-04 | value=-1 → E-NEG"""
    _select_combo(window.unit_combo, "meter")
    window.value_input.setText("-1")
    window.convert_button.click()

    assert E_NEG in window.result_view.toPlainText()


def test_u_gui_04_reject_invalid_number(window):
    """U-GUI-04 | EXT-04 | value=abc → Invalid number"""
    _select_combo(window.unit_combo, "meter")
    window.value_input.setText("abc")
    window.convert_button.click()

    assert "Invalid number:" in window.result_view.toPlainText()
