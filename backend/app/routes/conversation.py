from fastapi import APIRouter, HTTPException, Depends, Query, Body
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.pydantic_schemas import ConversationSummary, MessageResponse
from app.repositories.conversation_repo import ConversationRepository
from app.repositories.vector_repo import VectorRepository

from app.dependencies import get_conversation_repo, get_vector_repo

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.get("/", response_model=List[ConversationSummary])
async def list_conversations(
    user_id: str = Query(..., description="User ID"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    conversation_repo: ConversationRepository = Depends(get_conversation_repo)
):
    """
    List all conversations for a user with pagination and filtering
    """
    conversations = await conversation_repo.list_user_conversations(
        user_id=user_id,
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
    user_id: str = Query(...),
    include_messages: bool = Query(True),
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
    
    if conversation.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if include_messages:
        # Paginate messages
        start = (page - 1) * page_size
        end = start + page_size
        messages = conversation.messages[start:end]
        
        # Convert to response model
        message_responses = [
            MessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                timestamp=msg.timestamp,
                tokens=msg.tokens,
                feedback=msg.feedback
            ) for msg in messages
        ]
        
        return {
            "conversation": {
                "id": str(conversation.id),
                "title": conversation.title,
                "created_at": conversation.created_at,
                "updated_at": conversation.updated_at,
                "total_messages": len(conversation.messages),
                "total_tokens": conversation.total_tokens,
                "metadata": conversation.metadata
            },
            "messages": message_responses,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_pages": (len(conversation.messages) + page_size - 1) // page_size,
                "total_messages": len(conversation.messages)
            }
        }
    
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
    user_id: str = Body(...),
    conversation_repo: ConversationRepository = Depends(get_conversation_repo)
):
    """
    Update conversation title
    """
    conversation = await conversation_repo.get_conversation(conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if conversation.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    updated = await conversation_repo.update_title(conversation_id, title)
    
    return {"status": "success", "title": updated.title}

# @router.delete("/{conversation_id}")
# async def delete_conversation(
#     conversation_id: str,
#     user_id: str = Body(...),
#     background_tasks: BackgroundTasks,
#     conversation_repo: ConversationRepository = Depends(),
#     vector_repo: VectorRepository = Depends(get_vector_repo)
# ):
#     """
#     Delete a conversation and optionally its vector embeddings
#     """
#     conversation = await conversation_repo.get_conversation(conversation_id)
    
#     if not conversation:
#         raise HTTPException(status_code=404, detail="Conversation not found")
    
#     if conversation.user_id != user_id:
#         raise HTTPException(status_code=403, detail="Access denied")
    
#     # Delete from MongoDB
#     await conversation_repo.delete_conversation(conversation_id)
    
#     # Optionally delete associated embeddings from Milvus
#     background_tasks.add_task(
#         vector_repo.delete_conversation_embeddings,
#         conversation_id=conversation_id
#     )
    
#     return {"status": "success", "message": "Conversation deleted"}