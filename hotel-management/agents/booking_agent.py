from .base_agent import BaseAgent
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
        super().__init__(tools, prompt=prompt)
        self.memory = memory

    def handle_booking(self, user_message: str, conversation_id: str = "default") -> str:
        if conversation_id != "default":
            self.memory = create_buffer_memory(conversation_id)

        # 添加预订核心逻辑
        try:
            # 解析用户请求
            if "豪华大床房" in user_message:
                room_type = "豪华大床房"
            elif "商务套房" in user_message:
                room_type = "商务套房"
            else:
                room_type = None

            # 调用工具获取房间信息
            rooms = HotelSearchTool().run(f"房型={room_type}")

            if rooms:
                # 提取第一个可用房间
                room = rooms[0]
                return (f"找到可用房间：{room['room_type']}，价格：{room['price']}元/晚。"
                        f"是否为您预订？")
            else:
                return "抱歉，目前没有符合要求的可用房间。需要帮您查询其他日期吗？"

        except Exception as e:
            return self.run(input=user_message, memory=self.memory)
