from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cache import users_cache
from mysql_db.db_service import get_db
from crud import users
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserRegisterRequest
from utils import response
from utils.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["users"])

# 用户注册
@router.post("/register")
async def register(user_data: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    # 注册逻辑：验证用户是否存在 -> 创建用户 → 生成 Token  → 响应结果
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    await users_cache.set_cache_user(user)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return response.success_response(message="注册成功", data=response_data)

# 用户登录
@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户是否存在 -> 验证密码 -> 生成 Token  → 响应结果
    user = await users.authenticate_user(db, user_data)
    token = await users.create_token(db, user.id)
    await users_cache.set_cache_user(user)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(user))
    return response.success_response(message="登录成功", data=response_data)

# 获取用户信息
@router.get("/info")
async def get_user_info(user: UserInfoResponse = Depends(get_current_user)):
    return response.success_response(
        message="获取用户信息成功",
        data=user.dict()
    )
