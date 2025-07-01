from typing import Optional

from fastapi import FastAPI, HTTPException
from openai import OpenAI, models  # 导入OpenAI SDK
from dotenv import load_dotenv
import os
from pydantic import BaseModel, conint, json
from datetime import date

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, llm
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.tools import BaseTool

# 创建酒店查询工具
import json
from datetime import date
from typing import Any, Dict, Optional

class HotelQuery(BaseModel):
    min_price: conint(ge=0) = 0
    max_price: conint(le=10000) = 1000
    date: Optional[date] = None


# 这行代码会加载.env文件中的变量

load_dotenv()
app = FastAPI()

# 千帆API配置（替换为你的千帆API Key）
# QIANFAN_API_KEY = "bce-v3/ALTAK-8aQMewMUYm94lfFubPwZF/5c65b326b3f078741d4dbb5c8c0827acbf084c3a"  # 完整的API Key（包含bce-v3/前缀）
QIANFAN_BASE_URL = "https://qianfan.baidubce.com/v2"  # 千帆API基础地址
# 修改前
# QIANFAN_API_KEY = "bce-v3/ALTAK-8aQMewMUYm94lfFubPwZF/5c65b326b3f078741d4dbb5c8c0827acbf084c3a"

# 修改后
QIANFAN_API_KEY = os.getenv("QIANFAN_API_KEY")
if not QIANFAN_API_KEY:
    raise ValueError("请设置QIANFAN_API_KEY环境变量")


# 创建全局LLM实例
llm = ChatOpenAI(
    api_key=QIANFAN_API_KEY,
    base_url=QIANFAN_BASE_URL,
    model="ernie-4.0-8k",
    temperature=0.7
)

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



# 使用千帆平台处理投诉（使用OpenAI兼容接口）
def handle_complaint_with_qianfan(user_message: str):
    try:
        # 创建 CRISPE 提示词模板
        crispe_template = PromptTemplate(
            input_variables=["user_message"],
            template="""
                    您是一名五星级酒店值班经理（员工编号A100）。用户说：{user_message}
                    请按以下要求处理：
                    1. 诚恳承认错误并表达歉意
                    2. 提供即时解决方案（换房或合理补偿）
                    3. 避免使用"系统问题"等推脱表述
                    4. 回复长度不超过80字
                    禁用词：不可能/没办法/规定
                    """
        )


        #creat handle chain
        complaint_chain = LLMChain(
            llm=llm,
            prompt=crispe_template,
            verbose=True,
        )

        response = complaint_chain.invoke({"user_message": user_message})
        return response["text"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"千帆API调用失败: {str(e)}")


def handle_complaint_with_memory(user_message: str,conversation_id:str):
    #create single memory for session
    memory = ConversationBufferMemory(memory_key="chat_history")

    #add history
    memory.save_context(
        {"input":"用户之前的问题"},
        {"output":"之前的回复"},
    )
    memory_template = PromptTemplate(
        input_variables=["chat_history","user_message"],
        template="""
        历史对话:
        {chat_history}
        
        当前用户消息:
        {user_message}
        您是一名五星级酒店值班经理（员工编号A100），请按以下要求处理：
        1. 诚恳承认错误并表达歉意
        2. 提供即时解决方案（换房或合理补偿）
        3. 避免使用"系统问题"等推脱表述
        4. 回复长度不超过80字
        禁用词：不可能/没办法/规定
        
        """
    )
    #create chain with memory
    chain = LLMChain(
            llm=llm,
            prompt=memory_template,
            memory=memory,
    )


    return chain.invoke({"user_message": user_message})["text"]


from langchain.agents import Tool, initialize_agent
from langchain.tools import BaseTool


# 优化后的酒店查询工具
class HotelSearchTool(BaseTool):
    name: str = "hotel_search"
    description: str = (
        "根据价格范围(min_price和max_price)和日期(date)查询酒店信息。"
        "参数要求：min_price为整数（最低价格），max_price为整数（最高价格），date为字符串（格式YYYY-MM-DD）。"
        "返回匹配的酒店列表或空列表。"
    )

    def _run(self, min_price: int, max_price: int, date: str = None):
        # 执行搜索
        results = [h for h in fake_db if min_price <= h["price"] <= max_price]
        if date:
            results = [h for h in results if h["date"] == date]

        # 返回结构化结果
        return {
            "match_criteria": {
                "min_price": min_price,
                "max_price": max_price,
                "date": date
            },
            "result_count": len(results),
            "results": results
        }



# 创建带工具的代理
def create_complaint_agent():
    # 使用工具实例而不是Tool包装器
    tools = [HotelSearchTool()]

    # 使用适合多参数的结构化代理
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,  # 处理参数解析错误
        max_iterations=3,  # 限制最大对话轮数
        early_stopping_method = "generate"  # 当无法解析时直接生成回复
    )

    return agent


# 使用代理处理复杂请求
def handle_complex_request(user_query: str):
    try:
        agent = create_complaint_agent()
        return agent.run(user_query)
    except Exception as e:
        # 记录详细错误信息
        error_details = f"代理执行错误: {str(e)}\n"

        # 添加额外的调试信息
        error_details += f"查询内容: '{user_query}'\n"
        error_details += f"代理类型: {type(agent).__name__}\n"

        # 抛出包含详细信息的HTTP异常
        raise HTTPException(
            status_code=500,
            detail=error_details
        )

# 使用代理处理复杂请求
def handle_complex_request(user_query: str):
    agent = create_complaint_agent()
    return agent.run(user_query)

# API端点
@app.post("/handle_complaint")
async def handle_complaint(user_message: str):
    """基本投诉处理"""
    try:
        ai_reply = handle_complaint_with_qianfan(user_message)
        return {"ai_reply": ai_reply}
    except Exception as e:
        return {"error": str(e)}



# 带记忆的投诉处理
@app.post("/handle_complaint_with_memory")
async def handle_complaint_with_memory_endpoint(request: dict):
    """带对话历史的投诉处理"""
    try:
        response = handle_complaint_with_memory(
            user_message=request["message"],
            conversation_id=request.get("conversation_id", "default")
        )
        return {"ai_reply": response}
    except Exception as e:
        return {"error": str(e)}

# 代理端点
@app.post("/complex_query")
async def complex_query(user_query: str):
    """处理需要工具使用的复杂查询"""
    try:
        response = handle_complex_request(user_query)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}


# 测试路由
@app.get("/test_prompt")
async def test_prompt():
    """测试CRISPE提示词效果"""
    test_message = "你们欺诈消费者！我要曝光你们！"
    # 使用基本处理函数
    return {"ai_reply": handle_complaint_with_qianfan(test_message)}

@app.get("/test_memory")
async def test_memory():
    """测试记忆功能"""
    # 第一轮对话
    response1 = handle_complaint_with_memory("我订的海景房呢？", "test_conversation")
    # 第二轮对话
    response2 = handle_complaint_with_memory("你上次说给我升级，为什么还是普通房？", "test_conversation")
    return {"first": response1, "second": response2}

@app.get("/test_agent")
async def test_agent():
    """测试代理工具功能"""
    response = handle_complex_request("帮我找300-500元之间的酒店")
    return {"response": response}

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