from fastapi import Depends
from typing import Dict, Any, List
from app.repositories.vector_repo import VectorRepository
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService

from app.core.logger import default_logger as logger


class RAGService:
    def __init__(self, repo: VectorRepository = Depends(),
                embedder: EmbeddingService = Depends(),
                llm: LLMService = Depends()
    ):
        self.repo = repo
        self.embedder = embedder
        self.llm = llm

    async def ask(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        logger.info("Embedding query...")
        query_embedding = await self.embedder.embed(query)
        logger.info("Query embebed...")

        logger.info("Searching in vector DB...")
        results = self.repo.search(query, query_embedding, limit=top_k)

        if not results:
            return {
                "answer": "I don't have enough information to answer this question.",
                "sources": [],
            }
        context = self._build_context(results)

        prompt = self._build_prompt(query, context)

        response = await self.llm.chat(prompt)

        return {
            "answer": response,
            "sources": self._extract_sources(results),
            "context_used": context,
        }

    def _build_context(self, results: List[Dict]) -> str:
        return "\n\n".join(
            [doc["entity"]["content"] for doc in results]
        )

    def _build_prompt(self, query: str, context: str) -> str:
        return f"""
You are a helpful assistant.

Answer the following question based only on the provided context.
If the context doesn't contain relevant information, say:
"I don't have enough information to answer this question."

Context:
{context}

Question: {query}

Answer:
"""

    def _extract_sources(self, results: List[Dict]) -> List[Dict]:
        return [
            {
                "score": doc["distance"],
                "content": doc["entity"]["content"],
                "metadata": doc["entity"].get("metadata", {}),
            }
            for doc in results
        ]