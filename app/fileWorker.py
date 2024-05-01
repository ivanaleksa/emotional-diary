import os
import glob
import json
from datetime import datetime


class FileWorker:
    __instance = None
    notesDirectory: str = "emotion_analyser/UserNotes"
    metaFile: str = "meta_info.json"
    prohibitedChars: list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|', '+']

    def __new__(csv, *args, **kwargs):
        if not isinstance(csv.__instance, csv):
            csv.__instance = object.__new__(csv, *args, **kwargs)
        return csv.__instance

    def __init__(self):
        if not os.path.exists(self.notesDirectory):
            os.makedirs(self.notesDirectory)
            with open(self.notesDirectory + "/" + self.metaFile, "w") as f:
                json.dump({}, f)
        
        with open(self.notesDirectory + "/" + self.metaFile, "r") as f:
            self.filesInfo: dict = json.load(f)
        
        self._updateMetaInfo()
    
    def _updateMetaInfo(self):
        txtFiles = [os.path.basename(file) for file in glob.glob(os.path.join(self.notesDirectory, "*.txt"))]
        keys_to_delete = []

        for fileTitle in self.filesInfo.keys():
            if fileTitle + ".txt" not in txtFiles:
                keys_to_delete.append(fileTitle)

        for key in keys_to_delete:
            del self.filesInfo[key]
        
        with open(self.notesDirectory + "/" + self.metaFile, "w") as f:
            json.dump(self.filesInfo, f)
    
    def addNewNote(self, title: str, content: str, emotion: str = ""):
        if title != "":
            for c in self.prohibitedChars:
                title = title.replace(c, "U")
            
            self.filesInfo[title] = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "emotion": emotion
                    }

            with open(self.notesDirectory + "/" + title + ".txt", "w", encoding="utf-8") as file:
                file.write(content)
        
            self._updateMetaInfo()

    def deleteNode(self, title: str):
        os.remove(self.notesDirectory + "/" + title)
        self._updateMetaInfo()

    def getFileList(self) -> list[str]:
        return self.filesInfo
    
    def getFileInfo(self, title: str):
        """ Returns a dict with fields: content, date, emotion"""

        for f in self.filesInfo:
            if f["title"] == title:
                with open(self.notesDirectory + "/" + title, "r") as file:
                    content = "".join([line for line in file.readlines()])
                
                return {
                    "content": content,
                    "date": f["date"],
                    "emotion": f["emotion"]
                }
        
        raise FileNotFoundError("There is no such a file")
