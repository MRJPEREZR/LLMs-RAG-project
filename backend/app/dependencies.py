# # app/api/dependencies.py
# from functools import lru_cache
# from app.services.llm.openai_service import OpenAIService
# from app.services.llm.ollama_service import OllamaService
# from app.services.embedding.sentence_transformer import SentenceTransformerService
# from app.services.rag.retriever import VectorRetriever, RAGService
# from app.services.chat_service import ChatService
# from app.repositories.conversation_repo import ConversationRepository
# from app.repositories.vector_repo import VectorRepository

# from fastapi import Depends

# @lru_cache()
# def get_settings():
#     return Settings()

# async def get_llm_service():
#     """Factory for LLM service based on config"""
#     settings = get_settings()
    
#     if settings.LLM_PROVIDER == "openai":
#         return OpenAIService(
#             api_key=settings.OPENAI_API_KEY,
#             model=settings.OPENAI_MODEL
#         )
#     elif settings.LLM_PROVIDER == "ollama":
#         return OllamaService(
#             base_url=settings.OLLAMA_URL,
#             model=settings.OLLAMA_MODEL
#         )
#     else:
#         raise ValueError(f"Unknown LLM provider: {settings.LLM_PROVIDER}")

# async def get_embedding_service():
#     """Factory for embedding service"""
#     settings = get_settings()
    
#     if settings.EMBEDDING_PROVIDER == "sentence_transformer":
#         return SentenceTransformerService(
#             model_name=settings.SENTENCE_TRANSFORMER_MODEL
#         )
#     elif settings.EMBEDDING_PROVIDER == "openai":
#         return OpenAIEmbeddingService(api_key=settings.OPENAI_API_KEY)
#     else:
#         raise ValueError(f"Unknown embedding provider: {settings.EMBEDDING_PROVIDER}")

# async def get_vector_repo(
#     milvus_client=Depends(get_milvus_client),
#     embedding_service=Depends(get_embedding_service)
# ):
#     return VectorRepository(milvus_client, embedding_service)

# async def get_rag_service(
#     vector_repo=Depends(get_vector_repo),
#     embedding_service=Depends(get_embedding_service),
#     llm_service=Depends(get_llm_service)
# ):
#     retriever = VectorRetriever(vector_repo, embedding_service)
#     return RAGService(retriever, llm_service)

# async def get_chat_service(
#     llm_service=Depends(get_llm_service),
#     rag_service=

# app/api/dependencies.py
from app.repositories.conversation_repo import ConversationRepository
from app.database.mongodb import get_database_client
from functools import lru_cache
from fastapi import Depends, HTTPException
import logging

logger = logging.getLogger(__name__)

# Option 1: Simple dependency that creates a new instance each time
async def get_conversation_repo():
    """
    Dependency provider for ConversationRepository.
    Creates a new repository instance for each request.
    """
    # Get database client (however you initialize it)
    db_client = await get_database_client()
    
    # Create and return repository instance
    return ConversationRepository(db_client)


# Option 2: With caching/singleton pattern (more efficient)
@lru_cache()
def get_conversation_repo_singleton():
    """
    Singleton pattern - same instance for all requests.
    Be careful with this if your repository maintains state!
    """
    db_client = get_database_client()  # This might need to be async
    return ConversationRepository(db_client)


# Option 3: More complex with error handling and logging
async def get_conversation_repo_with_monitoring():
    """
    Production-ready dependency with logging and monitoring
    """
    try:
        db_client = await get_database_client()
        repo = ConversationRepository(db_client)
        
        # You could add logging here
        logger.debug("ConversationRepository created successfully")
        
        return repo
    except Exception as e:
        logger.error(f"Failed to create ConversationRepository: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Database connection failed"
        )


# Option 4: If you need to pass parameters
def get_conversation_repo_with_config(collection_name: str = "conversations"):
    """
    Factory function that returns a dependency with specific config
    """
    async def dependency():
        db_client = await get_database_client()
        return ConversationRepository(
            db_client=db_client,
            collection_name=collection_name  # If your repo accepts this
        )
    return dependency