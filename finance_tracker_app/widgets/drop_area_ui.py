import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDropEvent, QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DropArea_ui(QWidget):
    """Drop Area widget, includes drop frame and buttons."""

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()

        frame = QFrame(self)
        frame.setObjectName("frame1")
        frame.setStyleSheet("""
            QFrame#frame1 {
                border-radius: 10%;
                background-color: white;
            }
        """)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)

        self.drop_frame = DropFrame()
        self.drop_frame.resize(550, 300)
        frame_layout.addWidget(self.drop_frame, stretch=1)

        font = QFont()
        font.setPointSize(16)

        button_layout = QHBoxLayout()

        self.new_analysis_btn = SecondaryButton("New Analysis")
        self.new_analysis_btn.setMinimumSize(QSize(100, 40))
        self.new_analysis_btn.setFont(font)
        button_layout.addWidget(self.new_analysis_btn)

        self.analyze_btn = RoundedButton("Analyze")
        self.analyze_btn.setMinimumSize(QSize(100, 40))
        self.analyze_btn.setFont(font)
        button_layout.addWidget(self.analyze_btn)

        frame_layout.addLayout(button_layout)

        layout.addWidget(frame)

        self.setLayout(layout)


class DropFrame(QFrame):
    """Drop Area to drop files for analysis. Supports multiple CSV files."""

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("DropArea")
        self.setAcceptDrops(True)
        self.file_paths: list[str] = []

        self.setStyleSheet("""
            QFrame#DropArea {
                border: 2px dashed #aaa;
                border-radius: 10%;
                background-color: white;
            }
        """)

        font = QFont()
        font.setPointSize(16)

        layout = QVBoxLayout()

        self.label = QLabel("Drag and drop CSV files here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.setLayout(layout)

        bottom_right_layout = QHBoxLayout()
        bottom_right_layout.addStretch()
        self.upload_btn = RoundedButton("Or select CSV file(s)")
        self.upload_btn.setMinimumSize(QSize(150, 40))
        self.upload_btn.setFont(font)
        bottom_right_layout.addWidget(self.upload_btn)

        layout.addLayout(bottom_right_layout)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.set_highlight(True)

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        self.set_highlight(False)

    def dropEvent(self, event: QDropEvent) -> None:
        self.set_highlight(False)
        urls = event.mimeData().urls()
        valid = [u.toLocalFile() for u in urls if u.toLocalFile().endswith(".csv")]
        if valid:
            self.file_paths.extend(valid)
            self._update_label()
            self.successful_highlight()
        else:
            self.label.setText("Invalid file type. Please drop CSV files.")

    def _update_label(self) -> None:
        n = len(self.file_paths)
        if n == 0:
            self.label.setText("Drag and drop CSV files here")
        elif n <= 3:
            self.label.setText("\n".join(os.path.basename(p) for p in self.file_paths))
        else:
            self.label.setText(f"{n} CSV files selected")

    def reset(self) -> None:
        self.file_paths = []
        self.label.setText("Drag and drop CSV files here")
        self.setStyleSheet("""
            QFrame#DropArea {
                border: 2px dashed #aaa;
                border-radius: 20%;
                background-color: white;
            }
        """)

    def set_highlight(self, on: bool) -> None:
        if on:
            self.setStyleSheet("""
                QFrame#DropArea {
                    border: 2px solid #0078d7;
                    border-radius: 20%;
                    background-color: #e6f2ff;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame#DropArea {
                    border: 2px dashed #aaa;
                    border-radius: 20%;
                    background-color: white;
                }
            """)

    def successful_highlight(self) -> None:
        self.setStyleSheet("""
        QFrame#DropArea {
        border: 2px dashed #aaa;
        border-radius: 20%;
        background-color: #e8f5e9;
        }
    """)


class RoundedButton(QPushButton):
    """ " Class for rounded blue buttons. They get darker when hovered over and clicked on."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #318CE7;   /* Blue */
                color: white;
                border-radius: 15%;
            }

            QPushButton:hover {
                background-color: #1976D2;   /* Darker blue */
            }

            QPushButton:pressed {
                background-color: #1565C0;   /* Even darker blue */
            }
        """)


class SecondaryButton(QPushButton):
    """Gray secondary button for reset/secondary actions."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border-radius: 15%;
            }

            QPushButton:hover {
                background-color: #616161;
            }

            QPushButton:pressed {
                background-color: #424242;
            }
        """)
