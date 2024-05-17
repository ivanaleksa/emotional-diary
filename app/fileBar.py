from functools import partial

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon
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
    QLineEdit,
    QDialog,
    QDateEdit
)
from datetime import datetime

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
    buttonStyles = """
        QPushButton {
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover{
            background-color: #d9d9d9;
        }
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet(self.scrollAreaStyle)

        self.searchField = QLineEdit()
        self.searchField.setPlaceholderText("Search note")
        self.searchField.setStyleSheet(self.searchStyles)
        self.searchField.editingFinished.connect(self._searchTextChanged)

        self.sortBtn = QPushButton()
        self.sortBtn.setIcon(QIcon("emotion_analyser/app/media/sort.png"))
        self.sortBtn.setToolTip("Sort notes")
        self.sortBtn.setIconSize(QSize(17, 17))
        self.sortBtn.setStyleSheet(self.buttonStyles)
        self.sortBtn.clicked.connect(self._sortButtonClicked)

        self.filterBtn = QPushButton()
        self.filterBtn.setIcon(QIcon("emotion_analyser/app/media/filter.png"))
        self.filterBtn.setToolTip("Filter notes")
        self.filterBtn.setIconSize(QSize(17, 17))
        self.filterBtn.setStyleSheet(self.buttonStyles)
        self.filterBtn.clicked.connect(self._filterButtonClicked)

        self.searchLayout = QHBoxLayout()
        self.searchLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.searchLayout.addWidget(self.searchField, 5)
        self.searchLayout.addWidget(self.sortBtn, 1)
        self.searchLayout.addWidget(self.filterBtn, 1)
        self.searchLayout.setContentsMargins(0, 0, 25, 5)


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
    
    def _sortButtonClicked(self):
        sortDialog = SortDialog(self)
        sortDialog.sortRequested.connect(self._sortFiles)
        sortDialog.exec()

    def _filterButtonClicked(self):
        filterDialog = FilterDialog(self)
        filterDialog.filterRequested.connect(self._filterFiles)
        filterDialog.exec()
    
    def _sortFiles(self, criterion):
        files = FILE_WORKER.getFileList()
        if criterion == 'alphabet':
            sorted_files = dict(sorted(files.items()))
        elif criterion == 'date':
            sorted_files = dict(sorted(files.items(), key=lambda item: datetime.strptime(item[1]['date'], "%Y-%m-%d %H:%M:%S")))

        self._updateFileListWithNewOrder(sorted_files)

    def _filterFiles(self, start_date, end_date):
        files = FILE_WORKER.getFileList()

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        filtered_files = {k: v for k, v in files.items() if start_date.date() <= datetime.strptime(v['date'], "%Y-%m-%d %H:%M:%S").date() <= end_date.date()}

        self._updateFileListWithNewOrder(filtered_files)

    def _updateFileListWithNewOrder(self, files):
        self.showenFiles = []
        self.buttons = {}

        self.absentFilesLabel.setVisible(False)

        for i in reversed(range(self.filesLayout.count())):
            widget = self.filesLayout.itemAt(i).widget()
            if widget and widget != self.searchField and widget != self.sortBtn and widget != self.filterBtn:
                widget.setParent(None)

        for i in files.keys():
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



class SortDialog(QDialog):
    sortRequested = pyqtSignal(str)

    buttonsStyles = """
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            font-weight: bold;
            padding: 10px 20px;
        }
        QPushButton:hover {
            background-color: #d3d3d3;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Sort notes")
        self.setLayout(QVBoxLayout())

        alphabetBtn = QPushButton("Alphabetically")
        alphabetBtn.clicked.connect(self._sortAlphabetically)

        dateBtn = QPushButton("By Date")
        dateBtn.clicked.connect(self._sortByDate)

        self.layout().addWidget(alphabetBtn)
        self.layout().addWidget(dateBtn)

        alphabetBtn.setStyleSheet(self.buttonsStyles)
        dateBtn.setStyleSheet(self.buttonsStyles)

    def _sortAlphabetically(self):
        self.sortRequested.emit('alphabet')
        self.accept()

    def _sortByDate(self):
        self.sortRequested.emit('date')
        self.accept()


class FilterDialog(QDialog):
    filterRequested = pyqtSignal(str, str)

    buttonStyles = """
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            font-weight: bold;
            padding: 10px 20px;
        }
        QPushButton:hover {
            background-color: #d3d3d3;
        }
    """

    dateStyles = """
        QDateEdit {
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            font-weight: bold;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Filter notes")
        self.setLayout(QVBoxLayout())

        self.startDateEdit = QDateEdit()
        self.endDateEdit = QDateEdit()

        startDateLabel = QLabel("Start Date:")
        endDateLabel = QLabel("End Date:")
        confirmBtn = QPushButton("Filter")
        confirmBtn.clicked.connect(self._filterNotes)

        startDateLayout = QHBoxLayout()
        startDateLayout.addWidget(startDateLabel)
        startDateLayout.addWidget(self.startDateEdit)

        endDateLayout = QHBoxLayout()
        endDateLayout.addWidget(endDateLabel)
        endDateLayout.addWidget(self.endDateEdit)

        confirmLayout = QHBoxLayout()
        confirmLayout.addWidget(confirmBtn)

        self.layout().addLayout(startDateLayout)
        self.layout().addLayout(endDateLayout)
        self.layout().addLayout(confirmLayout)

        # Применим стилизацию к кнопкам
        confirmBtn.setStyleSheet(self.buttonStyles)

        # Применим стилизацию к меткам
        startDateLabel.setStyleSheet("font-weight: bold;")
        endDateLabel.setStyleSheet("font-weight: bold;")

        # Применим стилизацию к полям ввода дат
        self.startDateEdit.setStyleSheet(self.dateStyles)
        self.endDateEdit.setStyleSheet(self.dateStyles)

    def _filterNotes(self):
        start_date = self.startDateEdit.date().toString("yyyy-MM-dd")
        end_date = self.endDateEdit.date().toString("yyyy-MM-dd")
        self.filterRequested.emit(start_date, end_date)
        self.accept()
