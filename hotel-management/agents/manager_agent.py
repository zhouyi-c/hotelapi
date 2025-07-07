from langchain import memory

# 协调层 ManagerAgent：负责任务分解、意图识别、任务路由到专家Agent
from .consult_agent import ConsultAgent
from .booking_agent import BookingAgent
from .complaint_agent import ComplaintAgent
from .base_agent import BaseAgent
from langchain.tools import Tool
from config import Config
from utils.prompts import get_routing_prompt
from langchain.agents import AgentType
from utils.memory import get_session_memory, clear_session_memory  # 更新导入


class ManagerAgent(BaseAgent):
    """
    智能路由管理器，继承自BaseAgent
    负责将用户请求路由到合适的专家Agent
    """

    def __init__(self, conversation_id: str = "default"):
        self.memory = get_session_memory(conversation_id)
        self.current_conversation_id = conversation_id  # 存储当前会话ID

        # 初始化专家Agent
        self.consult_agent = ConsultAgent(conversation_id)
        self.booking_agent = BookingAgent(conversation_id)
        self.complaint_agent = ComplaintAgent(conversation_id)

        # 创建工具集
        self.tools = self._define_expert_tools()

        # 获取路由专用提示词
        prompt = get_routing_prompt()


        # 初始化BaseAgent
        super().__init__(
            tools=self.tools,
            prompt=prompt,
            memory=self.memory,
            agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
        )



    def _define_expert_tools(self):
        """定义专家工具集"""
        return [
            Tool(
                name="投诉专家",
                func=self.complaint_agent.handle_complaint,
                description="处理用户投诉、不满和问题举报"
            ),
            Tool(
                name="预订专家",
                func=self.booking_agent.handle_booking,
                description="处理房间预订、修改和取消，可能涉及多轮交互以收集必要信息"
            ),
            Tool(
                name="咨询专家",
                func=self.consult_agent.handle_consult,
                description="回答一般咨询问题，如政策、服务等"
            ),
            Tool(
                name="后备专家",
                func=lambda q: "抱歉，我没理解您的需求，请换种方式描述您的问题",
                description="当问题无法分类时的默认处理"
            )
        ]

    def route_task(self, user_input: str, conversation_id: str = "default") -> str:
        """
        路由任务到合适的专家Agent
        新增会话记忆管理功能
        :param user_input: 用户输入内容
        :param conversation_id: 会话ID
        :return: 智能回复文本
        """
        # 如果切换了会话，更新记忆
        if conversation_id != self.current_conversation_id:
            self.memory = get_session_memory(conversation_id)
            self.current_conversation_id = conversation_id

        try:
            # 添加当前对话到记忆
            self.memory.chat_memory.add_user_message(user_input)

            # 使用BaseAgent的run方法处理请求
            response = self.run(
                input=user_input,
                memory=self.memory,
                conversation_id=conversation_id
            )

            # 添加AI响应到记忆
            self.memory.chat_memory.add_ai_message(response)
            return response

        except Exception as e:
            # 错误处理 - 使用后备专家
            error_msg = f"系统处理出错: {str(e)}，原始问题: {user_input}"
            self.memory.chat_memory.add_ai_message(error_msg)
            return error_msg

    def reset_conversation(self, conversation_id: str):
        """
        重置指定会话的记忆
        :param conversation_id: 会话ID
        """
        clear_session_memory(conversation_id)
        # 重新初始化记忆
        self.memory = get_session_memory(conversation_id)
        self.current_conversation_id = conversation_id