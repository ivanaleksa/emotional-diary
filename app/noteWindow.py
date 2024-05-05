from PyQt6.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QLabel,
    QPushButton,
    QApplication
)

from .fileBar import FILE_WORKER
from .preloaderDialog import LoadingDialog
from ..model_service import TFIDFEmotionalModel


PREDICTION_MODEL = TFIDFEmotionalModel(model_path="emotion_analyser/model/xgboost.model", vectorizer_path="emotion_analyser/model/tfidf_vectorizer.pkl")


class NoteWindow(QWidget):
    windowClosed = pyqtSignal()
    titleChanged = pyqtSignal(str, str)

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

        self.previousTitle = ""

        self.titleField = QLineEdit()
        self.titleField.setPlaceholderText("Title")
        self.titleField.setStyleSheet(self.titleInputStyles)
        self.titleField.editingFinished.connect(self._onTitleChanged)

        self.contentField = QTextEdit()
        self.contentField.setPlaceholderText("Your thoughts here...")
        self.contentField.setStyleSheet(self.contentInputStyles)
        self.contentField.textChanged.connect(self._onContentChanged)

        headerWidget = QWidget()
        self.header = NoteWindowHeader()
        self.header.textChanged.connect(self._predictText)
        self.header.closeRequested.connect(self._onCloseRequested)
        headerWidget.setLayout(self.header)

        self.emLayout = QVBoxLayout()
        self.emLayout.addWidget(headerWidget)
        self.emLayout.addWidget(self.titleField)
        self.emLayout.addWidget(self.contentField)

        self.setLayout(self.emLayout)
    
    def setContent(self, noteTitle: str):
        fileContent = FILE_WORKER.getFileInfo(noteTitle)

        self.titleField.setText(noteTitle)
        self.contentField.setText(fileContent["content"])
        self.header.emotionContainer.setText(", ".join(fileContent["emotion"]))
        self.previousTitle = noteTitle
    
    @pyqtSlot()
    def _onContentChanged(self):
        if self.contentField.toPlainText():
            FILE_WORKER.addNewNote(self.titleField.text(), self.contentField.toPlainText())
    
    @pyqtSlot()
    def _onTitleChanged(self):
        if self.titleField.text() and self.previousTitle != self.titleField.text():
            FILE_WORKER.changeNoteTitle(self.previousTitle, self.titleField.text())

            # if a user change the note's title and then doesn't change content, the previous title will be saves
            # to avoid that, let's save all note again
            FILE_WORKER.addNewNote(self.titleField.text(), self.contentField.toPlainText())
            self.titleChanged.emit(self.previousTitle, self.titleField.text())
            self.previousTitle = self.titleField.text()

    def _onCloseRequested(self):
        self.titleField.setText("")
        self.contentField.setText("")
        self.header.emotionContainer.setText("")

        self.windowClosed.emit()
    
    def _predictText(self, text):
        # TODO: animation doesn't work
        loadingDialog = LoadingDialog(self)
        loadingDialog.show()

        QApplication.processEvents()

        prediction = PREDICTION_MODEL.predict(text)

        loadingDialog.close()

        self.header.emotionContainer.setText(prediction)
        FILE_WORKER.addNewNote(self.titleField.text(), self.contentField.toPlainText(), self.header.emotionContainer.text(), u=True)


class NoteWindowHeader(QHBoxLayout):
    closeRequested = pyqtSignal()
    textChanged = pyqtSignal(str)

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
        self.closeBtn.setIcon(QIcon("emotion_analyser/app/media/close_icon.png"))
        self.closeBtn.setToolTip("Save and Close the note")
        self.closeBtn.setIconSize(QSize(25, 25))
        self.closeBtn.setStyleSheet(self.closeButtonStyles)
        self.closeBtn.clicked.connect(self._closeButtonClicked)

        self.analyseBtn = QPushButton()
        self.analyseBtn.setIcon(QIcon("emotion_analyser/app/media/analyse_icon.png"))
        self.analyseBtn.setToolTip("Analyse the note")
        self.analyseBtn.setIconSize(QSize(25, 25))
        self.analyseBtn.setStyleSheet(self.analyseButtonStyles)
        self.analyseBtn.clicked.connect(self._analyseNoteClicked)

        self.addWidget(self.emotionContainer, 10)
        self.addWidget(self.analyseBtn, 3)
        self.addWidget(self.closeBtn, 1)
    
    def _closeButtonClicked(self):
        self.closeRequested.emit()

    def _analyseNoteClicked(self):
        self.textChanged.emit(self.parent().parent().contentField.toPlainText())
