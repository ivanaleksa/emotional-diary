from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QBrush, QColor, QFont
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QDateEdit,
    QLabel,
    QHBoxLayout,
    QCalendarWidget
)
from .fileWorker import FileWorker

FILE_WORKER = FileWorker()


class AnalyticsWidget(QWidget):
    combo_box_style = """
    QComboBox {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        padding: 4px;
        font-size: 14px;
    }
    """
    label_style = """
    QLabel {
        font-size: 18px;
        color: black;
        font-weight: bold;
    }
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setLayout(QVBoxLayout())
        calendar = CalendarWidget()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout().addWidget(self.canvas)

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Day", "Week", "Month"])
        self.comboBox.currentTextChanged.connect(self.update_inputs)
        self.layout().addWidget(self.comboBox)

        self.dateEdit = QDateEdit()
        self.dateEdit.setDate(QDate.currentDate())
        self.dateLabel = QLabel("Select Date:")
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setVisible(True)
        self.dateEdit.setCalendarWidget(CalendarWidget())

        self.weekDateEdit = QDateEdit()
        self.weekDateEdit.setDate(QDate.currentDate())
        self.weekLabel = QLabel("Select Week:")
        self.weekDateEdit.setCalendarPopup(True)
        self.weekDateEdit.setVisible(False)
        self.weekLabel.setVisible(False)
        self.weekDateEdit.setCalendarWidget(CalendarWidget())

        self.monthDateEdit = QDateEdit()
        self.monthDateEdit.setDate(QDate.currentDate())
        self.monthDateEdit.setCalendarPopup(True)
        self.monthDateEdit.setCalendarWidget(CalendarWidget())
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

        self.dateLabel.setStyleSheet(self.label_style)
        self.weekLabel.setStyleSheet(self.label_style)
        self.monthLabel.setStyleSheet(self.label_style)
        self.comboBox.setStyleSheet(self.combo_box_style)

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
            elif period == "Month" and date.month == selected_month and date.year == selected_year:
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


class CalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("color: black;")
        self.setStyleSheet("""
        QToolButton {
            color: black;
        }
        #qt_calendar_prevmonth, #qt_calendar_nextmonth{
            qproperty-iconSize: 0px
        }
        QCalendarWidget QTableView {
                selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                            stop: 0 rgba(57, 128, 233, 255),
                            stop: 1 rgba(0, 255, 68, 255));
            }
        """)
    
        self.setGridVisible(True)

        saturday_format = self.weekdayTextFormat(Qt.DayOfWeek.Saturday)
        saturday_format.setForeground(QBrush(QColor(Qt.GlobalColor.black)))
        saturday_format.setFontWeight(QFont.Weight.Bold)
        self.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, saturday_format)
        
        sunday_format = self.weekdayTextFormat(Qt.DayOfWeek.Sunday)
        sunday_format.setForeground(QBrush(QColor(Qt.GlobalColor.black)))
        sunday_format.setFontWeight(QFont.Weight.Bold)
        self.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, sunday_format)
