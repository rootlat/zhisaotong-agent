import os
from fastapi import APIRouter, UploadFile, File, Depends, Path
from utils.md5 import calculate_file_md5
from utils.path_tool import get_abs_path
from utils import response
from utils.auth import get_current_user
from schemas.users import UserInfoResponse
from mysql_db.db_service import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from utils.config_handler import path_conf
from crud.files import (
    add_file,
    get_file_by_md5_and_name,
    get_file_by_name,
    get_files_by_user_id,
    get_file_by_id,
    delete_file_by_id,
    clear_files_by_user_id,
)
from rabbitmq.rabbitmq_service import rabbit_service

router = APIRouter(prefix="/api/file", tags=["file"])
UPLOAD_DIR = get_abs_path(path_conf['upload_file_dir'])
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_file(
        files: list[UploadFile] = File(...),
        user: UserInfoResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    current_file_path = os.path.join(UPLOAD_DIR, f"user-{user.id}")
    os.makedirs(current_file_path, exist_ok=True)

    for file in files:
        if not file.filename:
            continue

        file_content = await file.read()
        file_md5 = await calculate_file_md5(file, file_content)
        filename = file.filename
        file_size = round(len(file_content) / 1024, 4)

        # 重复文件跳过
        exist = await get_file_by_md5_and_name(db, user.id, file_md5, filename)
        if exist:
            continue

        # 同名文件覆盖
        same_name_file = await get_file_by_name(db, user.id, filename)
        if same_name_file:
            same_name_file.fileMd5 = file_md5
            same_name_file.fileSize = file_size
            same_name_file.status = 1
            with open(same_name_file.filePath, "wb") as f:
                f.write(file_content)
            await db.commit()

            await rabbit_service.send_parse_task(
                file_id=same_name_file.id,
                user_id=user.id,
                file_md5=file_md5,
                file_path=same_name_file.filePath
            )
            continue

        # 新文件
        save_path = os.path.join(current_file_path, filename)
        with open(save_path, "wb") as f:
            f.write(file_content)

        file_data = {
            "fileName": filename,
            "fileSize": file_size,
            "filePath": save_path,
            "fileMd5": file_md5,
            "userId": user.id,
            "status": 1
        }

        new_file = await add_file(db, file_data)
        if not new_file:
            continue

        await rabbit_service.send_parse_task(
            file_id=new_file.id,
            user_id=user.id,
            file_md5=file_md5,
            file_path=save_path
        )

    return response.success_response(message="上传成功，已进入队列解析")


@router.get("/list")
async def get_file_list(
        user: UserInfoResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    files = await get_files_by_user_id(db, user.id)
    return response.success_response(data=files)


@router.delete("/delete/{file_id}")
async def delete_file(
    file_id: int = Path(...),
    user: UserInfoResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. 使用 CRUD 函数查询
    file_info = await get_file_by_id(db, file_id, user.id)
    if not file_info:
        return response.success_response(message="文件不存在或无权限")

    # 2. 使用 CRUD 函数删除数据库记录
    await delete_file_by_id(db, file_id, user.id)

    # 3. 删除本地文件
    try:
        if os.path.exists(file_info.filePath):
            os.remove(file_info.filePath)
    except Exception as e:
        print("删除本地文件失败：", e)

    # 4. 删除 Milvus 向量
    try:
        from rag.milvus.milvus_service import milvus_service
        milvus_service.delete_file_data(file_id=file_id, user_id=user.id)
    except Exception as e:
        print("删除向量失败：", e)

    return response.success_response(message="删除成功")



@router.delete("/clearAll")
async def clear_all_files(
    user: UserInfoResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    file_list = await get_files_by_user_id(db, user.id)
    if not file_list:
        return response.success_response(message="暂无文件可清空")

    # 使用 CRUD 函数清空
    await clear_files_by_user_id(db, user.id)

    # 清空本地文件夹
    user_folder = os.path.join(UPLOAD_DIR, f"user-{user.id}")
    try:
        if os.path.exists(user_folder):
            for f in os.listdir(user_folder):
                os.remove(os.path.join(user_folder, f))
    except Exception as e:
        print("清空文件夹失败：", e)

    # 清空 Milvus
    try:
        from rag.milvus.milvus_service import milvus_service
        milvus_service.clear_user_data(user.id)
    except Exception as e:
        print("清空向量失败：", e)

    return response.success_response(message="已清空所有文件")