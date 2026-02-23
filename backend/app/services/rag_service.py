# # app/services/rag/retriever.py
# from typing import List, Dict, Any, Optional
# import asyncio

# class VectorRetriever:
#     """Retrieve relevant documents from vector store"""
    
#     def __init__(
#         self,
#         vector_repo,
#         embedding_service,
#         collection_name: str = "knowledge_base"
#     ):
#         self.vector_repo = vector_repo
#         self.embedding_service = embedding_service
#         self.collection_name = collection_name
    
#     async def retrieve(
#         self,
#         query: str,
#         top_k: int = 5,
#         score_threshold: float = 0.7,
#         filter_criteria: Optional[Dict] = None
#     ) -> List[Dict[str, Any]]:
#         """
#         Retrieve relevant documents for a query
#         """
#         # Generate query embedding
#         query_embedding = await self.embedding_service.embed(query)
        
#         # Search in Milvus
#         results = await self.vector_repo.similarity_search(
#             collection_name=self.collection_name,
#             query_embedding=query_embedding,
#             top_k=top_k,
#             filter=filter_criteria
#         )
        
#         # Filter by score threshold
#         filtered_results = [
#             {
#                 "text": r.text,
#                 "score": r.score,
#                 "metadata": r.metadata,
#                 "document_id": r.document_id
#             }
#             for r in results
#             if r.score >= score_threshold
#         ]
        
#         return filtered_results

# class ContextBuilder:
#     """Build context from retrieved documents"""
    
#     @staticmethod
#     def build_context(
#         documents: List[Dict[str, Any]],
#         max_tokens: int = 2000,
#         include_metadata: bool = True
#     ) -> str:
#         """
#         Build a context string from retrieved documents
#         """
#         context_parts = []
#         current_tokens = 0
        
#         for i, doc in enumerate(documents, 1):
#             doc_text = doc["text"]
            
#             # Rough token estimation (4 chars ≈ 1 token)
#             doc_tokens = len(doc_text) // 4
            
#             if current_tokens + doc_tokens > max_tokens:
#                 break
            
#             if include_metadata and doc.get("metadata"):
#                 source = doc["metadata"].get("source", "Unknown")
#                 doc_text = f"[Source {i}: {source}]\n{doc_text}"
#             else:
#                 doc_text = f"[Document {i}]\n{doc_text}"
            
#             context_parts.append(doc_text)
#             current_tokens += doc_tokens
        
#         return "\n\n".join(context_parts)

# class RAGService:
#     """Main RAG service orchestrator"""
    
#     def __init__(
#         self,
#         retriever: VectorRetriever,
#         llm_service: BaseLLMService,
#         context_builder: ContextBuilder = None
#     ):
#         self.retriever = retriever
#         self.llm_service = llm_service
#         self.context_builder = context_builder or ContextBuilder()
    
#     async def answer_question(
#         self,
#         question: str,
#         conversation_history: Optional[List[Dict]] = None,
#         top_k: int = 5,
#         temperature: float = 0.7
#     ) -> Dict[str, Any]:
#         """
#         Answer a question using RAG
#         """
#         # 1. Retrieve relevant documents
#         retrieved_docs = await self.retriever.retrieve(
#             query=question,
#             top_k=top_k
#         )
        
#         # 2. Build context from retrieved docs
#         context = self.context_builder.build_context(retrieved_docs)
        
#         # 3. Format conversation history
#         history_str = ""
#         if conversation_history:
#             history_str = PromptTemplates.format_conversation_history(
#                 conversation_history
#             )
        
#         # 4. Create RAG prompt
#         prompt = PromptTemplates.format_rag_prompt(
#             query=question,
#             context=context,
#             history=history_str
#         )
        
#         # 5. Generate response with LLM
#         response = await self.llm_service.generate(
#             prompt=prompt,
#             system_prompt=PromptTemplates.SYSTEM_PROMPTS["rag"],
#             temperature=temperature
#         )
        
#         # 6. Prepare sources for citation
#         sources = [
#             {
#                 "text": doc["text"][:200] + "...",  # Truncate for response
#                 "score": doc["score"],
#                 "metadata": doc.get("metadata", {})
#             }
#             for doc in retrieved_docs[:3]  # Top 3 sources
#         ]
        
#         return {
#             "answer": response.text,
#             "sources": sources,
#             "tokens_used": response.tokens_used,
#             "model_used": response.model_used
#         }
    
#     async def stream_answer(
#         self,
#         question: str,
#         conversation_history: Optional[List[Dict]] = None
#     ) -> AsyncGenerator[str, None]:
#         """
#         Stream RAG answer token by token
#         """
#         # Retrieve docs first (can't stream this part)
#         retrieved_docs = await self.retriever.retrieve(
#             query=question,
#             top_k=5
#         )
        
#         context = self.context_builder.build_context(retrieved_docs)
        
#         prompt = PromptTemplates.format_rag_prompt(
#             query=question,
#             context=context,
#             history=conversation_history
#         )
        
#         # Stream LLM response
#         async for token in self.llm_service.stream_generate(
#             prompt=prompt,
#             system_prompt=PromptTemplates.SYSTEM_PROMPTS["rag"]
#         ):
#             yield token