from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from utils.config_handler import mysql_conf


class DatabaseService:
    def __init__(self):
        self.url = (
            f"mysql+aiomysql://{mysql_conf['user']}:{mysql_conf['password']}"
            f"@{mysql_conf['host']}:{mysql_conf['port']}/{mysql_conf['database']}"
            f"?charset={mysql_conf['charset']}"
        )

        self.engine = create_async_engine(
            self.url,
            echo=mysql_conf["echo"],
            pool_size=mysql_conf["pool_size"],
            max_overflow=mysql_conf["max_overflow"],
        )

        self.session_local = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_db(self):
        async with self.session_local() as session:
            try:
                yield session
                # 路由正常执行完后，commit
                await session.commit()
            except Exception:
                # 发生异常，rollback
                await session.rollback()
                raise


# 全局单例
db_service = DatabaseService()


async def get_db():
    async for session in db_service.get_db():
        yield session