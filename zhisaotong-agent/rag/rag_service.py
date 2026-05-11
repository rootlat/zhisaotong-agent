from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from models.factory import chat_model
from utils.prompt_loader import load_rag_prompts
from rag.milvus.milvus_service import milvus_service
from rag.embed.embedding_service import embedding_service
from utils.logger_handler import logger
from utils.config_handler import milvus_conf
from rag.rerank import bm25_service


def print_prompt(prompt):
    logger.info("=" * 20)
    logger.info(prompt.to_string())
    logger.info("=" * 20)
    return prompt

print_prompt_runnable = RunnableLambda(print_prompt)

class RagSummarizeService:
    def __init__(self):
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = self._init_chain()
        self.bm25 = bm25_service.BM25Service()

    def _init_chain(self):
        return self.prompt_template | print_prompt_runnable | self.model | StrOutputParser()

    async def retrieve_context(self, query: str, user_id: int, top_k=milvus_conf["k"]):
        try:
            query_vector = await embedding_service.embed_query(query)

            vector_result1 = milvus_service.search(vector=query_vector, user_id=user_id, limit=top_k)
            vector_result2 = milvus_service.search(vector=query_vector, user_id=0, limit=top_k)

            hits = []
            if vector_result1: hits += vector_result1[0]
            if vector_result2: hits += vector_result2[0]

            vector_docs = [h["entity"]["content"] for h in hits]

            bm25_docs = self.bm25.search_with_public(user_id, query, top_k)

            seen = set()
            merged_docs = []
            for doc in vector_docs + bm25_docs:
                if doc not in seen:
                    seen.add(doc)
                    merged_docs.append(doc)

            if not merged_docs:
                return ""

            top_docs = merged_docs[:milvus_conf["top"]]

            return "\n".join(f"【参考资料{i + 1}】{doc}" for i, doc in enumerate(top_docs))

        except Exception as e:
            logger.error(f"Hybrid检索失败：{e}", exc_info=True)
            return ""

    async def rag_summarize(self, query: str, user_id: int) -> str:
        try:
            context = await self.retrieve_context(query, user_id)
            if not context:
                return "抱歉，没有找到相关资料"

            return await self.chain.ainvoke({
                "input": query,
                "context": context,
            })
        except Exception as e:
            logger.error(f"RAG失败：{e}", exc_info=True)
            return "查询失败"

rag_service = RagSummarizeService()