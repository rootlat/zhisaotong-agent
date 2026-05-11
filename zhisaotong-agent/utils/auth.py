from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from cache import users_cache
from mysql_db.db_service import get_db
from schemas.users import UserInfoResponse
from .jwt import verify_token

async def get_current_user(
        request: Request,
        db: AsyncSession = Depends(get_db)
) -> UserInfoResponse:
    auth_header = request.headers.get("Authorization", "").strip()
    if not auth_header:
        raise HTTPException(401, "请先登录")

    # 正确提取 Bearer token
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    else:
        token = auth_header
    try:
        token_data = verify_token(token)
    except:
        raise HTTPException(401, "登录状态无效")

    user = await users_cache.get_cache_user_by_id(db, user_id=token_data.user_id)

    if not user:
        raise HTTPException(401, "用户不存在")

    return user