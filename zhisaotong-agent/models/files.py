from datetime import datetime

from .base import Base

from sqlalchemy import Index, Integer, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column


class FileModel(Base):
    """
    文件管理表ORM模型
    """
    __tablename__ = 'file'

    __table_args__ = (
        Index('idx_user_id', 'userId'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="文件ID")
    fileName: Mapped[str] = mapped_column(String(255), nullable=False, comment="文件名")
    fileSize: Mapped[float] = mapped_column(Float, nullable=False, comment="文件大小（KB）")
    filePath: Mapped[str] = mapped_column(String(512), nullable=False, comment="文件存储路径")
    fileMd5: Mapped[str] = mapped_column(String(32), nullable=False, comment="文件MD5值，用于去重")
    userId: Mapped[int] = mapped_column(Integer, nullable=False, comment="上传用户ID")
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="状态 1—已上传（待解析）2—解析中 3—解析成功 4—解析失败")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(), comment="更新时间")

    def __repr__(self):
        return f"<FileModel(id={self.id}, fileName='{self.fileName}', status={self.status})>"