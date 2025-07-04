from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from config import Config
from utils.callback import ConsoleCallbackHandler


class BaseAgent:
    def __init__(self, tools, prompt=None, agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION):
        self.llm = ChatOpenAI(
            api_key=Config.QIANFAN_API_KEY,
            base_url=Config.QIANFAN_BASE_URL,
            model=Config.QIANFAN_MODEL,
            temperature=0.7
        )

        ia_kwargs = dict(
            tools=tools,
            llm=self.llm,
            agent=agent_type,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
            early_stopping_method="generate",
            callbacks=[ConsoleCallbackHandler()]
        )
        if prompt is not None:
            ia_kwargs['prompt'] = prompt
        self.agent = initialize_agent(**ia_kwargs)

    def run(self, query: str = None, **kwargs):
        """
        支持传递prompt、memory等参数，自动适配langchain新版API。
        - 仅有query时，直接传递query。
        - 若有prompt、memory等参数（如input、prompt、memory），则全部用kwargs传递，确保模板生效。
        【注意】如未传递input参数，模板不会生效，务必保证调用时input字段传递用户输入。
        """
        if kwargs:
            # 只用关键词参数（如prompt、memory、input等），不混用位置参数
            return self.agent.run(**kwargs)
        else:
            return self.agent.run(query)