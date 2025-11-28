from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import logging
from typing import Optional

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Code Assistant")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-coder:6.7b"


class CodeRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 100
    temperature: Optional[float] = 0.7


class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = "You are a helpful coding assistant"


def check_ollama_health() -> bool:
    """Проверка доступности Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    ollama_healthy = check_ollama_health()
    return {
        "fastapi_status": "healthy",
        "ollama_status": "healthy" if ollama_healthy else "unavailable",
        "model": MODEL_NAME if ollama_healthy else "unknown",
    }


@app.post("/ai/generate")
async def generate_code(request: CodeRequest) -> dict:
    """Генерация кода с продвинутыми опциями"""
    if not check_ollama_health():
        raise HTTPException(status_code=503, detail="Ollama server is not available")

    payload = {
        "model": MODEL_NAME,
        "prompt": request.prompt,
        "stream": False,
        "options": {
            "num_predict": request.max_tokens,
            "temperature": request.temperature,
            "top_k": 40,
            "top_p": 0.9,
        },
    }

    try:
        logger.info(f"Generating code for prompt: {request.prompt[:100]}...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        logger.info(f"Generated {len(result.get('response', ''))} characters")

        return {
            "response": result.get("response", "").strip(),
            "model": result.get("model", ""),
            "stats": {
                "total_duration": result.get("total_duration", 0),
                "load_duration": result.get("load_duration", 0),
                "prompt_eval_count": result.get("prompt_eval_count", 0),
                "eval_count": result.get("eval_count", 0),
            },
        }

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Ollama request timeout")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")


@app.post("/ai/chat")
async def chat_with_ai(request: ChatRequest) -> dict:
    """Чат с AI"""
    full_prompt = f"{request.system_prompt}\n\nUser: {request.message}\nAssistant:"

    code_request = CodeRequest(prompt=full_prompt, max_tokens=150)
    return await generate_code(code_request)
