from app.repositories.conversation_repo import ConversationRepository
from app.repositories.vector_repo import VectorRepository
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService 
from app.services.rag_service import RAGService
from app.databases.mongodb import init_mongodb
from app.databases.milvus import connect
from fastapi import HTTPException, Depends
from app.core.logger import default_logger as logger

from app.core.config import LLM_MODEL, LLM_URL, EMBEDDING_MODEL, EMBEDDING_URL

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

async def get_vector_repo(
        collection_name: str = "football_docs",
        dim: int = 1024
):
    logger.debug("VectorRepository created successfully")
    return VectorRepository(collection_name=collection_name, dim=dim)

async def get_embedding_service(
        url: str = EMBEDDING_URL,
        model: str = EMBEDDING_MODEL
):
    logger.info(f"Using embedding URL: {EMBEDDING_URL} and model: {EMBEDDING_MODEL}")
    return EmbeddingService(url, model)

async def get_llm_service(
        url: str = LLM_URL,
        model: str = LLM_MODEL
):
    logger.info(f"Using llm URL: {LLM_URL} and model: {LLM_MODEL}")
    return LLMService(url, model)

async def get_rag_service(
    repo: VectorRepository = Depends(get_vector_repo),
    embedder: EmbeddingService = Depends(get_embedding_service),
    llm: LLMService = Depends(get_llm_service),
):
    logger.debug("RAGService created successfully")
    return RAGService(repo, embedder, llm)