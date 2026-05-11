from rank_bm25 import BM25Okapi
import jieba
from typing import List, Dict


class BM25Service:
    def __init__(self):
        # 数据结构：
        # key: user_id (int)
        # value: dict {
        #   "indexed_chunks": List[Tuple[file_id, content]]
        #   "bm25_model": BM25Okapi | None
        #   "tokenized_chunks": List[List[str]]
        # }
        self.user_data: Dict[int, Dict] = {}

    def _get_or_create_user_space(self, user_id: int) -> Dict:
        """获取或初始化用户的索引空间"""
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "indexed_chunks": [],
                "bm25_model": None,
                "tokenized_chunks": []
            }
        return self.user_data[user_id]

    def add_documents(self, user_id: int, file_id: int, docs: List[str]):
        """新增文档（增量添加）"""
        space = self._get_or_create_user_space(user_id)
        for content in docs:
            space["indexed_chunks"].append((file_id, content))
        self._rebuild_index(user_id)

    def _rebuild_index(self, user_id: int):
        """内部方法：重建指定用户的 BM25 索引"""
        space = self._get_or_create_user_space(user_id)
        all_contents = [content for (_, content) in space["indexed_chunks"]]
        if not all_contents:
            space["bm25_model"] = None
            space["tokenized_chunks"] = []
            return
        space["tokenized_chunks"] = [list(jieba.cut(doc)) for doc in all_contents]
        space["bm25_model"] = BM25Okapi(space["tokenized_chunks"])


    def search(self, user_id: int, query: str, top_k=5) -> List[str]:
        """搜索（仅搜索当前用户的数据）"""
        space = self._get_or_create_user_space(user_id)
        if not space["bm25_model"]:
            return []

        tokenized_query = list(jieba.cut(query))
        scores = space["bm25_model"].get_scores(tokenized_query)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        all_contents = [content for (_, content) in space["indexed_chunks"]]
        return [all_contents[i] for i, _ in ranked[:top_k]]


    def search_with_public(self, user_id: int, query: str, top_k=5) -> List[str]:
        """
        搜索：自己的数据 + 系统公共数据（user_id=0）
        自动合并、去重、排序
        """
        # 1. 搜自己
        user_docs = self.search(user_id, query, top_k)

        # 2. 搜公共库（系统预置知识）
        public_docs = self.search(0, query, top_k)

        # 3. 合并 + 去重 + 保持顺序
        seen = set()
        combined = []
        for doc in user_docs + public_docs:
            if doc not in seen:
                seen.add(doc)
                combined.append(doc)

        return combined[:top_k]


    def delete_by_file_id(self, user_id: int, file_id: int):
        if user_id not in self.user_data:
            return
        space = self.user_data[user_id]
        space["indexed_chunks"] = [
            (fid, content) for (fid, content) in space["indexed_chunks"]
            if fid != file_id
        ]
        self._rebuild_index(user_id)

    def clear_by_user_id(self, user_id: int):
        if user_id in self.user_data:
            del self.user_data[user_id]