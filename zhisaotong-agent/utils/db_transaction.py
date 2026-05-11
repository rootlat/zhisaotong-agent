import logging
from functools import wraps
from typing import Callable, Any, Coroutine
from sqlalchemy.ext.asyncio import AsyncSession

# 配置日志
logger = logging.getLogger(__name__)

def async_db_transaction():
    """
    通用异步数据库事务装饰器
    功能：
    1. 自动执行函数逻辑
    2. 异常时自动回滚 + 记录日志
    3. 成功时自动提交
    4. 兼容任意数据库操作函数（新增/修改/删除用户、更新新闻等）
    """
    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)  # 保留原函数的名称和文档字符串
        async def wrapper(db: AsyncSession, *args, **kwargs):
            try:
                # 执行核心业务逻辑（新增/修改/删除等）
                result = await func(db, *args, **kwargs)
                # 逻辑执行成功 → 提交事务
                await db.commit()
                logger.debug(f"函数{func.__name__}数据库操作成功，已提交事务")
                return result
            except Exception as e:
                # 任意异常 → 自动回滚
                await db.rollback()
                logger.error(
                    f"函数{func.__name__}数据库操作失败，已回滚事务 | 异常信息: {str(e)}",
                    exc_info=True  # 记录完整堆栈信息，方便排查
                )
                # 抛出异常让上层处理（缓存层/接口层可捕获）
                raise e
        return wrapper
    return decorator

async_db_transaction_simple = async_db_transaction()