# schemas/ner_request.py
from pydantic import BaseModel

class NERRequest(BaseModel):
    sentence: str
