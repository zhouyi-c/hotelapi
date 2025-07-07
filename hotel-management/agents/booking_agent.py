from .base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool, HotelBookingTool
from utils.prompts import get_booking_prompt
from utils.memory import get_session_memory


class BookingAgent(BaseAgent):
    """
    专家层：预订Agent，负责处理酒店房间预订相关的智能问答或流程。
    支持多轮交互收集预订信息。
    """

    def __init__(self, conversation_id: str = "default"):
        tools = [HotelSearchTool(), HotelBookingTool()]  # 添加预订工具
        prompt = get_booking_prompt()
        memory = get_session_memory(conversation_id)
        super().__init__(tools, prompt=prompt)
        self.memory = memory
        self.conversation_id = conversation_id

    def handle_booking(self, user_message: str, conversation_id: str = "default") -> str:
        if conversation_id != self.conversation_id:
            self.memory = get_session_memory(conversation_id)
            self.conversation_id = conversation_id

        # 使用Agent处理预订请求
        return self.run(
            input=user_message,
            memory=self.memory,
            conversation_id=conversation_id
        )