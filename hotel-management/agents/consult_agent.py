
from agents.base_agent import BaseAgent
from langchain.agents import AgentType
from tools.hotel_tool import HotelSearchTool
from tools.attraction_tool import AttractionRecommendTool
from  tools.knowledge_tool import KnowledgeBaseTool
from utils.prompts import get_consult_prompt
from utils.memory import create_buffer_memory
from langchain.callbacks.stdout import StdOutCallbackHandler  # 添加标准输出回调


class ConsultAgent(BaseAgent):
    """
    专家层：咨询Agent（集成ReAct框架）
    负责解答用户关于酒店、房型、设施、周边等问题。
    """

    def __init__(self, conversation_id: str = "default"):
        tools = [HotelSearchTool(), AttractionRecommendTool(),KnowledgeBaseTool()]
        prompt = get_consult_prompt()
        memory = create_buffer_memory(conversation_id)

        # 初始化BaseAgent并强制开启思考过程
        super().__init__(
            tools=tools,
            prompt=prompt,
            agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
        )

        # 启用详细思考日志
        self.agent.agent.llm_chain.verbose = True  # 核心修改：打印推理步骤

        # 添加控制台回调处理器
        self.agent.callbacks.append(StdOutCallbackHandler())

        self.memory = memory

    def handle_consult(self, user_message: str, conversation_id: str = "default") -> str:
        """
        处理咨询主流程（集成ReAct）
        """
        if conversation_id != "default":
            self.memory = create_buffer_memory(conversation_id)

        # 使用ReAct框架处理请求
        return self.run(input=user_message, memory=self.memory)