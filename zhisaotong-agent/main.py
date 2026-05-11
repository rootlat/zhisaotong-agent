import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rabbitmq.rabbitmq_service import rabbit_service
from rag.embed.embedding_service import embedding_service
from rag.milvus.milvus_service import milvus_service
from tasks.mq_consumer import parse_handler
from routers import users, files, chat
from utils import exception_handlers
from rag.rerank.bm25_service import BM25Service
from utils.import_local_knowledge_on_startup import import_local_knowledge_on_startup

app = FastAPI()


# 跨域，添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #允许访问的源
    allow_credentials=True, #允许携带 Cookie
    allow_methods=["*"], #允许所有请求方法
    allow_headers=["*"] #允许所以请求头
)

# 挂载路由/路由注册
app.include_router(users.router)
app.include_router(files.router)
app.include_router(chat.router)

@app.on_event("startup")
async def startup_event():
    milvus_service.init_collection()
    embedding_service.init()
    await rabbit_service.init()

    # 用于清除所有数据。测试时使用
    # bm25 = BM25Service()
    # bm25.clear_by_user_id(1)
    # milvus_service.clear_user_data(1)

    asyncio.create_task(rabbit_service.start_consumer(parse_handler))
    asyncio.create_task(import_local_knowledge_on_startup())

# 注册异常处理器
exception_handlers.register_exception_handlers(app)
