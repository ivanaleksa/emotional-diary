from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QLabel,
    QPushButton
)

from fileBar import FILE_WORKER


class NoteWindow(QWidget):
    windowClosed = pyqtSignal()

    titleInputStyles = """
        QLineEdit {
            border: none; 
            background: transparent; 
            color: black;
            font-size: 24px;
            font-weight: bold;
        }
        QLineEdit:hover {
            border: 1px solid rgb(0, 215, 157);
            border-radius: 5px;
        }
    """

    contentInputStyles = """
        QTextEdit {
            border: none; 
            background: transparent; 
            color: black;
            font-size: 14px;
        }
        QTextEdit:hover {
            border: 1px solid rgb(0, 215, 157);
            border-radius: 5px;
        }

        QScrollBar:vertical {
            background: lightgray;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: none;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical {
            background: none;
        }
        QScrollBar::sub-line:vertical {
            background: none;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.titleField = QLineEdit()
        self.titleField.setPlaceholderText("Title")
        self.titleField.setStyleSheet(self.titleInputStyles)

        self.contentField = QTextEdit()
        self.contentField.setPlaceholderText("Your thoughts here...")
        self.contentField.setStyleSheet(self.contentInputStyles)
        self.contentField.textChanged.connect(self._onContentChanged)

        headerWidget = QWidget()
        self.header = NoteWindowHeader()
        self.header.closeRequested.connect(self._onCloseRequested)
        headerWidget.setLayout(self.header)

        self.emLayout = QVBoxLayout()
        self.emLayout.addWidget(headerWidget)
        self.emLayout.addWidget(self.titleField)
        self.emLayout.addWidget(self.contentField)

        self.setLayout(self.emLayout)
    
    def _onContentChanged(self):
        if self.contentField.toPlainText():
            FILE_WORKER.addNewNote(self.titleField.text(), self.contentField.toPlainText())

    def _onCloseRequested(self):
        self.titleField.setText("")
        self.contentField.setText("")
        self.header.emotionContainer.setText("")

        self.windowClosed.emit()


class NoteWindowHeader(QHBoxLayout):
    closeRequested = pyqtSignal()

    buttonStyles = """
        QPushButton {
            border: none;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover{
            background-color: #d9d9d9;
        }
    """
    closeButtonStyles = buttonStyles + """
        QPushButton:pressed{
            background-color: #CA5151;
        }"""
    analyseButtonStyles = buttonStyles + """
        QPushButton:pressed{
            background-color: #75FF75;
        }"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.emotionContainer = QLabel()

        self.closeBtn = QPushButton()
        self.closeBtn.setIcon(QIcon("app/media/close_icon.png"))
        self.closeBtn.setIconSize(QSize(25, 25))
        self.closeBtn.setStyleSheet(self.closeButtonStyles)
        self.closeBtn.clicked.connect(self._closeButtonClicked)

        self.analyseBtn = QPushButton()
        self.analyseBtn.setIcon(QIcon("app/media/analyse_icon.png"))
        self.analyseBtn.setIconSize(QSize(25, 25))
        self.analyseBtn.setStyleSheet(self.analyseButtonStyles)

        self.addWidget(self.emotionContainer, 10)
        self.addWidget(self.analyseBtn, 3)
        self.addWidget(self.closeBtn, 1)
    
    def _closeButtonClicked(self):
        self.closeRequested.emit()