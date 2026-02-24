from fastapi import FastAPI
from app.routes import root, chat, conversation

app = FastAPI()

app.include_router(root.router)
app.include_router(chat.router)
app.include_router(conversation.router)