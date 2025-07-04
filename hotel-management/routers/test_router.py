from fastapi import APIRouter
from services.complaint_service import handle_complaint_basic, handle_complaint_with_agent
from services.attraction_service import recommend_attractions

router = APIRouter()

@router.get("/test_complaint")
async def test_complaint():
    test_message = "你们欺诈消费者！我要曝光你们！"
    return {"ai_reply": handle_complaint_basic(test_message)}

@router.get("/test_agent")
async def test_agent():
    return {"response": handle_complaint_with_agent("帮我找300-500元之间的酒店")}

@router.get("/test_attraction")
async def test_attraction():
    return recommend_attractions(5)