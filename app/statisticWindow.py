import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QDateEdit,
    QLabel,
    QHBoxLayout
)
from PyQt6.QtCore import QDate
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
        self.comboBox.currentTextChanged.connect(self.update_inputs)
        self.layout().addWidget(self.comboBox)

        self.dateEdit = QDateEdit()
        self.dateLabel = QLabel("Select Date:")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setVisible(True)

        self.weekDateEdit = QDateEdit()
        self.weekLabel = QLabel("Select Week:")
        self.weekDateEdit.setCalendarPopup(True)
        self.weekDateEdit.setVisible(False)
        self.weekLabel.setVisible(False)

        self.monthDateEdit = QDateEdit()
        self.monthDateEdit.setCalendarPopup(True)
        self.monthLabel = QLabel("Select Month:")
        self.monthDateEdit.setVisible(False)
        self.monthLabel.setVisible(False)

        self.inputLayout = QHBoxLayout()
        self.inputLayout.addWidget(self.dateLabel)
        self.inputLayout.addWidget(self.dateEdit)
        self.inputLayout.addWidget(self.weekLabel)
        self.inputLayout.addWidget(self.weekDateEdit)
        self.inputLayout.addWidget(self.monthLabel)
        self.inputLayout.addWidget(self.monthDateEdit)
        self.layout().addLayout(self.inputLayout)

        self.dateEdit.dateChanged.connect(self.update_chart)
        self.weekDateEdit.dateChanged.connect(self.update_chart)
        self.monthDateEdit.dateChanged.connect(self.update_chart)

        self.update_chart()

    def update_inputs(self, period):
        self.dateEdit.setVisible(period == "Day")
        self.dateLabel.setVisible(period == "Day")
        self.weekDateEdit.setVisible(period == "Week")
        self.weekLabel.setVisible(period == "Week")
        self.monthDateEdit.setVisible(period == "Month")
        self.monthLabel.setVisible(period == "Month")
        self.update_chart()

    def update_chart(self):
        period = self.comboBox.currentText()
        selected_date = self.dateEdit.date().toPyDate() if period == "Day" else None
        selected_week_date = self.weekDateEdit.date().toPyDate() if period == "Week" else None
        selected_month_date = self.monthDateEdit.date().toPyDate() if period == "Month" else None
        selected_month = selected_month_date.month if period == "Month" else None
        selected_year = selected_month_date.year if period == "Month" else None

        data = FILE_WORKER.getFileList()

        dates = []
        emotions = []
        for key, value in data.items():
            date = datetime.strptime(value['date'], "%Y-%m-%d %H:%M:%S")
            if period == "Day" and date.date() == selected_date:
                dates.append(date)
                emotions.append(value['emotion'])
            elif period == "Week" and date.isocalendar()[1] == selected_week_date.isocalendar()[1] and date.year == selected_week_date.year:
                dates.append(date)
                emotions.append(value['emotion'])
            elif period == "Month" and date.month == selected_month and date.year == selected_year and date.year == selected_month_date.year:
                dates.append(date)
                emotions.append(value['emotion'])

        emotion_counts = {emotion: 0 for emotion in ["anger", "fear", "joy", "sadness", "surprise", "love"]}
        for emotion_list in emotions:
            for emotion in emotion_list:
                if emotion in emotion_counts:
                    emotion_counts[emotion] += 1

        self.figure.clear()

        ax = self.figure.add_subplot(111)
        colors = ["#FF5733", "#C70039", "#FFC300", "#DAF7A6", "#581845", "#900C3F"]
        bar_positions = list(range(len(emotion_counts)))
        bar_heights = list(emotion_counts.values())
        bar_colors = colors[:len(emotion_counts)]

        bars = ax.bar(bar_positions, bar_heights, color=bar_colors)

        ax.set_xticks(bar_positions)
        ax.set_xticklabels(emotion_counts.keys())
        ax.set_title(f"Notes count per {period.lower()}")
        self.canvas.draw()
