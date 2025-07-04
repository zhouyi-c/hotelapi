from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool

class ComplaintAgent(BaseAgent):
    """
    投诉处理Agent，负责处理用户投诉相关的智能问答或流程。
    组合酒店搜索等相关工具，根据业务需要可扩展更多投诉处理工具。
    """
    def __init__(self):
        tools = [HotelSearchTool()]
        # 可根据实际业务扩展更多投诉相关Tool
        super().__init__(tools)

    def handle_complaint(self, user_message: str) -> str:
        """
        处理投诉主流程，调用底层Agent能力。
        :param user_message: 用户投诉内容
        :return: 智能回复文本
        """
        return self.run(user_message)
