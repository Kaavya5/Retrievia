from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Document Schemas ---

class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    message: str

class SummaryRequest(BaseModel):
    document_id: str

class SummaryResponse(BaseModel):
    document_id: str
    summary: str

# --- Chat Schemas ---

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    query: str
    document_id: Optional[str] = None

class SourceChunk(BaseModel):
    text: str
    document_id: str
    score: float

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[SourceChunk]

# --- History Schemas ---

class ChatMessageSchema(BaseModel):
    id: int
    session_id: str
    role: str # "user" or "assistant"
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatSessionSchema(BaseModel):
    id: str
    title: str
    created_at: datetime
    messages: List[ChatMessageSchema] = []

    class Config:
        from_attributes = True
