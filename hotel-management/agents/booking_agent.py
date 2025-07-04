from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool

from utils.prompts import get_booking_prompt
from utils.memory import create_buffer_memory

class BookingAgent(BaseAgent):
    """
    专家层：预订Agent，负责处理酒店房间预订相关的智能问答或流程。
    支持多会话记忆，供ManagerAgent调用。
    """
    def __init__(self, conversation_id: str = "default"):
        tools = [HotelSearchTool()]
        prompt = get_booking_prompt()
        memory = create_buffer_memory(conversation_id)
        super().__init__(tools)
        self.prompt = prompt
        self.memory = memory

    def handle_booking(self, user_message: str, conversation_id: str = "default") -> str:
        """
        处理预订主流程，自动注入Prompt和历史记忆。
        :param user_message: 用户预订请求内容
        :param conversation_id: 会话ID
        :return: 智能回复文本
        """
        if conversation_id != "default":
            self.memory = create_buffer_memory(conversation_id)
        return self.run(input=user_message, prompt=self.prompt, memory=self.memory)
