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

        titleField = QLineEdit()
        titleField.setPlaceholderText("Title")
        titleField.setStyleSheet(self.titleInputStyles)

        contentField = QTextEdit()
        contentField.setPlaceholderText("Your thoughts here...")
        contentField.setStyleSheet(self.contentInputStyles)
        contentField.textChanged.connect(self._onTextChanged)

        headerWidget = QWidget()
        self.header = NoteWindowHeader()
        self.header.closeRequested.connect(self._onCloseRequested)
        headerWidget.setLayout(self.header)

        layout = QVBoxLayout()
        layout.addWidget(headerWidget)
        layout.addWidget(titleField)
        layout.addWidget(contentField)

        self.setLayout(layout)
    
    def _onTextChanged(self):
        # TODO: this methis is needed for automate saving of a document
        pass

    def _onCloseRequested(self):
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

        emotionContainer = QLabel("Some emotion here")

        closeBtn = QPushButton()
        closeBtn.setIcon(QIcon("app/media/close_icon.png"))
        closeBtn.setIconSize(QSize(25, 25))
        closeBtn.setStyleSheet(self.closeButtonStyles)
        closeBtn.clicked.connect(self._closeButtonClicked)

        analyseBtn = QPushButton()
        analyseBtn.setIcon(QIcon("app/media/analyse_icon.png"))
        analyseBtn.setIconSize(QSize(25, 25))
        analyseBtn.setStyleSheet(self.analyseButtonStyles)

        self.addWidget(emotionContainer, 10)
        self.addWidget(analyseBtn, 3)
        self.addWidget(closeBtn, 1)
    
    def _closeButtonClicked(self):
        self.closeRequested.emit()
