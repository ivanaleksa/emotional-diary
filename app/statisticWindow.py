import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QComboBox,
)

from .fileWorker import FileWorker

FILE_WORKER = FileWorker()

class AnalyticsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout().addWidget(self.canvas)

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Day", "Week", "Month"])
        self.comboBox.currentTextChanged.connect(self.update_chart)
        self.layout().addWidget(self.comboBox)

        self.update_chart("Day")

    def update_chart(self, period):
        data = FILE_WORKER.getFileList()
        
        dates = []
        emotions = []
        for key, value in data.items():
            dates.append(datetime.strptime(value['date'], "%Y-%m-%d %H:%M:%S"))
            emotions.extend(value['emotion'])

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        if period == "Day":
            dates = [date.date() for date in dates]
            ax.hist(dates, bins=len(set(dates)))
        elif period == "Week":
            dates = [date.isocalendar()[1] for date in dates]
            ax.hist(dates, bins=len(set(dates)))
        elif period == "Month":
            dates = [date.month for date in dates]
            ax.hist(dates, bins=12)

        ax.set_title(f"Number of notes per {period.lower()}")
        self.canvas.draw()