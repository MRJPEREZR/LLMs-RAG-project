import requests
import json
from app.core.logger import default_logger as logger

from app.core.config import EMBEDDING_MODEL, EMBEDDING_URL

def embed(text: str) -> list:
    """Simple embedding call"""
    headers = {
        "Content-Type": "application/json"
    }
    logger.debug(f"Calling endpoint {EMBEDDING_URL}")
    #response = requests.post(f"{OLLAMA_HOST}/engines/llama.cpp/v1/embeddings", headers=headers, json={
    response = requests.post({EMBEDDING_URL}, headers=headers, json={
        "model": EMBEDDING_MODEL,
        "input": text
    })
    return {
        "status_code": response.status_code,
        "embedding": response.json()['data'][0]["embedding"],
    }