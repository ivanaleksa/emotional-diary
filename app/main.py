import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow, 
    QWidget, 
    QGridLayout,
)

from .sideBar import SideBar
from .fileBar import FileBar
from .addButton import AddButton
from .noteWindow import NoteWindow
from .statisticWindow import AnalyticsWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Emotional Diary")
        self.setMinimumSize(450, 300)
        self.resize(1000, 700)
        self.setStyleSheet("background-color: white;")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self._appUp()

    def _appUp(self):
        self.sideBar = SideBar()
        self.fileBar = FileBar()
        self.analyticsWidget = AnalyticsWidget()

        self.addButton = AddButton()
        self.noteWindow = NoteWindow()
        self.noteWindow.header.closeRequested.connect(self.noteWindow._onCloseRequested)
        self.noteWindow.windowClosed.connect(self._onNoteWindowClosed)
        self.noteWindow.titleChanged.connect(self._onNoteTitleChanged)
        self.noteWindow.setVisible(False)

        self.layoutMain = QGridLayout()
        self.layoutMain.addWidget(self.sideBar, 0, 0, 2, 1)
        self.layoutMain.addWidget(self.fileBar, 0, 1, 2, 1)
        self.layoutMain.addWidget(self.analyticsWidget, 0, 1, 2, 1)
        self.layoutMain.addWidget(self.addButton, 0, 2, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layoutMain.addWidget(self.noteWindow, 0, 2, 2, 2)

        self.layoutMain.setSpacing(0)
        self.layoutMain.setColumnStretch(0, 1)
        self.layoutMain.setColumnStretch(1, 6)
        self.layoutMain.setColumnStretch(2, 8)
        self.layoutMain.setColumnStretch(3, 12)
        self.layoutMain.setRowStretch(0, 1)
        self.layoutMain.setRowStretch(1, 5)

        self.centralWidget.setLayout(self.layoutMain)

        self.addButton.clicked.connect(self._onAddButtonClicked)
        self.fileBar.openNoteRequested.connect(self._openNote)

        self.sideBar.filesButton.clicked.connect(self._showFileBar)
        self.sideBar.analiticsButton.clicked.connect(self._showAnalyticsWidget)

        self.analyticsWidget.setVisible(False)

    def _showFileBar(self):
        self.layoutMain.setSpacing(0)
        self.layoutMain.setColumnStretch(0, 1)
        self.layoutMain.setColumnStretch(1, 6)
        self.layoutMain.setColumnStretch(2, 8)
        self.layoutMain.setColumnStretch(3, 12)
        self.layoutMain.setRowStretch(0, 1)
        self.layoutMain.setRowStretch(1, 5)

        self.fileBar.setVisible(True)
        self.addButton.setVisible(True)
        self.noteWindow.setVisible(False)
        self.analyticsWidget.setVisible(False)

    def _showAnalyticsWidget(self):
        self.layoutMain.setSpacing(0)
        self.layoutMain.setColumnStretch(0, 1)
        self.layoutMain.setColumnStretch(1, 18)
        self.layoutMain.setColumnStretch(2, 0)
        self.layoutMain.setColumnStretch(3, 0)
        self.layoutMain.setRowStretch(0, 1)
        self.layoutMain.setRowStretch(1, 5)

        self.fileBar.setVisible(False)
        self.addButton.setVisible(False)
        self.noteWindow.setVisible(False)
        self.analyticsWidget.setVisible(True)

    def _onAddButtonClicked(self):
        self.addButton.setVisible(False)
        self.noteWindow.setVisible(True)

        self.noteWindow.previousTitle = ""

    def _onNoteWindowClosed(self):
        self.noteWindow.setVisible(False)
        self.addButton.setVisible(True)
    
    def _openNote(self, fileName):
        self.addButton.setVisible(False)
        self.noteWindow.setVisible(True)

        self.noteWindow.setContent(fileName)

    def _onNoteTitleChanged(self, old, new):
        self.fileBar.onNoteTitleChanged(old, new)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
