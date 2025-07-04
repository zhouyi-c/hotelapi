"""
业务通用Prompt模板定义，便于多Agent系统复用和维护。
"""
from langchain.prompts import PromptTemplate

from langchain.prompts import PromptTemplate

def get_consult_prompt():
    """
    咨询场景Prompt（酒店信息/景点推荐）。
    :return: PromptTemplate对象
    """
    return PromptTemplate(
        input_variables=["input"],
        template="""
            你是专业酒店前台客服，善于用简洁语言解答用户关于酒店信息、房型、设施、周边景点等问题。
            用户提问：{input}
            回复要求：
            1. 直接给出准确答案，必要时可推荐景点。
            2. 不要出现“我是AI”或“无法回答”等表述。
            3. 回复字数不超过100字。
        """
    )

def get_booking_prompt():
    """
    预订场景Prompt。
    :return: PromptTemplate对象
    """
    return PromptTemplate(
        input_variables=["input"],
        template="""
            你是酒店预订专员，负责解答和处理用户的房间预订相关请求。
            用户请求：{input}
            回复要求：
            1. 明确告知预订状态、剩余房型、价格等关键信息。
            2. 如有疑问，主动引导用户补充信息。
            3. 回复简洁，避免冗余。
        """
    )

def get_complaint_prompt():
    """
    投诉处理CRISPE模板。
    :return: PromptTemplate对象
    """
    return PromptTemplate(
        input_variables=["input"],
        template="""
            您是一名五星级酒店值班经理（员工编号A100）。用户说：{input}
            请按以下要求处理：
            1. 诚恳承认错误并表达歉意
            2. 提供即时解决方案（换房或合理补偿）
            3. 避免使用"系统问题"等推脱表述
            4. 回复长度不超过80字
            禁用词：不可能/没办法/规定
        """
    )
