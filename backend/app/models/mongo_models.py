from beanie import Document, Indexed
from datetime import datetime, timezone
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.now(timezone.utc)

class Conversation(Document):
    user_id: Annotated[str, Indexed()]
    session_id: Annotated[str, Indexed()]
    messages: List[Message] = Field(default_factory=list)
    title: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "conversations"
        indexes = [
            [("user_id", 1), ("updated_at", -1)],
        ]
    
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)