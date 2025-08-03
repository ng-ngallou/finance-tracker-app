import os

from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QFileDialog

from uis.drop_area_ui import DropArea_ui


class DropArea(DropArea_ui):
    def __init__(self):
        super().__init__()

        self.drop_frame.upload_btn.clicked.connect(self.open_file)
        self.file_path = None


    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV files (*.csv)")
        if file_path:
            self.file_path = file_path
            self.drop_frame.label.setText(f"Selected: {os.path.basename(self.file_path)}")
