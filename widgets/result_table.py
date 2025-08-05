from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QLabel


class ResultTable(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()

        layout = QVBoxLayout()
        font = QFont()
        font.setPointSize(16)
        self.table.setFont(font)

        font.setPointSize(18)

        self.label = QLabel("Total Monthly Expenses:")
        self.label.setFont(font)
        layout.addWidget(self.label)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def populate(self, data: dict):
        self.table.clear()

        self.table.setRowCount(len(data))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Category", "Amount"])

        for i, (category, amount) in enumerate(data.items()):
            self.table.setItem(i, 0, QTableWidgetItem(category))
            self.table.setItem(i, 1, QTableWidgetItem(str(amount)))

        self.table.resizeColumnsToContents()
