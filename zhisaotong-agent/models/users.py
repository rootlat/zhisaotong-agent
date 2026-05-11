from datetime import datetime
from typing import Optional

from .base import Base

from sqlalchemy import Index, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    """
    用户信息表ORM模型
    """
    __tablename__ = 'user'

    # 创建索引
    __table_args__ = (
        Index('username_UNIQUE', 'username'),
        Index('phone_UNIQUE', 'phone'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=False, comment="手机号")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码（加密存储）")
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="状态 0-禁用 1-正常")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(),
                                                 comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', phone='{self.phone}')>"


