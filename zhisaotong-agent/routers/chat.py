import asyncio

from fastapi import Depends, Query, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse
import json
from mysql_db.db_service import get_db
from schemas.chat import SessionCreate
from utils.auth import get_current_user
from schemas.users import UserInfoResponse
from crud.chat import (
    get_user_sessions,
    get_session_messages,
    save_ai_message,
    save_user_message, delete_session_by_id, clear_all_user_sessions
)
import uuid
from agent.react_agent import ReactAgent

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/session/create")
async def create_chat_session(
        req: SessionCreate,
        user: UserInfoResponse = Depends(get_current_user),
):
    session_id = str(uuid.uuid4())
    return {
        "code": 200,
        "data": {
            "id": session_id,
            "title": req.title
        }
    }


@router.get("/session/list")
async def list_user_sessions(
        user: UserInfoResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    sessions = await get_user_sessions(db, user.id)
    return {
        "code": 200,
        "data": sessions
    }


@router.get("/message/list")
async def list_messages(
        sessionId: str = Query(...),
        user: UserInfoResponse = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    messages = await get_session_messages(db, user.id, sessionId)
    return {
        "code": 200,
        "data": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content
            } for msg in messages
        ]
    }


@router.delete("/session/delete")
async def delete_session(
    sessionId: str = Query(...),
    user: UserInfoResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await delete_session_by_id(db, user.id, sessionId)
    return {"code": 200, "message": "删除成功"}


@router.delete("/session/clear-all")
async def clear_all_sessions(
    user: UserInfoResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await clear_all_user_sessions(db, user.id)
    return {"code": 200, "message": "已清空所有对话"}


@router.get("/stream")
async def chat_stream(
    sessionId: str = Query(...),
    content: str = Query(...),
    user: UserInfoResponse = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    history_msgs = await get_session_messages(db, user.id, sessionId)
    await save_user_message(db, user.id, sessionId, content)

    history_context = []
    for msg in history_msgs:
        role = "user" if msg.role == "user" else "assistant"
        history_context.append({"role": role, "content": msg.content})

    agent = ReactAgent()

    async def event_generator():
        full_answer = ""
        loop = asyncio.get_event_loop()
        sync_gen = agent.stream_chat(content, history_context, user.id, sessionId)

        while True:
            chunk_data = await loop.run_in_executor(None, lambda: next(sync_gen, None))
            if chunk_data is None:
                break

            yield chunk_data

            try:
                if chunk_data.startswith("data:"):
                    json_str = chunk_data.replace("data: ", "").strip()
                    data = json.loads(json_str)
                    if data.get("type") == "response" and data.get("content"):
                        full_answer += data.get("content")
            except:
                pass

        if full_answer.strip():
            await save_ai_message(db, user.id, sessionId, full_answer.strip())

    return StreamingResponse(event_generator(), media_type="text/event-stream; charset=utf-8")