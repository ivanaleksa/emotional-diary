import os
import pickle
import requests
import re
from abc import ABC, abstractmethod

import xgboost as xgb
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class AbstractModel(ABC):
    @abstractmethod
    def _validation(self):
        """This method should validate input data and return preprocessed data"""
        pass

    @abstractmethod
    def _preprocessing(self):
        """This method should preprocess data before sending it to a model"""
        pass

    @abstractmethod
    def predict(self):
        """This method recieves data and returns some prediction"""
        pass


class TFIDFEmotionalModel(AbstractModel):
    emotions = {
        0: "sadness",
        1: "joy",
        2: "love",
        3: "anger",
        4: "fear",
        5: "surprise"
    }

    def __init__(self, model_path: str, vectorizer_path: str):
        if self.__check_internet_connection():
            nltk.download('punkt', download_dir="emotion_analyser/model/nltk_data")
            nltk.download('stopwords', download_dir="emotion_analyser/model/nltk_data")
            nltk.download('wordnet', download_dir="emotion_analyser/model/nltk_data")
        else:
            if not all(
                os.path.exists(os.path.join("emotion_analyser/model/nltk_data", filename)) 
                    for filename in ['tokenizers/punkt', 'corpora/stopwords']
            ):
                raise FileNotFoundError("Necessary NLTK data files are missing.")

        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

        self.xgb_model = xgb.XGBClassifier()
        self.xgb_model.load_model(model_path)

        with open(vectorizer_path, "rb") as f:
            self.vectorizer = pickle.load(f)
        
        if self.xgb_model is None:
            raise ValueError("The model wasn't downloaded. Please, check its path")
        if self.vectorizer is None:
            raise ValueError("The text vectorizer wasn't downloaded. Please, check its path")
        
    def __check_internet_connection(self) -> bool:
        try:
            _ = requests.get("http://www.google.com", timeout=1)
            return True
        except requests.ConnectionError:
            return False
    
    def _validation(self, text: str) -> bool:
        if re.match(r'^[a-zA-Z0-9\s.,!?\'\"]+$', text):
            return True
        else:
            return False

    def _preprocessing(self, text: str) -> str:
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens]
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return " ".join(tokens)

    def predict(self, text_input: str) -> str:
        # if not self._validation(text_input):
        #     raise ValueError("Text should contain only: English lettes, punktuation or digits.")
        
        text_input = self._preprocessing(text_input)
        vector = self.vectorizer.transform([text_input])

        return TFIDFEmotionalModel.emotions[self.xgb_model.predict(vector)[0]]


if __name__ == "__main__":
    model = TFIDFEmotionalModel("model/xgboost.model", "model/tfidf_vectorizer.pkl")
    while True:
        s = input("Input your text: ")

        print(model.predict(s))
