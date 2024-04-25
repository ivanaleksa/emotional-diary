import os
import json


class FileWorker:
    __instance = None
    notesDictionary: str = "UserNotes"
    metaFile: str = "meta_info.json"

    def __new__(csv, *args, **kwargs):
        if not isinstance(csv.__instance, csv):
            csv.__instance = object.__new__(csv, *args, **kwargs)
        return csv.__instance

    def __init__(self):
        if not os.path.exists(self.notesDictionary):
            os.makedirs(self.notesDictionary)
            with open(self.notesDictionary + "/" + self.metaFile, "w") as f:
                json.dump([], f)
