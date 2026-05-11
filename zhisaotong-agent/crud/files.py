from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.files import FileModel
from utils.db_transaction import async_db_transaction_simple

@async_db_transaction_simple
async def add_file(db: AsyncSession, file_data: dict):
    db_file = FileModel(**file_data)
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file

# 根据用户ID查询文件列表
async def get_files_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(FileModel).where(FileModel.userId == user_id))
    return result.scalars().all()

# 规则1专用：根据 用户ID + MD5 + 文件名 查唯一文件
async def get_file_by_md5_and_name(db: AsyncSession, user_id: int, md5: str, filename: str):
    query = select(FileModel).where(
        FileModel.userId == user_id,
        FileModel.fileMd5 == md5,
        FileModel.fileName == filename
    )
    result = await db.execute(query)
    return result.scalars().first()

# 规则3专用：根据 用户ID + 文件名 查文件
async def get_file_by_name(db: AsyncSession, user_id: int, file_name: str):
    result = await db.execute(
        select(FileModel).where(
            FileModel.userId == user_id,
            FileModel.fileName == file_name
        )
    )
    return result.scalars().first()

# 兼容保留：根据 用户ID + MD5 查询
async def get_file_by_file_md5(db: AsyncSession, user_id: int, md5_file: str):
    query = select(FileModel).where(
        FileModel.userId == user_id,
        FileModel.fileMd5 == md5_file
    )
    result = await db.execute(query)
    return result.scalars().first()


@async_db_transaction_simple
async def update_file_status(db: AsyncSession, file_id: int, status: int):
    await db.execute(
        update(FileModel)
        .where(FileModel.id == file_id)
        .values(status=status)
    )


# 根据 ID 查询文件
async def get_file_by_id(db: AsyncSession, file_id: int, user_id: int):
    result = await db.execute(
        select(FileModel).filter(FileModel.id == file_id, FileModel.userId == user_id)
    )
    return result.scalar_one_or_none()

# 根据 ID 删除文件
@async_db_transaction_simple
async def delete_file_by_id(db: AsyncSession, file_id: int, user_id: int):
    await db.execute(
        delete(FileModel).where(FileModel.id == file_id, FileModel.userId == user_id)
    )

# 清空用户所有文件
@async_db_transaction_simple
async def clear_files_by_user_id(db: AsyncSession, user_id: int):
    await db.execute(delete(FileModel).where(FileModel.userId == user_id))


async def get_file_by_md5(db: AsyncSession, file_md5: str):
    result = await db.execute(
        select(FileModel).where(FileModel.fileMd5 == file_md5)
    )
    return result.scalars().first()