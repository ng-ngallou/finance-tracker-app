import os
from PyQt6.QtWidgets import QFileDialog
from uis.drop_area_ui import DropArea_ui


class DropArea(DropArea_ui):
    def __init__(self):
        super().__init__()
        self.open_file_path = None
        self.drop_frame.upload_btn.clicked.connect(self.open_file)


    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV files (*.csv)")
        if file_path:
            self.open_file_path = file_path
            print(self.open_file_path)
            self.drop_frame.label.setText(os.path.basename(self.open_file_path))
            self.drop_frame.successful_highlight()
            self.drop_frame.file_path = None
