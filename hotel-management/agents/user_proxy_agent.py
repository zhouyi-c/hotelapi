# 接口层 UserProxyAgent：统一入口，负责接收用户请求、初步解析、转发给ManagerAgent
from agents.manager_agent import ManagerAgent

class UserProxyAgent:
    def __init__(self):
        self.manager = ManagerAgent()

    def handle_request(self, user_input: str, conversation_id: str = "default"):
        """
        统一入口，处理用户请求。
        :param user_input: 用户输入内容
        :param conversation_id: 会话ID
        :return: 智能回复文本
        """
        # 可做初步意图识别、权限校验、日志等
        return self.manager.route_task(user_input, conversation_id)
