# 协调层 ManagerAgent：负责任务分解、意图识别、任务路由到专家Agent
from agents.consult_agent import ConsultAgent
from agents.booking_agent import BookingAgent
from agents.complaint_agent import ComplaintAgent

class ManagerAgent:
    def __init__(self):
        self.consult_agent = ConsultAgent()
        self.booking_agent = BookingAgent()
        self.complaint_agent = ComplaintAgent()

    def route_task(self, user_input: str, conversation_id: str = "default"):
        """
        任务分流，根据意图路由到不同专家Agent。
        :param user_input: 用户输入内容
        :param conversation_id: 会话ID
        :return: 智能回复文本
        """
        # 简单意图识别，可替换为LLM或更复杂NLU
        if "投诉" in user_input:
            return self.complaint_agent.handle_complaint(user_input, conversation_id)
        elif "预订" in user_input or "订房" in user_input:
            return self.booking_agent.handle_booking(user_input, conversation_id)
        else:
            return self.consult_agent.handle_consult(user_input, conversation_id)
