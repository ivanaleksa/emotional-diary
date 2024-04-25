from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QFrame
)


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

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet(self.scrollAreaStyle)

        filesWidget = QWidget()
        filesLayout = QVBoxLayout(filesWidget)
        filesLayout.setSpacing(0)
        filesLayout.setContentsMargins(0, 0, 0, 0)
        filesLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        filesWidget.setStyleSheet("background: rgb(235, 235, 235); border-radius: 5px;")

        # TODO fill this list with real files
        for i in range(20):
            btn = QPushButton(f"File {i + 1}")
            btn.setStyleSheet(self.fileButtonStyle)
            filesLayout.addWidget(btn)

        self.setWidget(filesWidget)
