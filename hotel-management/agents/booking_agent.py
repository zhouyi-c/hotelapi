from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool

from utils.prompts import get_booking_prompt
from utils.memory import create_buffer_memory

class BookingAgent(BaseAgent):
    """
    预订Agent，负责处理酒店房间预订相关的智能问答或流程。
    集成专属Prompt和记忆功能，可组合酒店搜索、预订等相关工具。
    """
    def __init__(self, conversation_id: str = "default"):
        tools = [HotelSearchTool()]
        prompt = get_booking_prompt()
        memory = create_buffer_memory(conversation_id)
        super().__init__(tools)
        self.prompt = prompt
        self.memory = memory

    def handle_booking(self, user_message: str) -> str:
        """
        处理预订主流程，调用底层Agent能力，自动注入Prompt和历史记忆。
        :param user_message: 用户预订请求内容
        :return: 智能回复文本
        """
        return self.run(input=user_message, prompt=self.prompt, memory=self.memory)
