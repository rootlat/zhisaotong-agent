from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    question: str

class SessionCreate(BaseModel):
    title: Optional[str] = "新对话"