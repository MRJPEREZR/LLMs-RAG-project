from app.repositories.conversation_repo import ConversationRepository
from app.databases.mongodb import init_mongodb
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

async def get_conversation_repo():
    try:
        db_client = await init_mongodb()
        repo = ConversationRepository()
        
        logger.debug("ConversationRepository created successfully")
        
        return repo
    except Exception as e:
        logger.error(f"Failed to create ConversationRepository: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Database connection failed"
        )