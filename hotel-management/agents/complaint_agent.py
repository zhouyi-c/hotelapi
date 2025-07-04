from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool

from utils.prompts import get_complaint_prompt
from utils.memory import create_buffer_memory

class ComplaintAgent(BaseAgent):
    """
    专家层：投诉处理Agent，负责处理用户投诉相关的智能问答或流程。
    支持多会话记忆，供ManagerAgent调用。
    """
    def __init__(self, conversation_id: str = "default"):
        tools = [HotelSearchTool()]
        prompt = get_complaint_prompt()
        memory = create_buffer_memory(conversation_id)
        super().__init__(tools)
        self.prompt = prompt
        self.memory = memory

    def handle_complaint(self, user_message: str, conversation_id: str = "default") -> str:
        """
        处理投诉主流程，自动注入Prompt和历史记忆。
        :param user_message: 用户投诉内容
        :param conversation_id: 会话ID
        :return: 智能回复文本
        """
        if conversation_id != "default":
            self.memory = create_buffer_memory(conversation_id)
        return self.run(input=user_message, prompt=self.prompt, memory=self.memory)
