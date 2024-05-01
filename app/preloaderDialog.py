from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtGui import QMovie

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowModality(Qt.WindowModality.WindowModal)

        layout = QVBoxLayout(self)
        self.loadingLabel = QLabel(self)
        self.loadingMovie = QMovie("emotion_analyser/app/media/preloader.gif")
        self.loadingLabel.setMovie(self.loadingMovie)
        layout.addWidget(self.loadingLabel, alignment=Qt.AlignmentFlag.AlignCenter)

    def showEvent(self, event):
        self.loadingMovie.start()
        super().showEvent(event)

    def hideEvent(self, event):
        self.loadingMovie.stop()
        super().hideEvent(event)
