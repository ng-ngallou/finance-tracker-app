import os

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout


class DropArea_ui(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("DropWidget")
        self.setStyleSheet("""
                    QFrame#DropWidget {
                        border-radius: 10%;
                        background-color: white;
                    }
                """)

        layout = QVBoxLayout()

        frame = QFrame(self)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)

        self.drop_frame = DropFrame()
        self.drop_frame.resize(550, 300)
        frame_layout.addWidget(self.drop_frame, stretch=1)

        font = QFont()
        font.setPointSize(16)

        self.analyze_btn = RoundedButton("Analyze")
        self.analyze_btn.setMinimumSize(QSize(100, 40))
        self.analyze_btn.setFont(font)
        frame_layout.addWidget(self.analyze_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(frame)

        self.setLayout(layout)


class DropFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("DropArea")
        self.setAcceptDrops(True)
        self.file_path = None

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

        self.label = QLabel("Drag and drop a CSV file here")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.setLayout(layout)

        bottom_right_layout = QHBoxLayout()
        bottom_right_layout.addStretch()
        self.upload_btn = RoundedButton("Or select CSV file")
        self.upload_btn.setMinimumSize(QSize(150, 40))
        self.upload_btn.setFont(font)
        bottom_right_layout.addWidget(self.upload_btn)

        layout.addLayout(bottom_right_layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.set_highlight(True)

    def dragLeaveEvent(self, event):
        self.set_highlight(False)

    def dropEvent(self, event: QDropEvent):
        self.set_highlight(False)
        urls = event.mimeData().urls()
        if urls and urls[0].toLocalFile().endswith(".csv"):
            self.file_path = urls[0].toLocalFile()
            self.label.setText(os.path.basename(self.file_path))
            self.successful_highlight()
        else:
            self.label.setText("Invalid file type. Please drop a CSV.")

    def set_highlight(self, on: bool):
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

    def successful_highlight(self):
        self.setStyleSheet("""
        QFrame#DropArea {
        border: 2px dashed #aaa;
        border-radius: 20%;
        background-color: #e8f5e9;
        }
    """)


class RoundedButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #318CE7;   /* Blue */
                color: white;
                border: 2px solid #0078d7;
                border-radius: 15%;
            }

            QPushButton:hover {
                background-color: #1976D2;   /* Darker blue */
            }

            QPushButton:pressed {
                background-color: #1565C0;   /* Even darker blue */
            }
        """)


