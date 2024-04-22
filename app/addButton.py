from PyQt6.QtWidgets import (
    QPushButton,
)


class AddButton:
    addButtonStyle = """
        QPushButton {
            border: none;
            border-radius: 37px;
            font-weight: bold;
            font-size: 25px;
            color: white;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(0, 255, 0, 255),
                                stop:1 rgba(51, 102, 255, 255));
        }
        QPushButton:hover {
            color: black;
        }
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(0, 255, 0, 255),
                                stop:1 rgba(204, 0, 204, 255));
        }
    """

    def __init__(self) -> None:
        self.newNoteButton = QPushButton()
        self.newNoteButton.setText("+")
        self.newNoteButton.setFixedSize(75, 75)
        self.newNoteButton.setStyleSheet(self.addButtonStyle)

    def getAddButton(self) -> QPushButton:
        return self.newNoteButton
