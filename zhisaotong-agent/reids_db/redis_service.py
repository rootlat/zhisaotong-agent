import json
import logging
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel
import redis.asyncio as redis
from sqlalchemy import inspect

from utils.config_handler import redis_conf

logger = logging.getLogger(__name__)


class RedisService:
    """
    Redis 缓存服务
    与项目所有服务保持统一封装风格
    自动处理 ORM / 时间 / JSON / 序列化
    """
    def __init__(self):
        # 初始化客户端（单例）
        self.client = redis.Redis(
            host=redis_conf["host"],
            port=redis_conf["port"],
            db=redis_conf["db"],
            decode_responses=True
        )

    @staticmethod
    def orm_to_dict(model):
        """ORM → 字典"""
        return {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}

    def normalize_data(self, data: Any):
        """万能数据清洗"""
        if data is None:
            return None
        if isinstance(data, list):
            return [self.normalize_data(item) for item in data]

        try:
            inspect(data)
            data = self.orm_to_dict(data)
        except:
            pass

        if isinstance(data, dict):
            return {k: self.normalize_data(v) for k, v in data.items()}

        if isinstance(data, BaseModel):
            return self.normalize_data(data.model_dump())

        if isinstance(data, datetime):
            return data.strftime("%Y-%m-%d %H:%M:%S")

        return data

    # ===================== 缓存操作 =====================
    async def get_cache(self, key: str) -> Optional[Any]:
        try:
            data = await self.client.get(key)
            if data is None:
                return None
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return data
        except Exception as e:
            logger.error("获取缓存失败", exc_info=e)
            return None

    async def set_cache(self, key: str, value: Any, expire: int = redis_conf["expire_time"]):
        try:
            value = self.normalize_data(value)
            serialized = json.dumps(value, ensure_ascii=False)
            await self.client.setex(key, expire, serialized)
            return True
        except Exception as e:
            logger.error("设置缓存失败", exc_info=e)
            return False

    async def delete_cache(self, key: str):
        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            logger.error("删除缓存失败", exc_info=e)
            return False

    async def delete_cache_pattern(self, pattern: str) -> int:
        try:
            deleted = 0
            cursor = 0
            while True:
                cursor, keys = await self.client.scan(cursor, match=pattern, count=100)
                if keys:
                    await self.client.delete(*keys)
                    deleted += len(keys)
                if cursor == 0:
                    break
            logger.info(f"删除缓存 pattern={pattern}, 数量={deleted}")
            return deleted
        except Exception as e:
            logger.error(f"批量删除缓存失败 {pattern}", exc_info=e)
            return 0


# ====================== 全局单例 ======================
redis_service = RedisService()