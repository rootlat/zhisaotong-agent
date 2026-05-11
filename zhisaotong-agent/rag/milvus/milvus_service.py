from pymilvus import MilvusClient, DataType
from utils.config_handler import milvus_conf
from utils.logger_handler import logger


class MilvusService:
    """
    Milvus 向量库服务层
    完全类封装，生产级标准
    """

    def __init__(self):
        self.client = MilvusClient(
            uri=f"http://{milvus_conf['host']}:{milvus_conf['port']}",
            token=f"{milvus_conf['user']}:{milvus_conf['password']}"
        )
        self.collection_name = milvus_conf["collection"]
        self.embedding_dim = milvus_conf.get("embedding_dim", 1024)

    def init_collection(self):
        try:
            if self.client.has_collection(self.collection_name):
                logger.info(f"✅ Milvus集合已存在：{self.collection_name}")
                return

            schema = self.client.create_schema(
                auto_id=True,
                enable_dynamic_field=False
            )

            schema.add_field(
                field_name="id",
                datatype=DataType.INT64,
                is_primary=True,
                auto_id=True
            )

            schema.add_field(
                field_name="file_id",
                datatype=DataType.INT64
            )

            schema.add_field(
                field_name="user_id",  # 用户ID
                datatype=DataType.INT64
            )

            schema.add_field(
                field_name="file_md5",
                datatype=DataType.VARCHAR,
                max_length=64
            )

            schema.add_field(
                field_name="content",
                datatype=DataType.VARCHAR,
                max_length=65535
            )

            schema.add_field(
                field_name="vector",
                datatype=DataType.FLOAT_VECTOR,
                dim=self.embedding_dim
            )

            index_params = self.client.prepare_index_params()

            index_params.add_index(
                field_name="vector",
                index_type="HNSW",
                metric_type="COSINE",
                params={"M": 16, "efConstruction": 200}
            )

            self.client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params
            )

            logger.info(f"✅ Milvus集合创建成功：{self.collection_name}")

        except Exception as e:
            logger.error(f"❌ Milvus初始化失败：{e}", exc_info=True)

    def has_md5(self, md5_value: str) -> bool:
        try:
            res = self.client.query(
                collection_name=self.collection_name,
                filter=f"file_md5 == '{md5_value}'",
                limit=1
            )
            return len(res) > 0
        except Exception as e:
            logger.error(f"查询MD5失败：{e}")
            return False

    def insert_chunks(self, chunks: list) -> dict:
        try:
            result = self.client.insert(
                collection_name=self.collection_name,
                data=chunks
            )
            logger.info(f"✅ 插入 {len(chunks)} 条向量成功")
            return result
        except Exception as e:
            logger.error(f"❌ 插入向量失败：{str(e)}", exc_info=True)
            return {}

    def search(self, vector: list, user_id: int = None, limit: int = milvus_conf["limit"]):
        """向量检索（RAG核心）"""
        filter_expr = ""

        if user_id is not None:
            filter_expr = f"user_id == {user_id}"

        return self.client.search(
            collection_name=self.collection_name,
            data=[vector],
            filter=filter_expr,
            limit=limit,
            output_fields=["id", "file_id", "user_id", "file_md5", "content"]
        )


    def delete_file_data(self, file_id: int, user_id: int):
        """
        删除单个文件的所有向量
        给文件删除接口用
        """
        try:
            filter_expr = f"file_id == {file_id} && user_id == {user_id}"
            self.client.delete(
                collection_name=self.collection_name,
                filter=filter_expr
            )
            logger.info(f"✅ 删除文件向量成功 | file_id={file_id} user_id={user_id}")
        except Exception as e:
            logger.error(f"❌ 删除文件向量失败：{e}")

    def clear_user_data(self, user_id: int):
        """
        清空某个用户的所有向量数据
        给清空所有文件接口用
        """
        try:
            filter_expr = f"user_id == {user_id}"
            self.client.delete(
                collection_name=self.collection_name,
                filter=filter_expr
            )
            logger.info(f"✅ 清空用户向量成功 | user_id={user_id}")
        except Exception as e:
            logger.error(f"❌ 清空用户向量失败：{e}")


# ====================== 全局单例 ======================
milvus_service = MilvusService()