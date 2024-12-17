# app.py
from fastapi import FastAPI
from schemas.ner_request import NERRequest
from models.ner_predictor import NERPredictor
import os

# Initialize the FastAPI app
app = FastAPI()

# Load the fine-tuned model
model_dir = "medical_ner_bert"
predictor = NERPredictor(model_dir)

# POST endpoint to extract NER
@app.post("/extract_entities/")
async def extract_ner(request: NERRequest):
    entities = predictor.extract_entities(request.sentence)
    return {"entities": entities}
