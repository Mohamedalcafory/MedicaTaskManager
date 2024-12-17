# app.py
from fastapi import FastAPI
from schemas.ner_request import NERRequest
from schemas.intent_request import IntentRequest
from models.ner_predictor import NERPredictor
from models.intent_predictor import IntentPredictor
import os
from pydantic import BaseModel
from typing import List

# Initialize the FastAPI app
app = FastAPI(
    title="Medical Task Manager API",
    description="API for Named Entity Recognition (NER) and Intent Classification",
    version="1.0.0"
)

# Load the models (Replace these with actual paths to your fine-tuned models)
ner_model_dir = "mohamedalcafory/MedicalTaskManagerNER"
intent_model_dir = "mohamedalcafory/MedicalTaskManager"
ner_predictor = NERPredictor(ner_model_dir)
intent_predictor = IntentPredictor(intent_model_dir)

class NERResponse(BaseModel):
    entities: List[str]  # List of identified entities
# Endpoint for NER
@app.post("/extract_entities/", response_model=NERResponse, tags=["NER"])
async def extract_ner(request: NERRequest):
    """
    Extract entities from the input sentence.
    - **sentence**: The sentence for NER processing.
    """
    entities = ner_predictor.extract_entities(request.sentence)
    return {"entities": entities}

# Response model for Intent Classification
class IntentResponse(BaseModel):
    intent: str  # Identified intent

# Endpoint for intent classification
@app.post("/classify_intent/", response_model=IntentResponse, tags=["Intent Classification"])
async def classify_intent(request: IntentRequest):
    """
    Classify the intent of the input sentence.
    - **sentence**: The sentence for intent classification.
    """
    intent = intent_predictor.extract_intent(request.sentence)
    return {"intent": intent}
