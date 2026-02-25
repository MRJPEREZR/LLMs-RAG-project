from typing import List, Dict
from pymilvus import AnnSearchRequest, RRFRanker
from app.databases.milvus import connect, get_or_create_collection
from app.core.logger import default_logger as logger

class VectorRepository:
    def __init__(self, collection_name: str, dim: int):
        connect()
        self.collection = get_or_create_collection(collection_name, dim)
        self.collection_name = collection_name

    def search(self, query: str, query_embedding: list[float], limit: int = 5):
        sparse_search_params = {"metric_type": "BM25"}

        sparse_request = AnnSearchRequest(
            data=[query],
            anns_field="sparse_vector",
            param=sparse_search_params,
            limit=limit,
        )

        dense_search_params = {"metric_type": "IP"}

        dense_request = AnnSearchRequest(
            data=[query_embedding],
            anns_field="dense_vector",
            param=dense_search_params,
            limit=limit,
        )

        results = self.collection.hybrid_search(
            requests=[sparse_request, dense_request],
            ranker=RRFRanker(),
            limit=limit,
            output_fields=["content", "metadata"],
        )

        return results[0]

    def insert_documents(self, documents: List[Dict]):
        """
        documents = [
            {
                "content": "some text",
                "embedding": embedding_vector
                "metadata": {"source": "pdf1"}
            }
        ]
        """

        entities = []
        for i, c in enumerate(documents):
            entities.append(
                {
                    "content": c["content"],
                    "dense_vector": c["embedding"],
                    "metadata": c.get("metadata", {}),
                }
            )

        self.collection.insert(entities)
        self.collection.flush()
        logger(f"Inserted {len(entities)} documents")