from typing import Optional

from fastapi import FastAPI, HTTPException
from openai import OpenAI, models  # 导入OpenAI SDK
from dotenv import load_dotenv
import os
from pydantic import BaseModel, conint
from datetime import date





class HotelQuery(BaseModel):
    min_price: conint(ge=0) = 0
    max_price: conint(le=10000) = 1000
    date: Optional[date] = None
# 这行代码会加载.env文件中的变量

load_dotenv()
app = FastAPI()

# 千帆API配置（替换为你的千帆API Key）
#QIANFAN_API_KEY = "bce-v3/ALTAK-8aQMewMUYm94lfFubPwZF/5c65b326b3f078741d4dbb5c8c0827acbf084c3a"  # 完整的API Key（包含bce-v3/前缀）
QIANFAN_BASE_URL = "https://qianfan.baidubce.com/v2"  # 千帆API基础地址
# 修改前
# QIANFAN_API_KEY = "bce-v3/ALTAK-8aQMewMUYm94lfFubPwZF/5c65b326b3f078741d4dbb5c8c0827acbf084c3a"

# 修改后
QIANFAN_API_KEY = os.getenv("QIANFAN_API_KEY")
if not QIANFAN_API_KEY:
    raise ValueError("请设置QIANFAN_API_KEY环境变量")


fake_db = [
    {"id": 1, "name": "四季酒店", "price": 800, "date": "2025-07-10"},
    {"id": 2, "name": "如家快捷", "price": 200, "date": "2025-07-12"}
]


# 酒店查询接口（保持不变）
@app.get("/hotels")
async def filter_hotels(min_price: int = 0, max_price: int = 1000, date: str = None):
    """根据价格和日期过滤酒店"""
    results = [h for h in fake_db if min_price <= h["price"] <= max_price]
    if date:
        results = [h for h in results if h["date"] == date]
    return {"hotels": results}


# CRISPE提示词构建函数（保持不变）
def build_crispe_prompt():
    return """
您是一名五星级酒店值班经理（员工编号A100）。用户预订了海景房但被安排在背街房，情绪激动。请按以下要求处理：
1. 诚恳承认错误并表达歉意
2. 提供即时解决方案（换房或合理补偿）
3. 避免使用"系统问题"等推脱表述
4. 回复长度不超过80字
禁用词：不可能/没办法/规定
"""


# 使用千帆平台处理投诉（使用OpenAI兼容接口）
def handle_complaint_with_qianfan(user_message: str):
    try:

        # 创建OpenAI客户端（配置千帆参数）
        client = OpenAI(
            api_key=QIANFAN_API_KEY,
            base_url=QIANFAN_BASE_URL
        )

        # 构建消息列表
        messages = [
            {"role": "system", "content": build_crispe_prompt()},
            {"role": "user", "content": user_message}
        ]

        # 发送请求到千帆平台
        completion = client.chat.completions.create(
            model="ernie-4.0-8k",  # 使用ERNIE 3.5模型
            messages=messages,
            temperature=0.7
        )

        # 返回AI生成的回复
        return completion.choices[0].message.content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"千帆API调用失败: {str(e)}")


# 客服投诉处理接口（修改函数名）
@app.post("/handle_complaint")
async def handle_complaint(user_message: str):
    """使用CRISPE框架处理用户投诉"""
    try:
        ai_reply = handle_complaint_with_qianfan(user_message)
        return {"ai_reply": ai_reply}
    except Exception as e:
        return {"error": str(e)}


# 测试路由（保持不变）
@app.get("/test_prompt")
async def test_prompt():
    """测试CRISPE提示词效果"""
    test_message = "你们欺诈消费者！我要曝光你们！"
    return await handle_complaint(test_message)


# 测试千帆API连接（更新测试）
@app.get("/test_qianfan_connection")
async def test_qianfan_connection():
    """测试千帆API连接"""
    try:
        test_message = "测试连接"
        ai_reply = handle_complaint_with_qianfan(test_message)
        return {"status": "success", "message": "千帆API连接正常", "response": ai_reply}
    except Exception as e:
        return {"status": "error", "message": str(e)}