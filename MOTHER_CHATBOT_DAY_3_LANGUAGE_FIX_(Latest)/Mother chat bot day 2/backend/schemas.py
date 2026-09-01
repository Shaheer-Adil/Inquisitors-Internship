from typing import List, Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=200)
    session_id: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=10000)

class EmotionAnalysis(BaseModel):
    emotion: str
    secondary_emotion: str = "none"
    intent: str
    urgency: str = "normal"
    language: str
    confidence: float

class RetrievedChunk(BaseModel):
    chunk_id: str
    text: str
    metadata: dict
    distance: Optional[float] = None

class ChatResponse(BaseModel):
    session_id: str
    analysis: EmotionAnalysis
    response: str
    retrieved: List[RetrievedChunk] = []
