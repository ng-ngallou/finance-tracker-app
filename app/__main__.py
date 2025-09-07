import calendar
import sys

import pandas as pd
from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

from app.core.scrape_exch_rate import ExchangeRate
from app.core.transactions import Transactions
from app.widgets.file_drop_area import DropArea
from app.widgets.plot import PlotWidget
from app.widgets.result_table import ResultTable
from app.widgets.unclassified import PrintoutWidget


class FinanceTrackerApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        # Init GUI
        self.setWindowTitle("Personal Finance Tracker")
        self.setMinimumSize(1200, 900)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(1, 1, 1, 1)
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

        self.statusBar().showMessage('Select a CSV file and press "Analyze".')

        # Connect button
        self.drop_area.analyze_btn.clicked.connect(self.run_analysis)

    def run_analysis(self) -> None:
        # self.result_table.table.clear()
        # self.plot_widget.figure.clear()
        # self.printout_widget.text_area.clear()

        path = (
            self.drop_area.drop_frame.file_path
            if self.drop_area.drop_frame.file_path is not None
            else self.drop_area.open_file_path
        )
        if not path:
            self.statusBar().showMessage("Please select a CSV file first.")
            return
        try:
            # Load the data
            df = pd.read_csv(path, sep=";", skiprows=1)
            df = df.dropna(subset=["Card number"])

            # Expose month and year
            last_date = df["Purchase date"][0]
            year = last_date.split(".")[-1]
            int_month = int(last_date.split(".")[1])
            month = calendar.month_abbr[int_month]

            # Scrape exchange rate
            exch = ExchangeRate(month, year)
            rate = exch.find_exch_rate()

            # Analyze transactions
            tr = Transactions(df, exchange_rate=rate)
            tr.analyze()

            # Plot results
            self.plot_widget.plot(
                tr.EXP_CATEGORIES, title=f"{calendar.month_name[int_month]} {year}"
            )

            # Result table
            self.result_table.label.setText(
                f"Total Monthly Expenses: {round(tr.total_expenses, 2)} EUR"
            )
            self.result_table.populate(tr.EXP_CATEGORIES)

            # Unclassified transactions
            self.printout_widget.dump_text(tr.UNCLASSIFIED_EXPENSES)

            self.statusBar().showMessage("Analysis completed successfully.")
        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceTrackerApp()
    window.show()
    sys.exit(app.exec())
