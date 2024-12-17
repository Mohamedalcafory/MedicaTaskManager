# models/intent_model.py
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class IntentModel:
    def __init__(self, model_dir: str):
        # Load the model and tokenizer
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.id2intent = self.model.config.id2label  # Maps ids to intents

    def predict(self, sentence: str):
        # Tokenize the input sentence
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=-1).item()
        intent = self.id2intent[predicted_class]
        return intent
