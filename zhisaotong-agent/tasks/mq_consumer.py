from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.rerank import bm25_service
from utils.config_handler import milvus_conf
from utils.file_handler import parse_document
from utils.clean_text import clean_text
from rag.embed.embedding_service import embedding_service
from rag.milvus.milvus_service import milvus_service
from crud.files import update_file_status
from mysql_db.db_service import db_service
import asyncio
import traceback

async def parse_handler(msg: dict):
    file_id = None
    try:
        file_id = msg["file_id"]
        user_id = msg["user_id"]
        file_md5 = msg["file_md5"]
        file_path = msg["file_path"]

        async with db_service.session_local() as db:

            # 1. 解析中
            await update_file_status(db, file_id, 2)
            await db.commit()
            print(f"✅ 文件 {file_id} 开始解析")

            # 2. 重复 MD5 跳过
            if milvus_service.has_md5(file_md5):
                await update_file_status(db, file_id, 3)
                await db.commit()
                return

            # 3. 解析文件
            docs = await parse_document(file_path)
            if not docs:
                raise Exception("文件解析为空")

            # 4. 切分
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=milvus_conf["chunk_size"],
                chunk_overlap=milvus_conf["chunk_overlap"],
                separators=milvus_conf["separators"]
            )
            split_docs = splitter.split_documents(docs)

            # 5. 清洗文本
            texts = []
            for d in split_docs:
                content = clean_text(d.page_content).strip()
                if len(content) < 5:
                    continue
                texts.append(content)

            if not texts:
                raise Exception("无有效文本")

            # 6. 向量化
            vectors = await embedding_service.embed_texts(texts)
            print(f"✅ 向量化完成：{len(texts)} 条")

            # 7. 组装数据
            data = [
                {
                    "file_id": file_id,
                    "user_id": user_id,
                    "file_md5": file_md5,
                    "content": t,
                    "vector": v
                }
                for i, (t, v) in enumerate(zip(texts, vectors))
            ]

            # 8. 插入 Milvus
            await asyncio.to_thread(milvus_service.insert_chunks, data)
            print("✅ Milvus 插入成功！")

            # 9. BM25
            await asyncio.to_thread(
                bm25_service.BM25Service().add_documents,
                user_id, file_id, texts
            )

            # 10. 成功
            await update_file_status(db, file_id, 3)
            await db.commit()
            print(f"✅ 文件 {file_id} 全部处理完成！")

    except Exception as e:
        print(f"❌ 解析失败 file_id={file_id}")
        traceback.print_exc()
        try:
            # ✅ 异常也用安全连接
            async with db_service.session_local() as db:
                await update_file_status(db, file_id, 4)
                await db.commit()
        except:
            pass