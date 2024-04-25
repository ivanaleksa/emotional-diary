import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow, 
    QWidget, 
    QGridLayout, 
)

from sideBar import SideBar
from fileBar import FileBar
from addButton import AddButton


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Emotional Diary")
        self.setMinimumSize(450, 300)
        self.setStyleSheet("background-color: white;")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self._appUp()

    def _appUp(self):
        layout = QGridLayout()
        layout.addWidget(SideBar().getWidget(), 0, 0, 2, 1)
        layout.addWidget(FileBar().getScrollArea(), 0, 1, 2, 1)
        layout.addWidget(AddButton(), 0, 2, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.setSpacing(0)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 8)
        layout.setColumnStretch(3, 12)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 5)

        self.centralWidget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
