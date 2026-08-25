"""
BCF Converter

Application entry point.
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from gui import MainWindow


def main() -> int:
    app = QApplication(sys.argv)

    app.setApplicationName("BCF Converter")
    app.setApplicationVersion("1.0.1")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())