import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog


class DropArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        self.label = QLabel("Drag and drop a CSV file here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.upload_btn = QPushButton("Or select CSV file")
        self.upload_btn.clicked.connect(self.open_file)
        layout.addWidget(self.upload_btn)

        self.analyze_btn = QPushButton("Analyze")
        layout.addWidget(self.analyze_btn)

        self.setLayout(layout)
        self.file_path = None

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].toLocalFile().endswith(".csv"):
            self.file_path = urls[0].toLocalFile()
            self.label.setText(f"Dropped: {os.path.basename(self.file_path)}")
        else:
            self.label.setText("Invalid file type. Please drop a CSV.")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV files (*.csv)")
        if file_path:
            self.file_path = file_path
            self.label.setText(f"Selected: {os.path.basename(self.file_path)}")
