# main.py
import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage
from agent import agent

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Personal Agent is running!"}

@app.get("/api/ask")
async def ask(q: str):
    """Stream agent thinking steps + final answer via SSE."""

    def stream():
        try:
            for chunk in agent.stream(
                {"messages": [HumanMessage(content=q)]},
                stream_mode="updates"
            ):
                # Agent thinking — tool calls
                if "agent" in chunk:
                    messages = chunk["agent"].get("messages", [])
                    for msg in messages:
                        # Tool call (agent deciding what to do)
                        if hasattr(msg, "tool_calls") and msg.tool_calls:
                            for tc in msg.tool_calls:
                                data = json.dumps({
                                    "type": "thinking",
                                    "text": f"Using tool: {tc['name']}..."
                                })
                                yield f"data: {data}\n\n"
                        # Final text response
                        elif hasattr(msg, "content") and msg.content:
                            data = json.dumps({
                                "type": "answer",
                                "text": msg.content
                            })
                            yield f"data: {data}\n\n"

                # Tool result
                if "tools" in chunk:
                    messages = chunk["tools"].get("messages", [])
                    for msg in messages:
                        if hasattr(msg, "content") and msg.content:
                            data = json.dumps({
                                "type": "tool_result",
                                "text": str(msg.content)[:300]
                            })
                            yield f"data: {data}\n\n"

            # Done
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'text': str(e)})}\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )