from app.models.mongo_models import Conversation
from typing import Optional, List
from datetime import datetime, timezone
from uuid import uuid4

class ConversationRepository:
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a single conversation by ID"""
        return await Conversation.get(conversation_id)
    
    async def get_conversations(self, limit: int = 100, offset: int = 0, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None) -> List[Conversation]:
        """Get all conversations"""
        query = Conversation.find_all()
        if from_date:
            query = query.where(Conversation.created_at >= from_date)
        if to_date:
            query = query.where(Conversation.created_at <= to_date)
        return await query.skip(offset).limit(limit).to_list()
    
    async def create_conversation(
        self, 
        title: Optional[str] = None
    ) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
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