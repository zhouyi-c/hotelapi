from fastapi import APIRouter
from services.complaint_service import handle_complaint_basic, handle_complaint_with_agent
from models.schemas import ComplaintRequest

router = APIRouter()

@router.post("/basic")
async def basic_complaint(request: ComplaintRequest):
    return {"ai_reply": handle_complaint_basic(request.message)}

@router.post("/agent")
async def agent_complaint(request: ComplaintRequest):
    return {"ai_reply": handle_complaint_with_agent(request.message)}