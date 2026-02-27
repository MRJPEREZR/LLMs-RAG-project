from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation_id: Optional[str] = None
    stream: bool = False
    use_rag: bool = True
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    metadata: Optional[dict] = {}

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    timestamp: datetime
    sources: Optional[List[dict]] = None
    tokens_used: Optional[int] = None
    processing_time: Optional[float] = None

class StreamChunk(BaseModel):
    chunk: str
    finished: bool
    message_id: Optional[str] = None

class ConversationSummary(BaseModel):
    id: str
    title: str
    message_count: int
    last_message_at: datetime
    created_at: datetime
    preview: Optional[str]  # Last message preview