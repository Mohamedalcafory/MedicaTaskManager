# app.py
from fastapi import FastAPI
from schemas.ner_request import NERRequest
from schemas.intent_request import IntentRequest
from models.ner_predictor import NERPredictor
from models.intent_predictor import IntentPredictor
import os

# Initialize the FastAPI app
app = FastAPI()

# Load the models (Replace these with actual paths to your fine-tuned models)
ner_model_dir = "mohamedalcafory/MedicalTaskManagerNER"
intent_model_dir = "mohamedalcafory/MedicalTaskManager"
ner_predictor = NERPredictor(ner_model_dir)
intent_predictor = IntentPredictor(intent_model_dir)

# Endpoint for NER
@app.post("/extract_entities/")
async def extract_ner(request: NERRequest):
    entities = ner_predictor.extract_entities(request.sentence)
    return {"entities": entities}

# Endpoint for intent classification
@app.post("/classify_intent/")
async def classify_intent(request: IntentRequest):
    intent = intent_predictor.extract_intent(request.sentence)
    return {"intent": intent}
