from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from config import Config
from utils.callback import ConsoleCallbackHandler


class BaseAgent:
    def __init__(self, tools, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION):
        self.llm = ChatOpenAI(
            api_key=Config.QIANFAN_API_KEY,
            base_url=Config.QIANFAN_BASE_URL,
            model=Config.QIANFAN_MODEL,
            temperature=0.7
        )

        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=agent_type,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
            early_stopping_method="generate",
            callbacks=[ConsoleCallbackHandler()]
        )

    def run(self, query: str):
        return self.agent.run(query)