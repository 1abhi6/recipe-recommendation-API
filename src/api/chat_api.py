import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.config import redis_client
from src.orchestrator import Orchestrator

router = APIRouter()


class UserInputModel(BaseModel):
    message: str


def session_key(session_id: str):
    return f"session:{session_id}:history"


def session_meta_key(session_id: str):
    return f"session:{session_id}:meta"


def session_exists(session_id: str) -> bool:
    return redis_client.exists(session_meta_key(session_id)) > 0


@router.post("/chat/new")
def create_session():
    session_id = str(uuid.uuid4())
    redis_client.hset(
        session_meta_key(session_id),
        mapping={"created_at": str(uuid.uuid1().time), "messages": 0},
    )
    redis_client.delete(session_key(session_id))
    return {"session_id": session_id}


@router.get("/chat/{session_id}")
async def chat_with_session(session_id: str, user_input: str):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    # Orchestrate chat and store history
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

    # Save history
    message = {"role": "user", "content": user_input}
    response_msg = {"role": "assistant", "content": response}
    redis_client.rpush(session_key(session_id), str(message))
    redis_client.rpush(session_key(session_id), str(response_msg))
    redis_client.hincrby(session_meta_key(session_id), "messages", 2)
    return {"response": response}


@router.get("/chat/{session_id}/history")
def get_history(session_id: str):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    history = redis_client.lrange(session_key(session_id), 0, -1)
    return {"session_id": session_id, "history": history}


@router.post("/chat/{session_id}/clear")
def clear_history(session_id: str):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    redis_client.delete(session_key(session_id))
    redis_client.hset(session_meta_key(session_id), "messages", 0)
    return {"session_id": session_id, "cleared": True}


@router.delete("/chat/{session_id}")
def delete_session(session_id: str):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    redis_client.delete(session_key(session_id))
    redis_client.delete(session_meta_key(session_id))
    return {"session_id": session_id, "deleted": True}


@router.get("/sessions")
def list_sessions():
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
    return {"sessions": sessions}


@router.get("/health")
def health():
    try:
        pong = redis_client.ping()
        return {"status": "ok", "redis": pong}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
