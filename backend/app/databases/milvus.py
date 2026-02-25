from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
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
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True,
        ),
        FieldSchema(
            name="content",
            dtype=DataType.VARCHAR,
            max_length=65535,
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
        ),
    ]

    schema = CollectionSchema(fields, description="Hybrid search collection")

    collection = Collection(
        name=collection_name,
        schema=schema,
    )

    # Dense index (Inner Product for embeddings)
    collection.create_index(
        field_name="dense_vector",
        index_params={
            "index_type": "HNSW",
            "metric_type": "IP",
            "params": {"M": 16, "efConstruction": 200},
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
    return collection