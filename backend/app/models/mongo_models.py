from beanie import Document, Indexed
from datetime import datetime, timezone
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    role: str
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Conversation(Document):
    messages: List[Message] = Field(default_factory=list)
    title: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Settings:
        name = "conversations"
        indexes = [
            [("updated_at", -1)],
        ]
    
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)