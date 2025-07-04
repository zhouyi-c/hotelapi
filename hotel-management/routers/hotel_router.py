from fastapi import APIRouter
from agents.user_proxy_agent import UserProxyAgent
from agents.consult_agent import ConsultAgent
from agents.booking_agent import BookingAgent

# 创建API路由器
router = APIRouter()

# 咨询服务API（酒店信息/景点推荐）
@router.post("/consult")
def consult(query: str, conversation_id: str = "default"):
    """
    酒店及景点咨询接口（多层Agent体系）
    """
    user_proxy_agent = UserProxyAgent()
    return user_proxy_agent.handle_request(query, conversation_id)

# 酒店预订API
@router.post("/booking")
def booking(query: str, conversation_id: str = "default"):
    """
    酒店预订接口（多层Agent体系）
    """
    user_proxy_agent = UserProxyAgent()
    return user_proxy_agent.handle_request(query, conversation_id)

# 测试接口
@router.get("/test_consult")
async def test_consult():
    agent = ConsultAgent("test_consult")
    return {"ai_reply": agent.handle_consult("请推荐附近的酒店和景点", conversation_id="test_consult")}

@router.get("/test_booking")
async def test_booking():
    agent = BookingAgent("test_booking")
    return {"ai_reply": agent.handle_booking("我要预订明天的大床房", conversation_id="test_booking")}