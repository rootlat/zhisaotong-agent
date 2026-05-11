from datetime import datetime, timedelta
from starlette import status

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from models.user_token import UserToken
from schemas.users import UserRequest, UserRegisterRequest
from utils import security, jwt
from utils.db_transaction import async_db_transaction_simple

# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 创建用户
@async_db_transaction_simple
async def create_user(db: AsyncSession, user_data: UserRegisterRequest):
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password, phone=user_data.phone)
    db.add(user)
    # 先同步到数据库
    await db.flush()
    # 从数据库读回最新的 user
    await db.refresh(user)
    return user

# 判断用户是否存在和验证密码一致
async def authenticate_user(db: AsyncSession, user_data: UserRequest):
    user = await get_user_by_username(db, user_data.username)
    # 统一提示（安全规范，防止用户名和密码被爆破）
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    if not security.verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    return user

# 生成 Token
@async_db_transaction_simple
async def create_token(db: AsyncSession, user_id: int):
    token = jwt.create_access_token(user_id)
    expires_at = datetime.now() + timedelta(days=7)
    # 查询现有 token
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        # 更新现有记录
        # 修改已托管的对象属性 → 无需add
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        # 创建新记录
        # 新建对象 → 必须add
        user_token = UserToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.add(user_token)
    return token

# 根据用户ID查询数据库
async def get_user_by_id(db: AsyncSession, user_id: int):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


