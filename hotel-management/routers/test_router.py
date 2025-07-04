from fastapi import APIRouter
from agents.complaint_agent import ComplaintAgent
from agents.consult_agent import ConsultAgent
from agents.booking_agent import BookingAgent

router = APIRouter()

@router.get("/test_complaint")
async def test_complaint():
    agent = ComplaintAgent("test_complaint")
    return {"ai_reply": agent.handle_complaint("为什么房间内有蟑螂？我要投诉你们")}

@router.get("/test_consult")
async def test_consult():
    agent = ConsultAgent("test_consult")
    return {"ai_reply": agent.handle_consult("附近有什么好玩的景点？")}

@router.get("/test_booking")
async def test_booking():
    agent = BookingAgent("test_booking")
    return {"ai_reply": agent.handle_booking("我要预订明天的大床房")}
    return recommend_attractions(5)