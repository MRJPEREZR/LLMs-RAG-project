import requests
from app.core.logger import default_logger as logger

class LLMService:
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model

    async def chat(self, prompt: str) -> str:
        """Call LLM service and return generated text"""

        headers = {"Content-Type": "application/json"}

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
        }

        logger.debug(f"Calling LLM endpoint: {self.url}/api/chat")

        try:
            response = requests.post(
                self.url + "/api/chat",
                headers=headers,
                json=payload,
                timeout=60,
            )

            response.raise_for_status()
            data = response.json()

            logger.debug(f"LLM response: {data}")

            if "message" in data:
                return data["message"]["content"]

            raise RuntimeError("Unexpected LLM response format")

        except requests.exceptions.RequestException as e:
            logger.error(f"LLM service failed: {e}")
            raise RuntimeError("LLM service unavailable")