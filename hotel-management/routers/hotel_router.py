from fastapi import APIRouter
from agents.consult_agent import ConsultAgent
from agents.booking_agent import BookingAgent

# 创建API路由器
router = APIRouter()

# 咨询服务API（酒店信息/景点推荐）
@router.post("/consult")
async def consult_service(user_message: str, conversation_id: str = "default"):
    """
    酒店咨询与景点推荐接口
    :param user_message: 用户咨询内容
    :param conversation_id: 对话唯一标识（用于记忆）
    :return: 智能回复文本
    """
    agent = ConsultAgent(conversation_id)
    return {"ai_reply": agent.handle_consult(user_message)}

# 酒店预订API
@router.post("/booking")
async def booking_service(user_message: str, conversation_id: str = "default"):
    """
    酒店预订接口
    :param user_message: 用户预订请求
    :param conversation_id: 对话唯一标识（用于记忆）
    :return: 智能回复文本
    """
    agent = BookingAgent(conversation_id)
    return {"ai_reply": agent.handle_booking(user_message)}

# 测试接口
@router.get("/test_consult")
async def test_consult():
    agent = ConsultAgent("test_consult")
    return {"ai_reply": agent.handle_consult("请推荐附近的酒店和景点")}

@router.get("/test_booking")
async def test_booking():
    agent = BookingAgent("test_booking")
    return {"ai_reply": agent.handle_booking("我要预订明天的大床房")}