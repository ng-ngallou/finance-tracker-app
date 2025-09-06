from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QLabel, QTextEdit, QVBoxLayout, QWidget


class PrintoutWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

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

        font = QFont()
        font.setPointSize(14)
        self.text_area.setFont(font)

        font.setPointSize(18)

        label = QLabel("Unclassified Transactions:")
        label.setFont(font)
        frame_layout.addWidget(label)

        frame_layout.addWidget(self.text_area)

        layout.addWidget(frame)
        self.setLayout(layout)

    def dump_text(self, lines: list[str]) -> None:
        self.text_area.clear()
        self.text_area.append(
            "\n\n------------------------------------------------------------------------------------\n\n".join(
                lines
            )
        )
