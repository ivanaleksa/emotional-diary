import os
import glob
import json
from datetime import datetime


class FileWorker:
    __instance = None
    notesDirectory: str = "UserNotes"
    metaFile: str = "meta_info.json"

    def __new__(csv, *args, **kwargs):
        if not isinstance(csv.__instance, csv):
            csv.__instance = object.__new__(csv, *args, **kwargs)
        return csv.__instance

    def __init__(self):
        if not os.path.exists(self.notesDirectory):
            os.makedirs(self.notesDirectory)
            with open(self.notesDirectory + "/" + self.metaFile, "w") as f:
                json.dump([], f)
        
        with open(self.notesDirectory + "/" + self.metaFile, "r") as f:
            self.filesInfo: list = json.load(f)
        
        self._updateMetaInfo()
    
    def _updateMetaInfo(self):
        txtFiles = [os.path.basename(file) for file in glob.glob(os.path.join(self.notesDirectory, "*.txt"))]

        for i in range(len(self.filesInfo) - 1, -1, -1):
            fileInfo = self.filesInfo[i]
            if fileInfo["title"] not in txtFiles:
                del self.filesInfo[i]
        
        with open(self.notesDirectory + "/" + self.metaFile, "w") as f:
            json.dump(self.filesInfo, f)
    
    def addNewNote(self, title: str, content: str, emotion: str = ""):
        if os.path.exists(self.notesDirectory + "/" + title + ".txt"):
            raise FileExistsError("There is already a file with this title")
        
        self.filesInfo.append({
            "title": title,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "emotion": emotion
        })

        with open(self.notesDirectory + "/" + title + ".txt", "w", encoding="utf-8") as file:
            file.write(content)
        
        self._updateMetaInfo()

    def deleteNode(self, title: str):
        os.remove(self.notesDirectory + "/" + title)
        self._updateMetaInfo()

    def getFileList(self) -> list[str]:
        return [f["title"] for f in self.filesInfo]
    
    def getFileInfo(self, title: str):
        """ Returns a dict with fields: title, content, date, emotion"""

        for f in self.filesInfo:
            if f["title"] == title:
                with open(self.notesDirectory + "/" + title, "r") as file:
                    content = "".join([line for line in file.readlines()])
                
                return {
                    "title": f["title"],
                    "content": content,
                    "date": f["date"],
                    "emotion": f["emotion"]
                }
        
        raise FileNotFoundError("There is no such a file")
