from PyQt6.QtWidgets import QFileDialog

from finance_tracker_app.widgets.drop_area_ui import DropArea_ui


class DropArea(DropArea_ui):
    def __init__(self) -> None:
        super().__init__()
        self.drop_frame.upload_btn.clicked.connect(self.open_file)

    def open_file(self) -> None:
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Open CSV", "", "CSV files (*.csv)"
        )
        if file_paths:
            self.drop_frame.file_paths.extend(file_paths)
            self.drop_frame._update_label()
            self.drop_frame.successful_highlight()
