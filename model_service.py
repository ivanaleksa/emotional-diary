import pickle
import xgboost as xgb
import nltk
from abc import ABC, abstractmethod

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class AbstractModel(ABC):
    @abstractmethod
    def validation(self):
        """This method should validate input data and return preprocessed data"""
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
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
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
    
    def validation(self, text: str) -> str:
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens]
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return " ".join(tokens)

    def predict(self, text_input: str) -> str:
        text_input = self.validation(text_input)
        vector = self.vectorizer.transform([text_input])

        return TFIDFEmotionalModel.emotions[self.xgb_model.predict(vector)[0]]
    

model = TFIDFEmotionalModel("model/xgboost.model", "model/tfidf_vectorizer.pkl")
print(model.predict("Today is sad, it's raining and I wanna do nothing"))
