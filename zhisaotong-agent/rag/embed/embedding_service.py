import asyncio
import os
from langchain_community.embeddings import DashScopeEmbeddings
from utils.config_handler import rag_conf
from utils.logger_handler import logger


class EmbeddingService:
    """
    向量化服务封装
    统一风格、全局单例、异步安全
    与 Milvus、RabbitMQ、VectorStore 保持一致
    """
    def __init__(self):
        self.model = rag_conf["embedding_model_name"]
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.embedding = None

    def init(self):
        """初始化 embedding 模型（全局一次）"""
        try:
            self.embedding = DashScopeEmbeddings(
                model=self.model,
                dashscope_api_key=self.api_key
            )
            logger.info(f"✅ Embedding 模型初始化完成：{self.model}")
        except Exception as e:
            logger.error(f"❌ Embedding 初始化失败：{str(e)}", exc_info=True)

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """批量文本向量化（异步安全）"""
        if not self.embedding:
            raise Exception("Embedding 未初始化，请先调用 init()")

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self.embedding.embed_documents,
            texts
        )

    async def embed_query(self, text: str) -> list[float]:
        """用户问题向量化"""
        if not self.embedding:
            raise Exception("Embedding 未初始化，请先调用 init()")

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self.embedding.embed_query,
            text
        )


# ====================== 全局单例 ======================
embedding_service = EmbeddingService()