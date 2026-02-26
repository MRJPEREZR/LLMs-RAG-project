from fastapi import FastAPI
from app.routes import root, chat, conversation
from app.core.logger import setup_logger

logger = setup_logger("fastapi_app")
app = FastAPI()

app.include_router(root.router)
app.include_router(chat.router)
app.include_router(conversation.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")