# models/ner_model.py
from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch

class NERModel:
    def __init__(self, model_dir: str):
        # Load the model and tokenizer
        self.model = AutoModelForTokenClassification.from_pretrained(model_dir)
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.id2label = self.model.config.id2label
        self.label2id = self.model.config.label2id

    def predict(self, sentence: str):
        # Tokenize the input sentence
        inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        logits = outputs.logits
        predicted_ids = torch.argmax(logits, dim=2)
        
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        labels = [self.id2label[i.item()] for i in predicted_ids[0]]
        
        entities = []
        for token, label in zip(tokens, labels):
            if label != 'O':  # Skip non-entities
                entities.append({"token": token, "label": label})
        
        return entities
