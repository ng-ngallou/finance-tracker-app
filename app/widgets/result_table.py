from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ResultTable(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.table = QTableWidget()
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

        font = QFont()
        font.setPointSize(16)
        self.table.setFont(font)

        font.setPointSize(18)

        self.label = QLabel("Total Monthly Expenses:")
        self.label.setFont(font)
        frame_layout.addWidget(self.label)

        frame_layout.addWidget(self.table)

        layout.addWidget(frame)
        self.setLayout(layout)

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Category", "Amount"])

    def populate(self, data: dict) -> None:
        self.table.clear()

        self.table.setRowCount(len(data))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Category", "Amount"])

        for i, (category, amount) in enumerate(data.items()):
            self.table.setItem(i, 0, QTableWidgetItem(category))
            self.table.setItem(i, 1, QTableWidgetItem(str(amount)))

        self.table.resizeColumnsToContents()
