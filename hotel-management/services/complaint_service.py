from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.tool_agent import ToolAgent
from config import Config

def handle_complaint_basic(user_message: str):
    """基本投诉处理"""
    try:
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

        complaint_chain = LLMChain(
            llm=ChatOpenAI(
                api_key=Config.QIANFAN_API_KEY,
                base_url=Config.QIANFAN_BASE_URL,
                model=Config.QIANFAN_MODEL,
                temperature=0.7
            ),
            prompt=crispe_template
        )

        return complaint_chain.invoke({"user_message": user_message})["text"]
    except Exception as e:
        raise Exception(f"投诉处理失败: {str(e)}")

def handle_complaint_with_agent(user_message: str):
    """使用代理处理复杂投诉"""
    try:
        agent = ToolAgent()
        return agent.run(user_message)
    except Exception as e:
        raise Exception(f"代理处理失败: {str(e)}")