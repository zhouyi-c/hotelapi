from fastapi import FastAPI, Request
from routers import hotel_router, complaint_router, test_router
from agents.user_proxy_agent import UserProxyAgent
import uuid  # 用于生成唯一会话ID
import config  # 确保配置加载

app = FastAPI(
    title="酒店管理系统API",
    description="集成AI代理的酒店管理服务",
    version="1.0.0"
)


# 全局代理实例
user_proxy = UserProxyAgent()

# 注册路由
app.include_router(hotel_router.router, prefix="/hotels", tags=["酒店服务"])
app.include_router(complaint_router.router, prefix="/complaints", tags=["投诉处理"])
app.include_router(test_router.router, prefix="/tests", tags=["系统测试"])

@app.get("/")
async def root():
    return {"message": "酒店管理系统API服务运行中"}


@app.post("/chat")
async def chat_endpoint(request: Request, user_input: str):
    """
    处理用户聊天请求，支持多轮对话
    """
    # 从cookies获取会话ID，如果没有则创建新会话
    from utils.memory import get_new_session_id
    # 如果不存在，则生成新的数字会话ID
    session_id = request.cookies.get("session_id") or get_new_session_id()

    # 处理用户请求
    response = user_proxy.handle_request(user_input, session_id)

    # 构建响应并设置cookie
    from fastapi.responses import JSONResponse
    response_data = {
        "response": response,
        "session_id": session_id
    }
    resp = JSONResponse(content=response_data)
    resp.set_cookie(key="session_id", value=session_id, httponly=True)
    return resp


@app.post("/reset")
async def reset_conversation(request: Request):
    """
    重置当前会话
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        # 获取ManagerAgent并重置会话
        user_proxy.manager.reset_conversation(session_id)
        return {"message": f"会话 {session_id} 已重置"}
    return {"message": "没有活动会话"}