from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, desc, and_
from models.chat_history import ChatHistory
from utils.db_transaction import async_db_transaction_simple


# 保存用户消息
@async_db_transaction_simple
async def save_user_message(db: AsyncSession, user_id: int, session_id: str, content: str):
    msg = ChatHistory(
        user_id=user_id,
        session_id=session_id,
        role="user",
        content=content
    )
    db.add(msg)


# 保存AI消息
@async_db_transaction_simple
async def save_ai_message(db: AsyncSession, user_id: int, session_id: str, content: str):
    msg = ChatHistory(
        user_id=user_id,
        session_id=session_id,
        role="assistant",
        content=content
    )
    db.add(msg)


# 获取会话消息
async def get_session_messages(db: AsyncSession, user_id: int, session_id: str):
    res = await db.execute(
        select(ChatHistory)
        .where(ChatHistory.user_id == user_id, ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at)
    )
    return res.scalars().all()


async def get_user_sessions(db: AsyncSession, user_id: int):
    # 子查询：每个会话 最后一条用户消息
    last_user_msg_subquery = (
        select(
            ChatHistory.session_id,
            ChatHistory.content.label("last_user_content"),
            func.row_number().over(
                partition_by=ChatHistory.session_id,
                order_by=desc(ChatHistory.created_at)
            ).label("rn")
        )
        .where(
            ChatHistory.user_id == user_id,
            ChatHistory.role == "user"
        )
        .subquery()
    )

    result = await db.execute(
        select(
            ChatHistory.session_id,
            func.max(ChatHistory.created_at).label("created_at"),
            last_user_msg_subquery.c.last_user_content
        )
        .outerjoin(
            last_user_msg_subquery,
            and_(
                ChatHistory.session_id == last_user_msg_subquery.c.session_id,
                last_user_msg_subquery.c.rn == 1
            )
        )
        .where(ChatHistory.user_id == user_id)
        .group_by(ChatHistory.session_id, last_user_msg_subquery.c.last_user_content)
        .order_by(func.max(ChatHistory.created_at).desc())
    )

    sessions = []
    for row in result.all():
        title = row.last_user_content or "新对话"
        if len(title) > 18:
            title = title[:18] + "..."

        sessions.append({
            "id": row.session_id,
            "title": title,
            "created_at": row.created_at
        })
    return sessions


# 删除单个会话
@async_db_transaction_simple
async def delete_session_by_id(db: AsyncSession, user_id: int, session_id: str):
    await db.execute(
        delete(ChatHistory).where(
            ChatHistory.user_id == user_id,
            ChatHistory.session_id == session_id
        )
    )


# 清空所有会话
@async_db_transaction_simple
async def clear_all_user_sessions(db: AsyncSession, user_id: int):
    await db.execute(
        delete(ChatHistory).where(ChatHistory.user_id == user_id)
    )