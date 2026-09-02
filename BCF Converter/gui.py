"""
BCF Converter

Graphical user interface for BCF loading and HDF5 conversion.

Provides the main application window and background worker classes
used to load BCF files, generate spectral previews, and save
converted data without blocking the user interface.

Copyright (c) 2026 Nicolas Gros

Licensed under the the GPL-3.0 license.
See the LICENSE file in the project root for details.
"""

from pathlib import Path

import numpy as np

from PySide6.QtCore import QObject, QThread, Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from converter import load_bcf, roi_preview, save_hdf5


# =============================================================================
# Worker classes
# =============================================================================

class LoadWorker(QObject):

    finished = Signal(object, object, object)
    error = Signal(str)

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        try:
            cube, metadata = load_bcf(self.filename)
            preview = roi_preview(cube)
            self.finished.emit(cube, metadata, preview)

        except Exception as e:
            self.error.emit(str(e))


class SaveWorker(QObject):

    finished = Signal()
    error = Signal(str)

    def __init__(self, cube, metadata, filename):
        super().__init__()
        self.cube = cube
        self.metadata = metadata
        self.filename = filename

    def run(self):
        try:
            save_hdf5(
                self.cube,
                self.metadata,
                self.filename,
            )
            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))


# =============================================================================
# Main Window
# =============================================================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("BCF → HDF5 Converter")
        self.resize(800, 700)

        self.cube = None
        self.metadata = None
        self.filename = None

        self.load_thread = None
        self.load_worker = None

        self.save_thread = None
        self.save_worker = None

        # ---------------------------------------------------------------------

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        self.open_button = QPushButton("Open BCF")
        self.convert_button = QPushButton("Convert to HDF5")
        self.convert_button.setEnabled(False)

        self.image = QLabel("Preview")
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumHeight(500)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)

        layout.addWidget(self.open_button)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.image)
        layout.addWidget(self.log)

        self.open_button.clicked.connect(self.open_file)
        self.convert_button.clicked.connect(self.convert)

    # =========================================================================

    def write(self, text):
        self.log.append(text)

    # =========================================================================

    def open_file(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open BCF",
            "",
            "BCF (*.bcf)",
        )

        if not filename:
            return

        self.filename = Path(filename)

        self.open_button.setEnabled(False)
        self.convert_button.setEnabled(False)

        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.write(f"Loading {self.filename.name}...")

        self.load_thread = QThread()
        self.load_worker = LoadWorker(filename)

        self.load_worker.moveToThread(self.load_thread)

        self.load_thread.started.connect(self.load_worker.run)

        self.load_worker.finished.connect(self.loading_finished)
        self.load_worker.error.connect(self.worker_error)

        self.load_worker.finished.connect(self.load_thread.quit)
        self.load_worker.error.connect(self.load_thread.quit)

        self.load_thread.finished.connect(self.load_thread.deleteLater)

        self.load_worker.finished.connect(self.load_worker.deleteLater)
        self.load_worker.error.connect(self.load_worker.deleteLater)

        self.load_thread.start()

    # =========================================================================

    def loading_finished(self, cube, metadata, preview):

        QApplication.restoreOverrideCursor()

        self.cube = cube
        self.metadata = metadata

        self.show_image(preview)

        self.write(f"Cube shape : {cube.shape}")
        self.write("Done.")

        self.open_button.setEnabled(True)
        self.convert_button.setEnabled(True)

    # =========================================================================

    def convert(self):

        outfile, _ = QFileDialog.getSaveFileName(
            self,
            "Save HDF5",
            self.filename.with_suffix(".h5").name,
            "HDF5 (*.h5)",
        )

        if not outfile:
            return

        self.open_button.setEnabled(False)
        self.convert_button.setEnabled(False)

        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.write("Saving...")

        self.save_thread = QThread()
        self.save_worker = SaveWorker(
            self.cube,
            self.metadata,
            outfile,
        )

        self.save_worker.moveToThread(self.save_thread)

        self.save_thread.started.connect(self.save_worker.run)

        self.save_worker.finished.connect(
            lambda: self.save_finished(outfile)
        )

        self.save_worker.error.connect(self.worker_error)

        self.save_worker.finished.connect(self.save_thread.quit)
        self.save_worker.error.connect(self.save_thread.quit)

        self.save_thread.finished.connect(self.save_thread.deleteLater)

        self.save_worker.finished.connect(self.save_worker.deleteLater)
        self.save_worker.error.connect(self.save_worker.deleteLater)

        self.save_thread.start()

    # =========================================================================

    def save_finished(self, outfile):

        QApplication.restoreOverrideCursor()

        self.write(f"Saved:\n{outfile}")

        self.open_button.setEnabled(True)
        self.convert_button.setEnabled(True)

    # =========================================================================

    def worker_error(self, message):

        QApplication.restoreOverrideCursor()

        self.write("ERROR")
        self.write(message)

        self.open_button.setEnabled(True)

        if self.cube is not None:
            self.convert_button.setEnabled(True)

    # =========================================================================

    def show_image(self, img):

        img = img.astype(np.float32)

        img -= img.min()

        maximum = img.max()

        if maximum > 0:
            img /= maximum

        img *= 255

        img = img.astype(np.uint8)

        h, w = img.shape

        qimg = QImage(
            img.data,
            w,
            h,
            w,
            QImage.Format_Grayscale8,
        )

        pixmap = QPixmap.fromImage(qimg)

        self.image.setPixmap(
            pixmap.scaled(
                self.image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    # =========================================================================

    def resizeEvent(self, event):

        pixmap = self.image.pixmap()

        if pixmap is not None and not pixmap.isNull():

            self.image.setPixmap(
                pixmap.scaled(
                    self.image.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

        super().resizeEvent(event)

    # =========================================================================

    def closeEvent(self, event):

        if (
            self.load_thread is not None
            and self.load_thread.isRunning()
        ):
            event.ignore()
            return

        if (
            self.save_thread is not None
            and self.save_thread.isRunning()
        ):
            event.ignore()
            return

        event.accept()
