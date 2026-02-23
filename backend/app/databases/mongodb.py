from pymongo import AsyncMongoClient
from beanie import init_beanie
from app.models.mongo_models import Conversation
from app.core.config import MONGODB_DB_NAME, MONGODB_USR, MONGODB_PWD, MONGODB_HOST, MONGODB_PORT

async def init_mongodb():
    client = AsyncMongoClient(
        f"mongodb://{MONGODB_USR}:{MONGODB_PWD}@{MONGODB_HOST}:{MONGODB_PORT}"
    )
    await init_beanie(
        database=client[MONGODB_DB_NAME],
        document_models=[Conversation]
    )
    return client