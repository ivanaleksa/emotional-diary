from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QPushButton,
)

class SideBar(QWidget):
    buttonStyle = """
        QPushButton {
            border: none;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover{
            background-color: #d9d9d9;
        }
        QPushButton:pressed{
            background-color: #b3b3b3;
        }
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.filesButton = QPushButton()
        self.analiticsButton = QPushButton()
        self.filesButton.setToolTip("Files")
        self.analiticsButton.setToolTip("Analytics")
        self.filesButton.setIcon(QIcon("emotion_analyser/app/media/files_icon.png"))
        self.analiticsButton.setIcon(QIcon("emotion_analyser/app/media/analytics_icon.png"))
        self.filesButton.setIconSize(QSize(25, 25))
        self.analiticsButton.setIconSize(QSize(25, 25))
        self.filesButton.setStyleSheet(self.buttonStyle)
        self.analiticsButton.setStyleSheet(self.buttonStyle)

        sideBarLayout = QVBoxLayout()
        self.setLayout(sideBarLayout)
        sideBarLayout.addWidget(self.analiticsButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        sideBarLayout.addWidget(self.filesButton, alignment=Qt.AlignmentFlag.AlignHCenter)

