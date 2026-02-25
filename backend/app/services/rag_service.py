from app.repositories.vector_repo import VectorRepository
from app.services.embedding_service import embed


repo = VectorRepository(
    collection_name="football_collection",
    dim=1024,
)

query = "What is a fault ?"
query_embedding = embed(query)

results = repo.hybrid_search(query, query_embedding)

print("\nHybrid Search (Combined):")
for i, result in enumerate(results):
    print(
        f"{i+1}. Score: {result['distance']:.4f}, Content: {result['entity']['content']}"
    )