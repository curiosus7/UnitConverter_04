"""PyQt desktop GUI for unit conversion (EXT-04)."""

from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from unit_converter.app.conversion_service import (
    ParseError,
    UnknownUnitError,
    build_registry,
    convert_input,
)
from unit_converter.app.output_formatter import VALID_FORMATS
from unit_converter.domain.unit_registry import UnitRegistry


class MainWindow(QMainWindow):
    def __init__(self, registry: UnitRegistry | None = None) -> None:
        super().__init__()
        self._registry = registry or build_registry()
        self.setWindowTitle("Unit Converter")
        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        unit_row = QHBoxLayout()
        unit_row.addWidget(QLabel("Unit:"))
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(sorted(self._registry.all_units()))
        unit_row.addWidget(self.unit_combo)
        layout.addLayout(unit_row)

        value_row = QHBoxLayout()
        value_row.addWidget(QLabel("Value:"))
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("2.5")
        value_row.addWidget(self.value_input)
        layout.addLayout(value_row)

        format_row = QHBoxLayout()
        format_row.addWidget(QLabel("Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(sorted(VALID_FORMATS))
        default_format_index = self.format_combo.findText("table")
        if default_format_index >= 0:
            self.format_combo.setCurrentIndex(default_format_index)
        format_row.addWidget(self.format_combo)
        layout.addLayout(format_row)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self._on_convert)
        layout.addWidget(self.convert_button)

        self.result_view = QPlainTextEdit()
        self.result_view.setReadOnly(True)
        self.result_view.setPlaceholderText("Conversion results appear here.")
        layout.addWidget(self.result_view)

    def _on_convert(self) -> None:
        unit = self.unit_combo.currentText()
        value_text = self.value_input.text().strip()
        output_format = self.format_combo.currentText()

        try:
            from unit_converter.app.input_parser import parse

            _, value = parse(f"{unit}:{value_text}")
            output = convert_input(
                unit,
                value,
                output_format=output_format,
                registry=self._registry,
            )
            self.result_view.setPlainText(output.rstrip("\n"))
        except (ParseError, UnknownUnitError) as exc:
            self.result_view.setPlainText(str(exc))
