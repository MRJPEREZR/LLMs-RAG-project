from fastapi import APIRouter, HTTPException, Depends
from app.repositories.conversation_repo import ConversationRepository
from app.repositories.vector_repo import VectorRepository
from app.services.rag_service import RAGService
from app.models.pydantic_schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    conv_repo: ConversationRepository = Depends(),
    vector_repo: VectorRepository = Depends(),
    rag_service: RAGService = Depends()
):
    # 1. Get or create conversation from MongoDB
    conversation = await conv_repo.get_or_create_conversation(
    )
    
    # 2. Save user message to MongoDB immediately
    user_message = await conv_repo.add_message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    
    # 3. If RAG is enabled, search Milvus for relevant context
    # context = None
    # if request.use_rag:
    #     context_chunks = await vector_repo.similarity_search(
    #         query=request.message,
    #         collection_name="knowledge_base",
    #         limit=5
    #     )
    #     context = "\n".join([chunk.text for chunk in context_chunks])
    
    # 4. Generate response using LLM (with context if available)
    # assistant_response = await rag_service.generate_response(
    #     query=request.message,
    #     context=context,
    #     conversation_history=conversation.messages[-10:]  # Last 10 messages
    # )
    
    # # 5. Save assistant response to MongoDB
    # assistant_message = await conv_repo.add_message(
    #     conversation_id=conversation.id,
    #     role="assistant",
    #     content=assistant_response.text,
    #     tokens=assistant_response.tokens
    # )
    
    # return ChatResponse(
    #     message=assistant_response.text,
    #     conversation_id=conversation.id,
    #     sources=context_chunks if request.use_rag else None
    # )