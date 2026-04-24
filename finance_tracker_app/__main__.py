import calendar
import sys

import pandas as pd
from PyQt6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

from finance_tracker_app.core.scrape_exch_rate import ExchangeRate
from finance_tracker_app.core.transactions import Transactions
from finance_tracker_app.widgets.file_drop_area import DropArea
from finance_tracker_app.widgets.plot import PlotWidget
from finance_tracker_app.widgets.result_table import ResultTable
from finance_tracker_app.widgets.unclassified import PrintoutWidget


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

        # Place widgets
        layout.addWidget(self.drop_area, 0, 0)
        layout.addWidget(self.plot_widget, 0, 1)
        layout.addWidget(self.result_table, 1, 1)
        layout.addWidget(self.printout_widget, 1, 0)

        self.statusBar().showMessage('Select CSV files and press "Analyze".')

        # Connect buttons
        self.drop_area.analyze_btn.clicked.connect(self.run_analysis)
        self.drop_area.new_analysis_btn.clicked.connect(self.reset_app)

    def run_analysis(self) -> None:
        paths = self.drop_area.drop_frame.file_paths
        if not paths:
            self.statusBar().showMessage("Please select at least one CSV file first.")
            return
        try:
            merged_categories: dict = {}
            all_unclassified: list = []
            total_expenses = 0.0
            titles = []
            rates_msg = []

            for path in paths:
                df = pd.read_csv(path, sep=";", skiprows=1)
                df = df.dropna(subset=["Card number"])

                last_date = df["Purchase date"][0]
                year = last_date.split(".")[-1]
                int_month = int(last_date.split(".")[1])
                month = calendar.month_abbr[int_month]

                exch = ExchangeRate(month, year)
                rate = exch.find_exch_rate()
                rates_msg.append(f"{month} {year}: 1CHF={rate}EUR")

                tr = Transactions(df, exchange_rate=rate)
                tr.analyze()

                for key, val in tr.EXP_CATEGORIES.items():
                    merged_categories[key] = round(
                        merged_categories.get(key, 0.0) + val, 2
                    )
                all_unclassified.extend(tr.UNCLASSIFIED_EXPENSES)
                total_expenses += tr.total_expenses
                titles.append(f"{calendar.month_name[int_month]} {year}")

            title = titles[0] if len(titles) == 1 else f"{titles[0]} – {titles[-1]}"

            self.statusBar().showMessage(" | ".join(rates_msg))

            self.plot_widget.plot(merged_categories, title=title)

            self.result_table.label.setText(
                f"Total Expenses: {round(total_expenses, 2)} EUR"
            )
            self.result_table.populate(merged_categories)

            self.printout_widget.dump_text(all_unclassified)

        except Exception as e:
            self.statusBar().showMessage(f"Error: {e}")

    def reset_app(self) -> None:
        self.drop_area.drop_frame.reset()
        self.plot_widget.figure.clear()
        self.plot_widget.canvas.draw()
        self.result_table.label.setText("Total Expenses:")
        self.result_table.table.clear()
        self.result_table.table.setColumnCount(2)
        self.result_table.table.setHorizontalHeaderLabels(["Category", "Amount"])
        self.result_table.table.setRowCount(0)
        self.printout_widget.text_area.clear()
        self.statusBar().showMessage('Select CSV files and press "Analyze".')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinanceTrackerApp()
    window.show()
    sys.exit(app.exec())
