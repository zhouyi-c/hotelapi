from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool

from utils.prompts import get_complaint_prompt
from utils.memory import create_buffer_memory

class ComplaintAgent(BaseAgent):
    """
    投诉处理Agent，负责处理用户投诉相关的智能问答或流程。
    集成专属Prompt和记忆功能，组合酒店搜索等相关工具。
    """
    def __init__(self, conversation_id: str = "default"):
        tools = [HotelSearchTool()]
        prompt = get_complaint_prompt()
        memory = create_buffer_memory(conversation_id)
        super().__init__(tools)
        self.prompt = prompt
        self.memory = memory

    def handle_complaint(self, user_message: str) -> str:
        """
        处理投诉主流程，调用底层Agent能力，自动注入Prompt和历史记忆。
        :param user_message: 用户投诉内容
        :return: 智能回复文本
        """
        return self.run(input=user_message, prompt=self.prompt, memory=self.memory)
