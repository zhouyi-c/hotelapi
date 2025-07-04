from fastapi import APIRouter
from services.complaint_service import handle_complaint_basic, handle_complaint_with_agent

# 创建API路由器
router = APIRouter()

# 投诉处理API
@router.post("/complaint")
async def complaint_service(user_message: str, conversation_id: str = "default"):
    """
    投诉处理接口
    :param user_message: 用户投诉内容
    :param conversation_id: 对话唯一标识（用于记忆）
    :return: 智能回复文本
    """
    agent = ComplaintAgent(conversation_id)
    return {"ai_reply": agent.handle_complaint(user_message)}

# 测试接口
@router.get("/test_complaint")
async def test_complaint():
    agent = ComplaintAgent("test_complaint")
    return {"ai_reply": agent.handle_complaint("房间不干净，怎么处理？")}