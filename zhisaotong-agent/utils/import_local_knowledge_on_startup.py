import os
import hashlib

from rabbitmq.rabbitmq_service import rabbit_service
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from utils.config_handler import path_conf
from crud.files import get_file_by_md5, add_file
# 直接使用你已有的单例 session_factory，不经过 get_db()
from mysql_db.db_service import db_service

async def import_local_knowledge_on_startup():
    """
    项目启动时自动导入本地预置知识库
    使用系统用户：SYSTEM_USER_ID = 0
    """
    try:
        # ====================== 配置 ======================
        local_knowledge_dir = get_abs_path(path_conf["local_knowledge_dir"])
        allowed_ext = [".pdf", ".docx", ".txt", ".csv", ".md", ".json"]
        system_user_id = 0

        # 目录不存在则创建
        if not os.path.exists(local_knowledge_dir):
            os.makedirs(local_knowledge_dir, exist_ok=True)
            logger.info(f"📁 已创建本地知识库目录: {path_conf['local_knowledge_dir']}")
            return

        # ====================== ✅ 终极修复：直接使用原生会话 ======================
        # 完全避开你自带事务管理的 get_db()，从根源解决连接争抢
        async with db_service.session_local() as db:
            # 遍历文件
            filenames = os.listdir(local_knowledge_dir)
            if not filenames:
                logger.info("📭 本地知识库目录无文件，跳过导入")
                return

            logger.info(f"🚀 开始自动导入本地知识库，共 {len(filenames)} 个文件")

            for filename in filenames:
                file_full_path = os.path.join(local_knowledge_dir, filename)

                # 跳过文件夹
                if not os.path.isfile(file_full_path):
                    continue

                # 过滤格式
                ext = os.path.splitext(filename)[1].lower()
                if ext not in allowed_ext:
                    logger.info(f"⏭️ 不支持的文件格式，跳过：{filename}")
                    continue

                # 计算 MD5（大文件安全版）
                with open(file_full_path, "rb") as f:
                    md5_obj = hashlib.md5()
                    while chunk := f.read(4096):
                        md5_obj.update(chunk)
                    file_md5 = md5_obj.hexdigest()

                # 去重
                exist_file = await get_file_by_md5(db, file_md5)
                if exist_file:
                    logger.info(f"⏭️ 已存在，跳过：{filename}")
                    continue

                # 文件大小
                file_size = os.path.getsize(file_full_path)

                # 插入文件
                file_data = {
                    "fileName": filename,
                    "fileSize": file_size,
                    "filePath": file_full_path,
                    "fileMd5": file_md5,
                    "userId": system_user_id,
                    "status": 1
                }
                file_record = await add_file(db, file_data)

                # 手动提交（因为我们直接用 session）
                await db.commit()

                # 发送解析任务
                await rabbit_service.send_parse_task(
                    file_id=file_record.id,
                    user_id=system_user_id,
                    file_md5=file_md5,
                    file_path=file_full_path
                )

                logger.info(f"✅ 已加入解析队列：{filename} (系统公共库)")

        logger.info("🎉 本地知识库自动导入完成！")

    except Exception as e:
        logger.error(f"❌ 自动导入失败：{str(e)}", exc_info=True)