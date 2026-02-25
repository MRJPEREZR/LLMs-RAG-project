from pymilvus import AnnSearchRequest, RRFRanker
from app.databases.milvus import connect, get_or_create_collection


class VectorRepository:
    def __init__(self, collection_name: str, dim: int):
        connect()
        self.collection = get_or_create_collection(collection_name, dim)
        self.collection_name = collection_name

    def hybrid_search(self, query: str, query_embedding: list[float], limit: int = 5):
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