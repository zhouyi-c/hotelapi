from fastapi import APIRouter
from services.complaint_service import handle_complaint_basic, handle_complaint_with_agent
from models.schemas import ComplaintRequest

# 创建API路由器
router = APIRouter()

# 基础投诉处理API
@router.post("/basic")
async def basic_complaint(request: ComplaintRequest):
    """
    基础投诉处理API
    参数：
        request: ComplaintRequest，包含message字段
    返回：AI回复（dict）
    """
    # 只做参数校验和Service调用，不含业务逻辑
    return {"ai_reply": handle_complaint_basic(request.message)}

# 基于Agent的复杂投诉处理API
@router.post("/agent")
async def agent_complaint(request: ComplaintRequest):
    """
    基于Agent的复杂投诉处理API
    参数：
        request: ComplaintRequest，包含message字段
    返回：AI回复（dict）
    """
    # 只做参数校验和Service调用，不含业务逻辑
    return {"ai_reply": handle_complaint_with_agent(request.message)}