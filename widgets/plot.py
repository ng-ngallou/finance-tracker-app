from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(18)

        frame = QFrame(self)
        frame.setObjectName('frame1')
        frame.setStyleSheet("""
            QFrame#frame1 {
                border-radius: 10%;
                background-color: white;
            }
        """)
        frame_layout = QVBoxLayout()
        frame.setLayout(frame_layout)

        self.label = QLabel("Percentage of total expenses:")
        self.label.setFont(font)
        frame_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignTop)

        self.figure = Figure(figsize=(4, 3))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        frame_layout.addWidget(self.canvas)

        layout.addWidget(frame)
        self.setLayout(layout)

    def plot(self, data: dict, title: str) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(data.values(), labels=list(data.keys()), autopct='%1.1f%%')
        ax.set_title(title)
        self.canvas.draw()
