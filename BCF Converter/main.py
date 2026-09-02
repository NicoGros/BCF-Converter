"""
BCF Converter

Application entry point.

Initializes the Qt application, sets application metadata,
and launches the main application window.

Copyright (c) 2026 Nicolas Gros

Licensed under the the GPL-3.0 license.
See the LICENSE file in the project root for details.
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
