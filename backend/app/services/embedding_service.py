# # app/services/embedding/base.py
# from abc import ABC, abstractmethod
# from typing import List, Union
# import numpy as np

# class BaseEmbeddingService(ABC):
#     """Abstract base for embedding services"""
    
#     @abstractmethod
#     async def embed(self, text: str) -> List[float]:
#         """Generate embedding for a single text"""
#         pass
    
#     @abstractmethod
#     async def embed_batch(self, texts: List[str]) -> List[List[float]]:
#         """Generate embeddings for multiple texts"""
#         pass
    
#     @property
#     @abstractmethod
#     def dimension(self) -> int:
#         """Return embedding dimension"""
#         pass

# # app/services/embedding/sentence_transformer.py
# from sentence_transformers import SentenceTransformer
# import numpy as np
# from typing import List

# class SentenceTransformerService(BaseEmbeddingService):
#     def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
#         self.model = SentenceTransformer(model_name)
#         self._dimension = self.model.get_sentence_embedding_dimension()
    
#     async def embed(self, text: str) -> List[float]:
#         """Generate embedding for a single text"""
#         embedding = self.model.encode(text, normalize_embeddings=True)
#         return embedding.tolist()
    
#     async def embed_batch(self, texts: List[str]) -> List[List[float]]:
#         """Generate embeddings for multiple texts"""
#         embeddings = self.model.encode(texts, normalize_embeddings=True)
#         return [emb.tolist() for emb in embeddings]
    
#     @property
#     def dimension(self) -> int:
#         return self._dimension

# # app/services/embedding/openai_embedding.py
# import openai
# from typing import List

# class OpenAIEmbeddingService(BaseEmbeddingService):
#     def __init__(self, api_key: str, model: str = "text-embedding-ada-002"):
#         openai.api_key = api_key
#         self.model = model
#         self._dimension = 1536  # Ada-002 dimension
    
#     async def embed(self, text: str) -> List[float]:
#         response = await openai.Embedding.acreate(
#             model=self.model,
#             input=text
#         )
#         return response['data'][0]['embedding']
    
#     async def embed_batch(self, texts: List[str]) -> List[List[float]]:
#         # OpenAI supports batch embedding
#         response = await openai.Embedding.acreate(
#             model=self.model,
#             input=texts
#         )
#         # Sort by index to maintain order
#         embeddings = sorted(response['data'], key=lambda x: x['index'])
#         return [item['embedding'] for item in embeddings]
    
#     @property
#     def dimension(self) -> int:
#         return self._dimension