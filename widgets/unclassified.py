from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel


class PrintoutWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)

        font = QFont()
        font.setPointSize(14)
        self.text_area.setFont(font)

        font.setPointSize(18)

        label = QLabel("Unclassified Transactions:")
        label.setFont(font)
        layout.addWidget(label)

        layout.addWidget(self.text_area)
        self.setLayout(layout)

    def dump_text(self, lines: list[str]):
        self.text_area.clear()
        self.text_area.append(
            "\n\n------------------------------------------------------------------------------------\n\n".join(lines)
        )
