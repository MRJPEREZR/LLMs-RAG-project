# class ConversationRepository:
#     def __init__(self, mongodb_client):
#         self.db = mongodb_client
    
#     async def get_or_create_conversation(self, user_id: str, session_id: str = None):
#         # Logic to find existing or create new conversation
#         pass
    
#     async def add_message(self, conversation_id: str, role: str, content: str):
#         # Add message to MongoDB conversation
#         pass
    
#     async def get_conversation_history(self, conversation_id: str, limit: int = 50):
#         # Retrieve conversation with pagination
#         pass

from app.models.mongo_models import Conversation
from typing import Optional, List
from datetime import datetime, timezone
from uuid import uuid4

class ConversationRepository:
    def __init__(self, db_client):
        self.db_client = db_client
        # If using Beanie ODM, you might not need db_client explicitly
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a single conversation by ID"""
        return await Conversation.get(conversation_id)
    
    async def list_user_conversations(
        self, 
        user_id: str, 
        limit: int = 20, 
        offset: int = 0
    ) -> List[Conversation]:
        """List conversations for a user"""
        return await Conversation.find(
            Conversation.user_id == user_id
        ).sort(-Conversation.updated_at).skip(offset).limit(limit).to_list()
    
    async def create_conversation(
        self, 
        user_id: str, 
        title: Optional[str] = None
    ) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            user_id=user_id,
            title=title or "New Conversation",
            messages=[]
        )
        await conversation.insert()
        return conversation
    
    async def add_message(
        self, 
        conversation_id: str, 
        role: str, 
        content: str
    ) -> dict:
        """Add a message to a conversation"""
        conversation = await self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        
        message = {
            "id": str(uuid4()),
            "role": role,
            "content": content,
            "timestamp": datetime.now(timezone.utc)
        }
        
        conversation.messages.append(message)
        conversation.updated_at = datetime.now(timezone.utc)
        await conversation.save()
        
        return message
    
    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        conversation = await self.get_conversation(conversation_id)
        if conversation:
            await conversation.delete()
            return True
        return False
    
    async def update_title(self, conversation_id: str, title: str) -> Conversation:
        """Update conversation title"""
        conversation = await self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        
        conversation.title = title
        await conversation.save()
        return conversation