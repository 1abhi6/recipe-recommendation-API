import os
import uuid

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from src.config import redis_client
from src.orchestrator import Orchestrator

load_dotenv()

API_KEY = os.getenv("API_KEY", None)
security = HTTPBearer()
router = APIRouter()


class UserInputModel(BaseModel):
    message: str


def session_key(session_id: str):
    return f"session:{session_id}:history"


def session_meta_key(session_id: str):
    return f"session:{session_id}:meta"


def session_exists(session_id: str) -> bool:
    return redis_client.exists(session_meta_key(session_id)) > 0


def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return True


@router.get("/")
def api_overview():
    try:
        redis_status = redis_client.ping()
    except Exception as e:
        redis_status = f"error: {str(e)}"
    overview = {
        "api": "Recipe Recommendation API",
        "routes": [
            "/chat/new",
            "/chat/{session_id}",
            "/chat/{session_id}/history",
            "/chat/{session_id}/clear",
            "/chat/{session_id} [DELETE]",
            "/sessions",
            "/health",
            "/",
        ],
        "redis_status": redis_status,
    }
    return JSONResponse(content=overview, status_code=200)


@router.post("/chat/new")
def create_session(authorized: bool = Depends(verify_api_key)):
    session_id = str(uuid.uuid4())
    redis_client.hset(
        session_meta_key(session_id),
        mapping={"created_at": str(uuid.uuid1().time), "messages": 0},
    )
    redis_client.delete(session_key(session_id))
    return JSONResponse(content={"session_id": session_id}, status_code=201)


@router.get("/chat/{session_id}")
async def chat_with_session(
    session_id: str, user_input: str, authorized: bool = Depends(verify_api_key)
):
    if not session_exists(session_id):
        return JSONResponse(content={"detail": "Session not found"}, status_code=404)
    orchestrator = Orchestrator(user_input=user_input)
    input_guardrail = await orchestrator.input_guardrail()
    if not input_guardrail.status:
        response = input_guardrail.message
    else:
        generated_recipe = await orchestrator.generate_recipe()
        output_guardrail = await orchestrator.output_guardrail(
            generated_recipe=generated_recipe
        )
        if output_guardrail.status:
            response = generated_recipe
        else:
            response = output_guardrail.message

    message = {"role": "user", "content": user_input}
    response_msg = {"role": "assistant", "content": response}
    redis_client.rpush(session_key(session_id), str(message))
    redis_client.rpush(session_key(session_id), str(response_msg))
    redis_client.hincrby(session_meta_key(session_id), "messages", 2)
    return JSONResponse(content={"response": response}, status_code=200)


@router.get("/chat/{session_id}/history")
def get_history(session_id: str, authorized: bool = Depends(verify_api_key)):
    if not session_exists(session_id):
        return JSONResponse(content={"detail": "Session not found"}, status_code=404)
    history = redis_client.lrange(session_key(session_id), 0, -1)
    return JSONResponse(
        content={"session_id": session_id, "history": history}, status_code=200
    )


@router.post("/chat/{session_id}/clear")
def clear_history(session_id: str, authorized: bool = Depends(verify_api_key)):
    if not session_exists(session_id):
        return JSONResponse(content={"detail": "Session not found"}, status_code=404)
    redis_client.delete(session_key(session_id))
    redis_client.hset(session_meta_key(session_id), "messages", 0)
    return JSONResponse(
        content={"session_id": session_id, "cleared": True}, status_code=200
    )


@router.delete("/chat/{session_id}")
def delete_session(session_id: str, authorized: bool = Depends(verify_api_key)):
    if not session_exists(session_id):
        return JSONResponse(content={"detail": "Session not found"}, status_code=404)
    redis_client.delete(session_key(session_id))
    redis_client.delete(session_meta_key(session_id))
    return JSONResponse(
        content={"session_id": session_id, "deleted": True}, status_code=200
    )


@router.get("/sessions")
def list_sessions(authorized: bool = Depends(verify_api_key)):
    keys = redis_client.keys("session:*:meta")
    sessions = []
    for key in keys:
        session_id = key.split(":")[1]
        meta = redis_client.hgetall(key)
        sessions.append(
            {
                "session_id": session_id,
                "created_at": meta.get("created_at"),
                "messages": meta.get("messages"),
            }
        )
    return JSONResponse(content={"sessions": sessions}, status_code=200)


@router.get("/health")
def health():
    try:
        pong = redis_client.ping()
        return JSONResponse(content={"status": "ok", "redis": pong}, status_code=200)
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "detail": str(e)}, status_code=500
        )
