from fastapi import FastAPI
from app.routes import chat, conversation

app = FastAPI()

app.include_router(chat.router)
app.include_router(conversation.router)