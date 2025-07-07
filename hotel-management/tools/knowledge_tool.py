from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Any, Optional


# 定义输入参数模式
class KnowledgeBaseToolInput(BaseModel):
    query: str = Field(description="用户问题，用于查询酒店知识库")


class KnowledgeBaseTool(BaseTool):
    # 声明所有字段
    name: str = "KnowledgeBaseTool"
    description: str = "使用酒店知识库回答问题"
    args_schema: Type[BaseModel] = KnowledgeBaseToolInput

    # 添加内部状态字段声明
    embeddings: Optional[Any] = None
    vector_db: Optional[Any] = None
    persist_directory: str = "data/chroma_db"

    def __init__(self, file_path: Optional[str] = None):
        super().__init__()

        # --- 路径处理：使用绝对路径避免不同位置执行脚本时出错 --- #
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if file_path is None:
            # 构造默认知识库文件的绝对路径
            file_path = os.path.join(current_dir, '..', 'data', 'knowledge_base.txt')

        # 构造 ChromaDB 持久化目录的绝对路径
        self.persist_directory = os.path.join(current_dir, '..', 'data', 'chroma_db')

        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"知识库文件未找到: {file_path}")

        # 初始化嵌入模型
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        # 加载或创建向量数据库
        if os.path.exists(self.persist_directory):
            self.vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            self._create_vector_db(file_path)

    def _create_vector_db(self, file_path):
        """创建向量数据库"""
        # 加载文本文件
        loader = TextLoader(file_path)
        documents = loader.load()

        # 分割文本
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？"]
        )
        docs = text_splitter.split_documents(documents)

        # 创建向量数据库
        self.vector_db = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        self.vector_db.persist()

    def _run(self, query: str) -> str:
        """
        使用酒店知识库回答问题
        :param query: 用户问题
        :return: 相关知识片段
        """
        # 确保向量数据库已初始化
        if self.vector_db is None:
            raise RuntimeError("向量数据库未初始化")

        # 检索最相关的文档片段
        docs = self.vector_db.similarity_search(query, k=2)

        # 组合检索结果
        context = "\n\n".join([doc.page_content for doc in docs])

        # 格式化响应
        response = f"根据酒店知识库，相关信息如下：\n\n{context}"
        return response