from fastapi import APIRouter
from services.complaint_service import handle_complaint_basic, handle_complaint_with_agent
from agents.user_proxy_agent import UserProxyAgent

# 创建API路由器
router = APIRouter()

# 实例化统一入口代理Agent
user_proxy_agent = UserProxyAgent()

# 投诉处理API
@router.post("/complaint")
def complaint_service(user_message: str, conversation_id: str = "default"):
    """
    投诉处理接口（多层Agent体系）
    :param user_message: 用户投诉内容
    :param conversation_id: 对话唯一标识（用于记忆）
    :return: 智能回复文本
    """
    return user_proxy_agent.handle_request(user_message, conversation_id)

# 测试接口
@router.get("/test_complaint")
def test_complaint():
    return user_proxy_agent.handle_request("房间不干净，怎么处理？", "test_complaint")