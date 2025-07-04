from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool
from tools.attraction_tool import AttractionRecommendTool

class ConsultAgent(BaseAgent):
    """
    咨询Agent，负责解答用户关于酒店、房型、设施、周边等问题。
    组合酒店搜索和景点推荐等相关工具。
    """
    def __init__(self):
        tools = [HotelSearchTool(), AttractionRecommendTool()]
        super().__init__(tools)

    def handle_consult(self, user_message: str) -> str:
        """
        处理咨询主流程，调用底层Agent能力。
        :param user_message: 用户咨询内容
        :return: 智能回复文本
        """
        return self.run(user_message)
