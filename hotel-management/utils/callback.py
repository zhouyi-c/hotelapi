from langchain_core.callbacks import BaseCallbackHandler


class ConsoleCallbackHandler(BaseCallbackHandler):
    """增强版ReAct回调处理器"""

    def on_llm_start(self, serialized, prompts, **kwargs):
        print(f"\n[思考开始] 正在分析用户请求...")

    def on_agent_action(self, action, **kwargs):
        if action.tool:
            print(f"\n[行动决策] 选择工具: {action.tool}")
            print(f"[参数输入] {action.tool_input}")
        else:
            print(f"\n[思考过程] {action.log}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"[工具执行] 开始: {serialized.get('name')}")

    def on_tool_end(self, output, **kwargs):
        print(f"[工具结果] 输出: {output}")

    def on_agent_finish(self, finish, **kwargs):
        print(f"\n[处理完成] 最终结果: {finish.return_values['output']}")