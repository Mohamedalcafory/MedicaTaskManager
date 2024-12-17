# models/intent_predictor.py
from .intent_model import IntentModel

class IntentPredictor:
    def __init__(self, model_dir: str):
        self.model = IntentModel(model_dir)

    def extract_intent(self, sentence: str):
        return self.model.predict(sentence)
