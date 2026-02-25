from pymilvus import (
    connections,
    FieldSchema,
    Function,
    CollectionSchema,
    DataType,
    FunctionType,
    Collection,
    utility,
)

from app.core.logger import default_logger as logger
from app.core.config import MILVUS_HOST, MILVUS_PORT

def connect():
    connections.connect(
        alias="default",
        host=MILVUS_HOST,
        port=MILVUS_PORT,
    )

def get_or_create_collection(collection_name: str, dim: int):
    if utility.has_collection(collection_name):
        return Collection(collection_name)

    fields = [
        FieldSchema(
            name="id",
            dtype=DataType.VARCHAR,
            is_primary=True,
            auto_id=True,
            max_length=100,
        ),
        FieldSchema(
            name="content",
            dtype=DataType.VARCHAR,
            max_length=65535,
            analyzer_params={"tokenizer": "standard", "filter": ["lowercase"]},
            enable_match=True,  # Enable text matching
            enable_analyzer=True,  # Enable text analysis
        ),
        FieldSchema(
            name="metadata",
            dtype=DataType.JSON,
        ),
        FieldSchema(
            name="dense_vector",
            dtype=DataType.FLOAT_VECTOR,
            dim=dim,
        ),
        FieldSchema(
            name="sparse_vector",
            dtype=DataType.SPARSE_FLOAT_VECTOR,
            dim=1024 # Dimension for Qwen3-Embedding-0.6B
        ),
    ]

    bm25_function = Function(
            name="bm25",
            function_type=FunctionType.BM25,
            input_field_names=["content"],
            output_field_names="sparse_vector",
        )

    schema = CollectionSchema(fields, description="Hybrid search collection")

    collection = Collection(
        name=collection_name,
        schema=schema,
        function=bm25_function
    )

    # Dense index (Inner Product for embeddings)
    collection.create_index(
        field_name="dense_vector",
        index_params={
            "index_type": "FLAT",
            "metric_type": "IP",
        },
    )

    # Sparse index (BM25)
    collection.create_index(
        field_name="sparse_vector",
        index_params={
            "index_type": "SPARSE_INVERTED_INDEX",
            "metric_type": "BM25",
        },
    )

    collection.load()
    logger(f"Collection '{collection_name}' created and loaded successfully")
    return collection