import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel
)
from PyQt6.QtCore import Qt

from widgets.file_drop_area import DropArea
from widgets.plot import PlotWidget
from widgets.result_table import ResultTable
from widgets.unclassified import PrintoutWidget


class FinanceTracker(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.empty_widget = QLabel("Reserved for future use")
        self.empty_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Place widgets
        layout.addWidget(self.drop_area, 0, 0)
        layout.addWidget(self.plot_widget, 0, 1)
        layout.addWidget(self.result_table, 1, 0)
        layout.addWidget(self.printout_widget, 1, 1)
        layout.addWidget(self.empty_widget, 2, 0, 1, 2)

        # Connect button
        self.drop_area.analyze_btn.clicked.connect(self.run_analysis)

    def run_analysis(self):
        path = self.drop_area.file_path
        if not path:
            self.statusBar().showMessage("Please select a CSV file first.")
            return
        try:
            # TODO: run analysis here
            self.statusBar().showMessage("Analysis complete.")
        except Exception as e:
            self.statusBar().showMessage(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceTracker()
    window.show()
    sys.exit(app.exec())
