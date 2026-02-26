from fastapi import APIRouter, HTTPException, Depends
from app.repositories.conversation_repo import ConversationRepository
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService
from app.models.pydantic_schemas import ChatRequest, ChatResponse

from app.dependencies import get_conversation_repo, get_rag_service, get_llm_service 

from app.core.logger import default_logger as logger

router = APIRouter(prefix="/chats", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    conv_repo: ConversationRepository = Depends(get_conversation_repo),
    rag_service: RAGService = Depends(get_rag_service),
    llm_service: LLMService = Depends(get_llm_service)
):
    # 1. Get or create conversation from MongoDB
    conversation = await conv_repo.get_or_create_conversation(request.conversation_id)
    
    # 2. Save user message to MongoDB immediately
    user_message = await conv_repo.add_message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    
    # 3. If RAG is enabled, search Milvus for relevant context
    if request.use_rag:
        assistant_response = await rag_service.ask(query=request.message, top_k= 5)
        content = assistant_response['answer']
        sources = assistant_response['sources']
    else:
        assistant_response = await llm_service.chat(prompt=request.message)
        content = assistant_response
        sources = {}
    
    # 5. Save assistant response to MongoDB
    assistant_message = await conv_repo.add_message(
        conversation_id=conversation.id,
        role="assistant",
        content=content
    )

    logger.debug(f"conversation_id {conversation.id}")
    logger.debug(f"message_id {conversation.id}")
    logger.debug(f"content {content}")
    logger.debug(f"sources {sources}")
    
    return ChatResponse(
        message_id=assistant_message.id,
        message=content,
        conversation_id=conversation.id,
        sources=sources
    )