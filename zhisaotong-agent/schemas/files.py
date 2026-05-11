from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


# ==================== 文件基础模型 ====================
class FileBase(BaseModel):
    """
    文件信息基础数据模型
    """
    fileName: Optional[str] = Field(None, description="文件名")
    fileSize: Optional[float] = Field(None, description="文件大小(KB)")
    filePath: Optional[str] = Field(None, description="文件存储路径")
    fileMd5: Optional[str] = Field(None, description="文件MD5值")
    userId: Optional[int] = Field(None, description="所属用户ID")
    status: Optional[int] = Field(None, description="状态 1—已上传（待解析）2—解析中 3—解析成功 4—解析失败")


# ==================== 文件响应模型 ====================
class FileResponse(FileBase):
    """
    文件列表/详情响应模型
    """
    id: int

    model_config = ConfigDict(
        from_attributes=True,  # 支持 ORM 转 Pydantic
    )


class FileUploadResponse(BaseModel):
    """
    文件上传完成响应模型
    """
    id: int
    fileName: str
    status: int

    model_config = ConfigDict(
        from_attributes=True,
    )