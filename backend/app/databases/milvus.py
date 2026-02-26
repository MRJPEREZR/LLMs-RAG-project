from pymilvus import (
    connections,
    Collection,
    utility,
)

from app.core.logger import default_logger as logger
from app.core.config import MILVUS_HOST, MILVUS_PORT
from app.models.milvus_schemas import build_hybrid_schema


def connect():
    connections.connect(
        alias="default",
        host=MILVUS_HOST,
        port=MILVUS_PORT,
    )


def get_or_create_collection(collection_name: str, dim: int):
    if utility.has_collection(collection_name):
        logger.info(f"Collection '{collection_name}' already exists. Loading...")
        collection = Collection(collection_name)
        collection.load()
        return collection

    schema = build_hybrid_schema(dim)

    collection = Collection(
        name=collection_name,
        schema=schema,
    )

    collection.create_index(
        field_name="dense_vector",
        index_params={
            "index_type": "FLAT",
            "metric_type": "IP",
        },
    )

    collection.create_index(
        field_name="sparse_vector",
        index_params={
            "index_type": "SPARSE_INVERTED_INDEX",
            "metric_type": "BM25",
        },
    )

    collection.load()
    logger.info(f"Collection '{collection_name}' created and loaded successfully")

    return collection