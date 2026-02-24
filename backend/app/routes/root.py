from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])
@router.get("/readiness")
async def readiness_check():
    return {"status": "ready"}