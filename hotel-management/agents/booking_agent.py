from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool

class BookingAgent(BaseAgent):
    """
    预订Agent，负责处理酒店房间预订相关的智能问答或流程。
    可组合酒店搜索、预订等相关工具。
    """
    def __init__(self):
        tools = [HotelSearchTool()]
        # 若有专门的预订Tool，可在此添加
        super().__init__(tools)

    def handle_booking(self, user_message: str) -> str:
        """
        处理预订主流程，调用底层Agent能力。
        :param user_message: 用户预订请求内容
        :return: 智能回复文本
        """
        return self.run(user_message)
