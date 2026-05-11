from datetime import datetime
from .base import Base
from sqlalchemy import Index, BigInteger, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column


class ChatHistory(Base):
    __tablename__ = "chat_history"

    updated_at = None

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="用户ID")
    session_id: Mapped[str] = mapped_column(String(128), nullable=False, comment="会话ID")
    role: Mapped[str] = mapped_column(String(20), nullable=False, comment="user/assistant")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="内容")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    __table_args__ = (
        Index("idx_user_session", "user_id", "session_id"),
    )