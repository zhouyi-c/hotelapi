#
# # 协调层 ManagerAgent：负责任务分解、意图识别、任务路由到专家Agent
# from .consult_agent import ConsultAgent
# from .booking_agent import BookingAgent
# from .complaint_agent import ComplaintAgent
# from langchain.agents import AgentExecutor, Tool, initialize_agent
# from langchain.agents import AgentType
# from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory
#
#
# class ManagerAgent:
#     def __init__(self):
#         # 初始化专家Agent
#         self.consult_agent = ConsultAgent()
#         self.booking_agent = BookingAgent()
#         self.complaint_agent = ComplaintAgent()
#
#         # 创建工具集
#         self.tools = self._define_expert_tools()
#
#         # 创建路由Agent执行器
#         self.router_agent = self._create_router_agent()
#
#         # 对话历史存储器
#         self.conversation_memory = {}
#
#     def _define_expert_tools(self):
#         """定义专家工具集"""
#         return [
#             Tool(
#                 name="投诉专家",
#                 func=self.complaint_agent.handle_complaint,
#                 description="处理用户投诉、不满和问题举报"
#             ),
#             Tool(
#                 name="预订专家",
#                 func=self.booking_agent.handle_booking,
#                 description="处理房间预订、修改和取消"
#             ),
#             Tool(
#                 name="咨询专家",
#                 func=self.consult_agent.handle_consult,
#                 description="回答一般咨询问题，如政策、服务等"
#             ),
#             Tool(
#                 name="后备专家",
#                 func=lambda q: "抱歉，我没理解您的需求，请换种方式描述您的问题",
#                 description="当问题无法分类时的默认处理"
#             )
#         ]
#
#     def _create_router_agent(self):
#         """创建智能路由Agent"""
#         llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")
#
#         # 使用替代方法创建路由代理
#         agent_executor = initialize_agent(
#             tools=self.tools,
#             llm=llm,
#             agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#             verbose=True,
#             handle_parsing_errors=True,
#             max_iterations=5
#         )
#
#         return agent_executor
#
#     def route_task(self, user_input: str, conversation_id: str = "default"):
#         """
#         智能路由任务到专家Agent
#         :param user_input: 用户输入内容
#         :param conversation_id: 会话ID
#         :return: 智能回复文本
#         """
#         # 获取或创建对话历史
#         history = self.conversation_memory.get(conversation_id, [])
#
#         # 构建包含上下文的输入（保留最近3轮对话）
#         context = "\n".join(history[-3:]) if history else ""
#         full_input = f"{context}\n用户最新消息: {user_input}" if context else user_input
#
#         try:
#             # 使用路由Agent处理
#             result = self.router_agent.run(full_input)
#
#             # 更新对话历史
#             history.append(f"用户: {user_input}")
#             history.append(f"助理: {result}")
#             self.conversation_memory[conversation_id] = history
#
#             return result
#         except Exception as e:
#             # 错误处理
#             error_msg = f"系统处理出错: {str(e)}"
#             return self.tools[-1].func(error_msg)  # 使用后备专家


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
        # 如果切换了会话，更新记忆
        if conversation_id != self.memory.conversation_id:
            self.memory = create_buffer_memory(conversation_id)

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
