from app.models.mongo_models import Conversation, Message
from typing import Optional, List
from datetime import datetime, timezone
from uuid import uuid4
from app.core.logger import default_logger as logger
from beanie import PydanticObjectId

class ConversationRepository:
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get a single conversation by ID"""
        try:
            obj_id = PydanticObjectId(conversation_id)
        except ValueError:
            return None
        return await Conversation.get(obj_id)
    
    async def get_conversations(self, limit: int = 100, offset: int = 0, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None) -> List[Conversation]:
        """Get all conversations"""
        query = Conversation.find_all()
        if from_date:
            query = query.where(Conversation.created_at >= from_date)
        if to_date:
            query = query.where(Conversation.created_at <= to_date)
        return await query.skip(offset).limit(limit).to_list()
    
    async def get_or_create_conversation(
        self,
        conversation_id: Optional[str] = None,
        title: Optional[str] = None
    ) -> Conversation:
        """Get an existing conversation or create a new one"""

        if conversation_id:
            conversation = await self.get_conversation(conversation_id)
            if conversation:
                logger.debug("Conversation found!")
                return conversation

        logger.debug("Conversation not found!")
        conversation = await self.create_conversation()

        return conversation

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
        logger.debug("New Conversation created!")
        return conversation
    
    async def add_message(
        self, 
        conversation_id: str, 
        role: str, 
        content: str
    ) -> Message:
        """Add a message to a conversation"""
        conversation = await self.get_conversation(conversation_id)
        if not conversation:
            raise ValueError("Conversation not found")
        
        message = Message(role=role, content=content)
        
        conversation.messages.append(message)
        conversation.updated_at = datetime.now(timezone.utc)
        await conversation.save()
        logger.debug("Message added!")

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