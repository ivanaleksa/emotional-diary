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
        self.addButton = AddButton()
        self.noteWindow = NoteWindow()
        self.noteWindow.header.closeRequested.connect(self.noteWindow._onCloseRequested)
        self.noteWindow.windowClosed.connect(self._onNoteWindowClosed)
        self.noteWindow.titleChanged.connect(self._onNoteTitleChanged)
        self.noteWindow.setVisible(False)

        layout = QGridLayout()
        layout.addWidget(self.sideBar, 0, 0, 2, 1)
        layout.addWidget(self.fileBar, 0, 1, 2, 1)
        layout.addWidget(self.addButton, 0, 2, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.noteWindow, 0, 2, 2, 2)

        layout.setSpacing(0)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 8)
        layout.setColumnStretch(3, 12)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 5)

        self.centralWidget.setLayout(layout)

        self.addButton.clicked.connect(self._onAddButtonClicked)
        self.fileBar.openNoteRequested.connect(self._openNote)  # connect open note action from file bar class

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
