import requests
import json
from logger import default_logger as logger

from app.core.config import LLM_MODEL, LLM_URL

def chat(prompt: str) -> str:
    """Simple chat call"""
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post({LLM_URL}, headers=headers, json={
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    })
    return {
        "status_code": response.status_code,
        "content": response.json()['message']['content']
    }