from pydantic import BaseModel

# token 数据模型
class TokenData(BaseModel):
    user_id: int | None = None