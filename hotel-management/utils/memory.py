"""
对话记忆功能封装，支持多Agent共享和扩展。
新增会话记忆管理中心，实现长期记忆功能。
"""
from langchain.memory import ConversationBufferMemory
# 全局会话记忆存储 {session_id: memory_obj}
session_memories = {}

def get_session_memory(session_id: str) -> ConversationBufferMemory:
    """
    获取或创建指定会话ID的记忆对象。
    :param session_id: 会话唯一标识
    :return: ConversationBufferMemory实例
    """
    if session_id not in session_memories:
        # 创建新的记忆对象并存储
        session_memories[session_id] = ConversationBufferMemory(memory_key="chat_history")
    return session_memories[session_id]

def clear_session_memory(session_id: str):
    """
    清除指定会话的记忆
    :param session_id: 会话唯一标识
    """
    if session_id in session_memories:
        del session_memories[session_id]

# 添加兼容函数
def create_buffer_memory(conversation_id: str = "default"):
    """
    兼容旧版代码的函数，实际调用 get_session_memory
    """
    return get_session_memory(conversation_id)