import os
from dotenv import load_dotenv
from urllib.parse import urljoin

load_dotenv()

MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "chatbot")
MONGODB_USR = os.getenv("MONGODB_USR", "user")
MONGODB_PWD = os.getenv("MONGODB_PWD", "pass")
MONGODB_HOST = os.getenv("MONGODB_HOST", "mongodb")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))

MILVUS_HOST = os.getenv("MILVUS_HOST", "milvus")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530") 

LLM_URL = os.getenv("LLM_URL", "http://localhost:12434")
if "/v1" in LLM_URL.rstrip("/"):
    LLM_URL = LLM_URL[:LLM_URL.rfind("/v1")]

EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://localhost:12434/engines/llama.cpp/v1/")
if "/v1" in EMBEDDING_URL.rstrip("/"):
    EMBEDDING_URL = EMBEDDING_URL[:EMBEDDING_URL.rfind("/v1")]
EMBEDDING_URL=urljoin(EMBEDDING_URL, "engines/llama.cpp/v1/")


LLM_MODEL = os.getenv("LLM_MODEL", "ai/qwen3:0.6B-Q4_0")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "ai/qwen3-embedding:0.6B-F16")