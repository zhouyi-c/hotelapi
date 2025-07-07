from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from config import Config
from utils.callback import ConsoleCallbackHandler


class BaseAgent:
    def __init__(self, tools, prompt=None, memory=None,agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION):
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
            callbacks=[ConsoleCallbackHandler()],

        )
        if memory:
            ia_kwargs['memory'] = memory  # 在初始化前设置
        if prompt is not None:
            ia_kwargs['prompt'] = prompt
        self.agent = initialize_agent(**ia_kwargs)

    # base_agent.py
    def run(self, **kwargs):
        """
        重构后的运行方法，正确构建LangChain输入
        """
        # 从kwargs获取必要参数
        user_input = kwargs.get("input") or kwargs.get("query")

        # 处理记忆
        chat_history = ""
        if "memory" in kwargs:
            chat_history = kwargs['memory'].load_memory_variables({}).get("chat_history", "")

        # 根据代理类型构建输入字典
        input_dict = {"input": user_input}

        # 添加历史记录（如果提示词需要）
        if chat_history:
            input_dict["chat_history"] = chat_history

        # 添加工具描述（路由代理需要）
        if hasattr(self, 'tools') and self.tools:
            tool_descriptions = "\n".join([f"- {tool.name}: {tool.description}" for tool in self.tools])
            input_dict["tools"] = tool_descriptions

        try:
            # 使用正确格式调用代理
            return self.agent.run(input_dict)
        except Exception as e:
            return f"代理执行出错: {str(e)}"