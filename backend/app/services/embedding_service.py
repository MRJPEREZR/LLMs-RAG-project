import requests
from app.core.logger import default_logger as logger

class EmbeddingService:
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    async def embed(self, text: str) -> list[float]:
        """Call embedding service and return vector"""

        headers = {"Content-Type": "application/json"}

        payload = {
            "model": self.model,
            "input": text,
        }

        logger.debug(f"Calling embedding endpoint: {self.url}/embeddings")

        try:
            response = requests.post(
                self.url + "/embeddings",
                headers=headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            return data["data"][0]["embedding"]

        except requests.exceptions.RequestException as e:
            logger.error(f"Embedding service failed: {e}")
            raise RuntimeError("Embedding service unavailable")