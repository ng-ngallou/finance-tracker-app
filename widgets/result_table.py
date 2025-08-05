from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QLabel


class ResultTable(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()

        layout = QVBoxLayout()
        font = QFont()
        font.setPointSize(14)

        label = QLabel("Total Monthly Expenses:")
        label.setFont(font)
        layout.addWidget(label)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def populate(self, data: dict):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Category", "Amount"])
        for i, (category, amount) in enumerate(data.items()):
            self.table.setItem(i, 0, QTableWidgetItem(category))
            self.table.setItem(i, 1, QTableWidgetItem(str(amount)))
