from pydantic import BaseModel

class EmotionResponse(BaseModel):
    status: str
    emotion:str
    confidence: float