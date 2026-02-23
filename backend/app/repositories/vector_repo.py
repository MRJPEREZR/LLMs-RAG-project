# class VectorRepository:
#     def __init__(self, milvus_client, embedding_service):
#         self.milvus = milvus_client
#         self.embedding_service = embedding_service
    
#     async def similarity_search(self, query: str, collection_name: str, limit: int = 5):
#         # Generate embedding for query
#         query_embedding = await self.embedding_service.embed(query)
        
#         # Search in Milvus
#         collection = await self.milvus.get_collection(collection_name)
#         results = collection.search(
#             data=[query_embedding],
#             anns_field="embedding",
#             param={"metric_type": "IP", "params": {"nprobe": 10}},
#             limit=limit,
#             output_fields=["text", "metadata"]
#         )
#         return results
    
#     async def store_conversation_pair(self, conversation_id: str, user_message: str, assistant_response: str):
#         # Store conversation embeddings in Milvus for future reference
#         pass