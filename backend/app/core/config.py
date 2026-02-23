import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "chatbot")
MONGODB_USR = os.getenv("MONGODB_USR", "user")
MONGODB_PWD = os.getenv("MONGODB_PWD", "pass")
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))