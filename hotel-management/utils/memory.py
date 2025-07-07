"""utils.memory
================
对话记忆功能封装，升级为 **Redis** 持久化版本。

核心特性
---------
1. 使用 ``RedisChatMessageHistory`` 实现**跨进程/长期**对话记忆持久化；
2. 会话 ID 采用 *纯数字* 自增，便于日志排查与定位；
3. 向外暴露与旧版一致的 ``get_session_memory``/``create_buffer_memory``，保证对上层代码零侵入升级；
"""

from __future__ import annotations

from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from redis import Redis

from config import Config

# ---------------------------------------------------------------------------
# Redis 连接设置
# ---------------------------------------------------------------------------
# 单例 Redis 客户端。decode_responses=True 以便直接存储/读取 str 类型。
redis_client: Redis = Redis.from_url(Config.REDIS_URL, decode_responses=True)

# Key 前缀常量，避免与业务其它键冲突
_HISTORY_PREFIX = "session_history:"
_COUNTER_KEY = "session_counter"


# ---------------------------------------------------------------------------
# 会话 ID 生成与管理
# ---------------------------------------------------------------------------

def get_new_session_id() -> str:
    """生成新的会话 ID（从 1 开始的数字字符串）。"""
    return str(redis_client.incr(_COUNTER_KEY))


# ---------------------------------------------------------------------------
# Memory 相关操作
# ---------------------------------------------------------------------------

def get_session_memory(session_id: str) -> ConversationBufferMemory:
    """返回指定 *session_id* 对应的 ``ConversationBufferMemory`` 实例。

    如果尚不存在会自动创建，并通过 ``RedisChatMessageHistory`` 将历史消息存储到
    Redis，确保多进程/多实例间共享持久化。
    """
    chat_history = RedisChatMessageHistory(
        session_id=session_id,
        url=Config.REDIS_URL,
        key_prefix=_HISTORY_PREFIX,
    )
    # return_messages=True：后续可直接在 Agent 中使用 messages
    return ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=True,
    )


def clear_session_memory(session_id: str) -> None:
    """删除指定会话在 Redis 中的全部聊天记录。"""
    redis_client.delete(f"{_HISTORY_PREFIX}{session_id}")


# ---------------------------------------------------------------------------
# 向后兼容（旧代码保留）
# ---------------------------------------------------------------------------

def create_buffer_memory(conversation_id: str = "default") -> ConversationBufferMemory:  # noqa: N802
    """兼容旧函数名，等同于 :func:`get_session_memory`."""
    return get_session_memory(conversation_id)




