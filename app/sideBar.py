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

        """ Set all buttons' settings """
        filesButton, analiticsButton = QPushButton(), QPushButton()
        filesButton.setToolTip("Files")
        analiticsButton.setToolTip("Analitics")
        filesButton.setIcon(QIcon("app/media/files_icon.png"))
        analiticsButton.setIcon(QIcon("app/media/analytics_icon.png"))
        filesButton.setIconSize(QSize(25, 25))
        analiticsButton.setIconSize(QSize(25, 25))
        filesButton.setStyleSheet(self.buttonStyle)
        analiticsButton.setStyleSheet(self.buttonStyle)

        sideBarLayout = QVBoxLayout()
        self.setLayout(sideBarLayout)
        sideBarLayout.addWidget(analiticsButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        sideBarLayout.addWidget(filesButton, alignment=Qt.AlignmentFlag.AlignHCenter)
