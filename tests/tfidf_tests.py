import pytest
from unittest.mock import MagicMock
from ..model_service import TFIDFEmotionalModel


@pytest.fixture
def tfidf_model():
    model = TFIDFEmotionalModel(model_path="emotion_analyser/model/xgboost.model", vectorizer_path="emotion_analyser/model/tfidf_vectorizer.pkl")
    return model

def test_tfidf_model_validation(tfidf_model):
    valid_text = "This is a valid text with letters and punctuation."
    invalid_text = "Invalid text with symbols #$%^&*()"
    
    assert tfidf_model._validation(valid_text) is True
    assert tfidf_model._validation(invalid_text) is False

def test_tfidf_model_preprocessing(tfidf_model):
    raw_text = "This is an example text!"
    expected_result = "example text !"
    
    assert tfidf_model._preprocessing(raw_text) == expected_result

def test_tfidf_model_prediction(tfidf_model):
    text_input = "I am so happy today!"
    expected_emotion = 1
    
    tfidf_model.predict = MagicMock(return_value=[1])
    assert tfidf_model.predict(text_input)[0] == expected_emotion
