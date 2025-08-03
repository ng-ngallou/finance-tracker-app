from PyQt6.QtWidgets import QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem


class ResultTable(QWidget):
    def __init__(self):
        super().__init__()
        self.table = QTableWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def populate(self, data: dict):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Category", "Amount"])
        for i, (category, amount) in enumerate(data.items()):
            self.table.setItem(i, 0, QTableWidgetItem(category))
            self.table.setItem(i, 1, QTableWidgetItem(str(amount)))
