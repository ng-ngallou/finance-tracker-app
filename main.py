import logging
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel
)
from PyQt6.QtCore import Qt

from core.transactions import Transactions
from widgets.file_drop_area import DropArea
from widgets.plot import PlotWidget
from widgets.result_table import ResultTable
from widgets.unclassified import PrintoutWidget


class FinanceTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        # Init GUI
        self.setWindowTitle("Personal Finance Tracker")
        self.setMinimumSize(1200, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        central_widget.setLayout(layout)

        # Initialize widgets
        self.drop_area = DropArea()
        self.plot_widget = PlotWidget()
        self.result_table = ResultTable()
        self.printout_widget = PrintoutWidget()
        # self.empty_widget = QLabel("Reserved for future use")
        # self.empty_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Place widgets
        layout.addWidget(self.drop_area, 0, 0)
        layout.addWidget(self.plot_widget, 0, 1)
        layout.addWidget(self.result_table, 1, 1)
        layout.addWidget(self.printout_widget, 1, 0)
        # layout.addWidget(self.empty_widget, 2, 0, 1, 2)

        self.statusBar().showMessage("Select a CSV file and press 'Analyze'.")

        # Connect button
        self.drop_area.analyze_btn.clicked.connect(self.run_analysis)

    def run_analysis(self):
        path = self.drop_area.drop_frame.file_path if self.drop_area.drop_frame.file_path is not None else self.drop_area.open_file_path
        if not path:
            self.statusBar().showMessage("Please select a CSV file first.")
            return
        try:
            # Analyze transactions
            tr = Transactions(path, exchange_rate=1.07)
            tr.analyze()

            # Plot results
            self.plot_widget.plot(tr.EXP_CATEGORIES, title=f"{tr.month} {tr.year}")

            # Results table
            self.result_table.label.setText(f"Total Monthly Expenses: {tr.total_expenses} EUR")
            self.result_table.populate(tr.EXP_CATEGORIES)

            # Unclassified transactions
            self.printout_widget.dump_text(tr.UNCLASSIFIED_EXPENSES)

            self.statusBar().showMessage("Analysis complete.")
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceTracker()
    window.show()
    sys.exit(app.exec())
