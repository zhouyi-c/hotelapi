from fastapi import FastAPI
from routers import hotel_router, complaint_router, test_router
import config  # 确保配置加载

app = FastAPI(
    title="酒店管理系统API",
    description="集成AI代理的酒店管理服务",
    version="1.0.0"
)

# 注册路由
app.include_router(hotel_router.router, prefix="/hotels", tags=["酒店服务"])
app.include_router(complaint_router.router, prefix="/complaints", tags=["投诉处理"])
app.include_router(test_router.router, prefix="/tests", tags=["系统测试"])

@app.get("/")
async def root():
    return {"message": "酒店管理系统API服务运行中"}