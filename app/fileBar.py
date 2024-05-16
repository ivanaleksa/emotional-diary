from functools import partial

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QFrame,
    QLabel,
    QMenu,
    QMessageBox,
    QLineEdit
)

from .fileWorker import FileWorker


FILE_WORKER = FileWorker()


class FileBar(QScrollArea):
    openNoteRequested = pyqtSignal(str)

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
        QPushButton::menu-indicator{
              image: none;
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

    menuStyles = """
        QMenu {
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            font-weight: bold;
        }
        QMenu::item:selected {
            background-color: #d3d3d3;
            color: black;
        }
        QMenu::item:pressed {
            background-color: rgb(122, 122, 122);
        }
    """
    searchStyles = """
        QLineEdit {
            background-color: rgb(185, 185, 185);
            border: 1px solid rgb(141, 141, 141);
        }
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet(self.scrollAreaStyle)

        self.searchLayout = QHBoxLayout()
        self.searchLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchField = QLineEdit()
        self.searchField.setPlaceholderText("Search note")
        self.searchField.setStyleSheet(self.searchStyles)
        self.searchField.editingFinished.connect(self._searchTextChanged)

        self.searchLayout.addWidget(self.searchField, 1)
        self.searchLayout.setContentsMargins(0, 0, 0, 5)


        self.filesWidget = QWidget()
        self.filesLayout = QVBoxLayout(self.filesWidget)
        self.filesLayout.setSpacing(0)
        self.filesLayout.setContentsMargins(0, 0, 0, 0)
        self.filesLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.filesWidget.setStyleSheet("background: rgb(235, 235, 235); border-radius: 5px;")

        self.absentFilesLabel = QLabel("There aren't any files yet")
        self.absentFilesLabel.setStyleSheet(self.absentFilesLabelStyles)
        self.absentFilesLabel.setVisible(False)

        self.filesLayout.addLayout(self.searchLayout)
        self.filesLayout.addWidget(self.absentFilesLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        self.showenFiles: list = []
        self.buttons = {}
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
                    btn.setToolTip(f"{files[i]['date']}\n{' ,'.join(files[i]['emotion'])}")
                    
                    menu = QMenu(btn)
                    menu.setStyleSheet(self.menuStyles)

                    openAction = menu.addAction("Open")
                    openAction.triggered.connect(partial(self._openNote, i))

                    deleteAction = menu.addAction("Delete")
                    deleteAction.triggered.connect(partial(self._deleteNote, i))

                    btn.setMenu(menu)

                    self.filesLayout.addWidget(btn)
                    self.showenFiles.append(i)
                    self.buttons[i] = btn
    
    def _deleteNote(self, fileName):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Delete confirmation")
        msgBox.setText(f"Are you sure you want to delete {fileName} note? It'll be irrevocably deleted!")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setDefaultButton(QMessageBox.StandardButton.No)
        
        if msgBox.exec() == QMessageBox.StandardButton.Yes:
            FILE_WORKER.deleteNode(fileName + ".txt")
            del self.showenFiles[self.showenFiles.index(fileName)]
            self.buttons[fileName].deleteLater()

        if len(self.showenFiles) == 0:
            self.absentFilesLabel.setVisible(True)
    
    def _openNote(self, fileName):
        self.openNoteRequested.emit(fileName)

    def onNoteTitleChanged(self, previousTitle, newTitle):
        if previousTitle != "":
            btn = self.buttons.pop(previousTitle)
            self.buttons[newTitle] = btn
            self.showenFiles[self.showenFiles.index(previousTitle)] = newTitle
            btn.setText(newTitle)

            menu = QMenu(btn)
            menu.setStyleSheet(self.menuStyles)

            openAction = menu.addAction("Open")
            openAction.triggered.connect(partial(self._openNote, newTitle))

            deleteAction = menu.addAction("Delete")
            deleteAction.triggered.connect(partial(self._deleteNote, newTitle))

            btn.setMenu(menu)

        self.updateFileList()
    
    def _searchTextChanged(self):
        text = self.searchField.text()

        # Очищаем текущий список файлов
        for i in reversed(range(self.filesLayout.count())):
            widget = self.filesLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Если строка поиска пуста, обновляем список всех файлов
        if not text:
            for file_name in self.showenFiles:
                self.filesLayout.addWidget(self.buttons[file_name])

        # Иначе отображаем только файлы, содержащие введенную подстроку в названии
        for file_name in self.showenFiles:
            if text.lower() in file_name.lower():
                self.filesLayout.addWidget(self.buttons[file_name])
