from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel


class PrintoutWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(QLabel("Unclassified Transactions"))
        layout.addWidget(self.text_area)
        self.setLayout(layout)

    def dump_text(self, lines: list[str]):
        self.text_area.clear()
        self.text_area.append("\n".join(lines))
