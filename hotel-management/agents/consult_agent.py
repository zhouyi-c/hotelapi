from agents.base_agent import BaseAgent
from langchain.agents import AgentType
from tools.hotel_tool import HotelSearchTool
from tools.attraction_tool import AttractionRecommendTool
from tools.knowledge_tool import KnowledgeBaseTool
from utils.prompts import get_consult_prompt
from utils.memory import get_session_memory  # 更新导入
from langchain.callbacks.stdout import StdOutCallbackHandler

class ConsultAgent(BaseAgent):
    """
    专家层：咨询Agent（集成ReAct框架）
    负责解答用户关于酒店、房型、设施、周边等问题。
    """

    def __init__(self, conversation_id: str = "default", memoryv=None):
        tools = [HotelSearchTool(), AttractionRecommendTool(), KnowledgeBaseTool()]
        prompt = get_consult_prompt()
        memory = get_session_memory(conversation_id)  # 使用正确的记忆获取函数

        # 初始化BaseAgent并强制开启思考过程
        super().__init__(
            tools=tools,
            prompt=prompt,
            agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            memory=memory
        )

        # 启用详细思考日志
        self.agent.agent.llm_chain.verbose = True

        # 添加控制台回调处理器
        self.agent.callbacks.append(StdOutCallbackHandler())

        self.memory = memory
        self.conversation_id = conversation_id  # 添加会话ID跟踪

    def handle_consult(self, user_message: str, conversation_id: str = "default") -> str:
        """
        处理咨询主流程（集成ReAct）
        """
        # 如果会话ID变更，更新记忆
        if conversation_id != self.conversation_id:
            self.memory = get_session_memory(conversation_id)
            self.conversation_id = conversation_id

        # 使用ReAct框架处理请求
        return self.run(input=user_message, memory=self.memory)