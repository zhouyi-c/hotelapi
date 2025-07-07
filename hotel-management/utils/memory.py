"""
对话记忆功能封装，支持多Agent共享和扩展。
"""
from langchain.memory import ConversationBufferMemory

def create_buffer_memory(conversation_id: str = "default"):
    """
    创建对话缓冲记忆对象。
    :param conversation_id: 会话唯一标识
    :return: ConversationBufferMemory实例
    """
    return ConversationBufferMemory(memory_key=conversation_id)
