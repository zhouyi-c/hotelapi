from langchain.callbacks.base import BaseCallbackHandler

class ConsoleCallbackHandler(BaseCallbackHandler):
    """自定义回调处理器，用于打印Agent内部决策过程"""

    def on_agent_action(self, action, **kwargs):
        print(f"\n[Agent决策] 选择工具: {action.tool}")
        print(f"[参数输入] {action.tool_input}")

    def on_agent_finish(self, finish, **kwargs):
        print(f"\n[Agent完成] 最终输出: {finish.return_values['output']}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        print(f"\n[工具执行] 开始: {serialized.get('name')} | 输入: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print(f"[工具结果] 输出: {output}")