# # app/models/milvus_schemas.py
# from pymilvus import CollectionSchema, FieldSchema, DataType

# # Define schema for knowledge base chunks
# knowledge_base_schema = CollectionSchema(
#     fields=[
#         FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#         FieldSchema(name="chunk_id", dtype=DataType.VARCHAR, max_length=100),
#         FieldSchema(name="document_id", dtype=DataType.VARCHAR, max_length=100),
#         FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=8192),
#         FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),  # Your embedding dimension
#         FieldSchema(name="metadata", dtype=DataType.JSON),  # Store source, page, etc.
#     ],
#     description="Knowledge base chunks for RAG"
# )

# # Schema for conversation embeddings (optional - for semantic search over chat history)
# conversation_memory_schema = CollectionSchema(
#     fields=[
#         FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#         FieldSchema(name="conversation_id", dtype=DataType.VARCHAR, max_length=100),
#         FieldSchema(name="message_id", dtype=DataType.VARCHAR, max_length=100),
#         FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=4096),
#         FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
#         FieldSchema(name="role", dtype=DataType.VARCHAR, max_length=20),
#         FieldSchema(name="timestamp", dtype=DataType.INT64),  # Unix timestamp
#     ],
#     description="Conversation memory for semantic search"
# )