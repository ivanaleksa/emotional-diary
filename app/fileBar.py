from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QFrame,
    QLabel
)
from .fileWorker import FileWorker


FILE_WORKER = FileWorker()


class FileBar(QScrollArea):
    fileButtonStyle = """
        QPushButton {
            border: none;
            border-radius: 5px;
            padding: 5px;
            text-align: left;
            color: rgba(117, 117, 117, 1);
            font-weight: bold;
        }
        QPushButton:hover{
            background-color: #d9d9d9;
        }
        QPushButton:pressed{
            background-color: #b3b3b3;
        }
    """

    scrollAreaStyle = """
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

    absentFilesLabelStyles = """
        QLabel {
            color: rgba(117, 117, 117, 1);
            font-weight: bold;
        }
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet(self.scrollAreaStyle)

        self.filesWidget = QWidget()
        self.filesLayout = QVBoxLayout(self.filesWidget)
        self.filesLayout.setSpacing(0)
        self.filesLayout.setContentsMargins(0, 0, 0, 0)
        self.filesLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.filesWidget.setStyleSheet("background: rgb(235, 235, 235); border-radius: 5px;")

        self.absentFilesLabel = QLabel("There aren't any files yet")
        self.absentFilesLabel.setStyleSheet(self.absentFilesLabelStyles)
        self.absentFilesLabel.setVisible(False)
        self.filesLayout.addWidget(self.absentFilesLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.showenFiles: list = []
        self.updateFileList()

        self.setWidget(self.filesWidget)
    
    def updateFileList(self):
        files: dict = FILE_WORKER.getFileList()
        if not files:
            self.absentFilesLabel.setVisible(True)
        else:
            self.absentFilesLabel.setVisible(False)
            for i in files.keys():
                if i not in self.showenFiles:
                    btn = QPushButton(i)
                    btn.setStyleSheet(self.fileButtonStyle)
                    self.filesLayout.addWidget(btn)
                    self.showenFiles.append(i)
