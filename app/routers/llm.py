from fastapi import APIRouter, Body
from pydantic import BaseModel
from app.services.llm_client import LLMClient

router = APIRouter(prefix="/llm", tags=["LLM"])

# Создаём клиент при инициализации роутера
client = LLMClient()


class ChatRequest(BaseModel):
    prompt: str


class ChatWithSystemRequest(BaseModel):
    system_prompt: str
    user_prompt: str


class ChatJsonRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    json_standard: str


@router.post("/chat")
async def chat(request: ChatRequest = Body(...)) -> str:
    """Простой запрос к LLM."""
    return client.chat(prompt=request.prompt)


@router.post("/chat-with-system")
async def chat_with_system(request: ChatWithSystemRequest = Body(...)) -> str:
    """Запрос к LLM с системным промптом."""
    return client.chat_with_system(system_prompt=request.system_prompt, user_prompt=request.user_prompt)


@router.post("/chat-json")
async def chat_json(request: ChatJsonRequest = Body(...)) -> dict:
    """
    Запрос к LLM со структурированным JSON-ответом.
    
    json_standard — описание формата JSON, который должен вернуть LLM.
    """
    full_system_prompt = f"{request.system_prompt}\nФормат ответа: {request.json_standard}"
    result = client.chat_json(system_prompt=full_system_prompt, user_prompt=request.user_prompt)
    return result
