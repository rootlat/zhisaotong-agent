from datetime import datetime, timedelta
from jose import JWTError, jwt

from schemas.token import TokenData
from utils.config_handler import jwt_conf
from utils.logger_handler import logger

# 配置项
SECRET_KEY = jwt_conf['secret_key']
ALGORITHM = jwt_conf['algorithm']
ACCESS_TOKEN_EXPIRE_TIME = jwt_conf['access_token_expire_time']


# 创建 access token
def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证 token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return TokenData(user_id=int(user_id))
    except JWTError as e:
        logger.error("验证失败原因", exc_info=e)
        return None