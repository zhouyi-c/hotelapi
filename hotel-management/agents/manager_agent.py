
# 协调层 ManagerAgent：负责任务分解、意图识别、任务路由到专家Agent
from .consult_agent import ConsultAgent
from .booking_agent import BookingAgent
from .complaint_agent import ComplaintAgent
from .base_agent import BaseAgent
from langchain.tools import Tool
from config import Config
from utils.prompts import get_routing_prompt
from utils.memory import create_buffer_memory
from langchain.agents import AgentType


class ManagerAgent(BaseAgent):
    """
    智能路由管理器，继承自BaseAgent
    负责将用户请求路由到合适的专家Agent
    """

    def __init__(self, conversation_id: str = "default"):
        # 初始化专家Agent
        self.consult_agent = ConsultAgent(conversation_id)
        self.booking_agent = BookingAgent(conversation_id)
        self.complaint_agent = ComplaintAgent(conversation_id)

        # 创建工具集
        self.tools = self._define_expert_tools()

        # 获取路由专用提示词
        prompt = get_routing_prompt()

        # 创建路由记忆
        memory = create_buffer_memory(conversation_id)

        # 初始化BaseAgent
        super().__init__(
            tools=self.tools,
            prompt=prompt,
            agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION
        )

        # 设置记忆
        self.memory = memory
        self.current_conversation_id = conversation_id  # 存储当前会话ID


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
                description="处理房间预订、修改和取消"
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
        :param user_input: 用户输入内容
        :param conversation_id: 会话ID
        :return: 智能回复文本
        """
        # # 如果切换了会话，更新记忆
        # if conversation_id != self.memory.conversation_id:
        #     self.memory = create_buffer_memory(conversation_id)
        # 如果切换了会话，更新记忆
        if conversation_id != self.current_conversation_id:  # 使用自定义属性
            self.memory = create_buffer_memory(conversation_id)
            self.current_conversation_id = conversation_id  # 更新当前会话ID
        try:
            # 使用BaseAgent的run方法处理请求
            return self.run(
                input=user_input,
                memory=self.memory,
                conversation_id=conversation_id
            )
        except Exception as e:
            # 错误处理 - 使用后备专家
            return self.tools[-1].func(
                f"系统处理出错: {str(e)}，原始问题: {user_input}"
            )
