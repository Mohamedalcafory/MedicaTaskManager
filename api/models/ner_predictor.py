# models/ner_predictor.py
from .ner_model import NERModel

class NERPredictor:
    def __init__(self, model_dir: str):
        self.model = NERModel(model_dir)

    def extract_entities(self, sentence: str):
        return self.model.predict(sentence)