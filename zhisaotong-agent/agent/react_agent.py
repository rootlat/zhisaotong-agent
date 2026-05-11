import asyncio
import json
import time
from langchain_core.messages import AIMessage
from models.factory import chat_model
from rag.rag_service import rag_service
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import (
    rag_summarize, get_weather, get_user_location, get_user_id,
    get_current_month, fetch_external_data, fill_context_for_report
)
from agent.middleware.middleware import monitor_tool, log_before_model, report_prompt_switch
from langchain.agents import create_agent


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[
                rag_summarize, get_weather, get_user_location, get_user_id,
                get_current_month, fetch_external_data, fill_context_for_report
            ],
            middleware=[monitor_tool, log_before_model, report_prompt_switch]
        )

    def stream_chat(self, query: str, history: list = None, user_id: int = None, session_id: str = None):
        try:
            use_user_id = user_id if user_id is not None else 0
            messages = []
            if history:
                messages.extend(history)
            messages.append({"role": "user", "content": query})

            # 1. 前置 RAG
            try:
                rag_result = asyncio.run(rag_service.rag_summarize(query, use_user_id))
                if rag_result and "抱歉" not in rag_result and "失败" not in rag_result and "参考资料中未提及" not in rag_result:
                    for char in rag_result:
                        print(f"data: {json.dumps({'type': 'response', 'content': char}, ensure_ascii=False)}\n\n")
                        yield f"data: {json.dumps({'type': 'response', 'content': char}, ensure_ascii=False)}\n\n"
                        time.sleep(0.015)
                    yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"
                    return
            except Exception as e:
                print(f"前置RAG失败：{e}")

            # 2. Agent 同步流式
            input_dict = {"messages": messages}
            last_content = ""
            skip_keywords = [
                "我需要先获取", "接下来将查询", "已获取到", "思考：", "工具调用：",
                "检索结果：", "thinking:", "tool_call:", "参考资料中未提及"
            ]

            for chunk in self.agent.stream(
                input_dict,
                stream_mode="messages",
                context={"report": False}
            ):
                msg = chunk[0] if isinstance(chunk, tuple) else chunk
                if not isinstance(msg, AIMessage):
                    continue
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    continue
                if not hasattr(msg, "content") or not msg.content:
                    continue

                content = msg.content.strip()
                if any(key in content for key in skip_keywords):
                    continue
                if content == last_content:
                    continue
                last_content = content

                # 逐字输出（流式核心）
                for char in content:
                    yield f"data: {json.dumps({'type': 'response', 'content': char}, ensure_ascii=False)}\n\n"
                    time.sleep(0.015)

            # 兜底
            if not last_content:
                tip = "抱歉，当前知识库暂无该问题相关内容。"
                for char in tip:
                    yield f"data: {json.dumps({'type': 'response', 'content': char}, ensure_ascii=False)}\n\n"
                    time.sleep(0.015)

            yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"

        except Exception as e:
            error_msg = f"处理失败：{str(e)}"
            yield f"data: {json.dumps({'type': 'error', 'content': error_msg}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done'}, ensure_ascii=False)}\n\n"