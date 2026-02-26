from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.pydantic_schemas import ConversationSummary, ChatResponse
from app.repositories.conversation_repo import ConversationRepository

from app.dependencies import get_conversation_repo

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("/",response_model=ConversationSummary)
async def create_conversation(
    title: Optional[str] = None,
    conversation_repo: ConversationRepository = Depends(get_conversation_repo)
):
    """
    Create an empty conversation
    """
    conv = await conversation_repo.create_conversation()

    return ConversationSummary(
            id=str(conv.id),
            title=conv.title or "New Conversation",
            message_count=len(conv.messages),
            last_message_at=conv.updated_at,
            created_at=conv.created_at,
            preview=None
        )


@router.get("/", response_model=List[ConversationSummary])
async def list_conversations(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    conversation_repo: ConversationRepository = Depends(get_conversation_repo)
):
    """
    List all conversations for a user with pagination and filtering
    """
    conversations = await conversation_repo.get_conversations(
        limit=limit,
        offset=offset,
        from_date=from_date,
        to_date=to_date
    )
    
    # Add message preview for each conversation
    result = []
    for conv in conversations:
        if conv.messages:
            last_msg = conv.messages[-1]
            preview = last_msg.content[:100] + "..." if len(last_msg.content) > 100 else last_msg.content
        else:
            preview = None
            
        result.append(ConversationSummary(
            id=str(conv.id),
            title=conv.title or "New Conversation",
            message_count=len(conv.messages),
            last_message_at=conv.updated_at,
            created_at=conv.created_at,
            preview=preview
        ))
    
    return result

@router.get("/{conversation_id}", response_model=dict)
async def get_conversation(
    conversation_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    conversation_repo: ConversationRepository = Depends(get_conversation_repo)
):
    """
    Get a specific conversation with paginated messages
    """
    conversation = await conversation_repo.get_conversation(conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "message_count": len(conversation.messages)
    }

@router.put("/{conversation_id}/title")
async def update_conversation_title(
    conversation_id: str,
    title: str = Body(..., embed=True),
    conversation_repo: ConversationRepository = Depends(get_conversation_repo)
):
    """
    Update conversation title
    """
    conversation = await conversation_repo.get_conversation(conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    updated = await conversation_repo.update_title(conversation_id, title)
    
    return {"status": "success", "title": updated.title}

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    conversation_repo: ConversationRepository = Depends(get_conversation_repo),
):
    """
    Delete a conversation
    """
    conversation = await conversation_repo.get_conversation(conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Delete from MongoDB
    await conversation_repo.delete_conversation(conversation_id)
    
    return {"status": "success", "message": "Conversation deleted"}