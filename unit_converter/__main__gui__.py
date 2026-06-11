import sys

from PyQt6.QtWidgets import QApplication

from unit_converter.ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(520, 420)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
