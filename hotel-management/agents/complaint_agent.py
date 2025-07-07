from agents.base_agent import BaseAgent
from tools.hotel_tool import HotelSearchTool

from utils.prompts import get_complaint_prompt
from utils.memory import get_session_memory  # 更新导入

class ComplaintAgent(BaseAgent):
    """
    专家层：投诉处理Agent，负责处理用户投诉相关的智能问答或流程。
    支持多会话记忆，供ManagerAgent调用。
    """
    def __init__(self, conversation_id: str = "default"):
        tools = [HotelSearchTool()]
        prompt = get_complaint_prompt()
        memory = get_session_memory(conversation_id)  # 使用正确的记忆获取函数
        super().__init__(tools, prompt=prompt)
        self.memory = memory
        self.conversation_id = conversation_id  # 添加会话ID跟踪

    def handle_complaint(self, user_message: str, conversation_id: str = "default") -> str:
        """
        处理投诉主流程，自动注入Prompt和历史记忆。
        :param user_message: 用户投诉内容
        :param conversation_id: 会话ID
        :return: 智能回复文本
        """
        # 如果会话ID变更，更新记忆
        if conversation_id != self.conversation_id:
            self.memory = get_session_memory(conversation_id)
            self.conversation_id = conversation_id

        return self.run(input=user_message, memory=self.memory)
