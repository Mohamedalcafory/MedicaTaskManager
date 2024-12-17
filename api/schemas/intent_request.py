# schemas/intent_request.py
from pydantic import BaseModel

class IntentRequest(BaseModel):
    sentence: str
