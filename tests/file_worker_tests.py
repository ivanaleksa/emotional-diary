import pytest
from unittest.mock import MagicMock, patch, mock_open
from ..app.fileWorker import FileWorker


@pytest.fixture
def file_worker():
    return FileWorker()

@patch('emotion_analyser.app.fileWorker.os.path.exists')
@patch('emotion_analyser.app.fileWorker.os.makedirs')
@patch('emotion_analyser.app.fileWorker.open', new_callable=mock_open, read_data='{}')
def test_file_worker_init(mock_open, mock_makedirs, mock_exists):
    mock_exists.side_effect = [False, True]
    worker = FileWorker()
    
    mock_makedirs.assert_called_once()
    mock_open.assert_called_with("emotion_analyser/UserNotes/meta_info.json", "w", encoding="utf-8")

def test_file_worker_add_new_note():
    worker = FileWorker()
    worker.addNewNote = MagicMock()
    worker._updateMetaInfo = MagicMock()
    
    title = "TestNote"
    content = "This is a test note."
    emotion = ["happy"]
    
    worker.addNewNote(title, content, emotion)
    worker.addNewNote.assert_called_with(title, content, emotion)

def test_file_worker_get_file_info(file_worker):
    with patch('emotion_analyser.app.fileWorker.open', mock_open(read_data="Test content")):
        file_worker.filesInfo = {
            "TestNote": {
                "date": "2024-07-21 16:00:00",
                "emotion": ["happy"]
            }
        }
        file_info = file_worker.getFileInfo("TestNote")
        assert file_info["content"] == "Test content"
        assert file_info["date"] == "2024-07-21 16:00:00"
        assert file_info["emotion"] == ["happy"]
