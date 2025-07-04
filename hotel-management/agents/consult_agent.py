from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool
from tools.attraction_tool import AttractionRecommendTool

from utils.prompts import get_consult_prompt
from utils.memory import create_buffer_memory

class ConsultAgent(BaseAgent):
    """
    咨询Agent，负责解答用户关于酒店、房型、设施、周边等问题。
    集成专属Prompt和记忆功能，组合酒店搜索和景点推荐等工具。
    """
    def __init__(self, conversation_id: str = "default"):
        tools = [HotelSearchTool(), AttractionRecommendTool()]
        prompt = get_consult_prompt()
        memory = create_buffer_memory(conversation_id)
        super().__init__(tools)
        self.prompt = prompt
        self.memory = memory

    def handle_consult(self, user_message: str) -> str:
        """
        处理咨询主流程，调用底层Agent能力，自动注入Prompt和历史记忆。
        :param user_message: 用户咨询内容
        :return: 智能回复文本
        """
        return self.run(input=user_message, prompt=self.prompt, memory=self.memory)
