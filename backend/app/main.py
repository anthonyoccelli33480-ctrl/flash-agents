"""Flash Agents — API backend."""

import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.agents import get_agent, list_agents
from app.agents.guides import get_guide
from app.cerebras_client import chat
from app.rate_gate import acquire, next_available_in
from app.secrets import ENV_PATH, load_key, save_key, validate_key

# Charge .env depuis la racine du repo
_root = Path(__file__).resolve().parents[2]
load_dotenv(_root / ".env")
load_dotenv(_root.parent / "jarvis-os" / ".env")  # repli si clé déjà là

app = FastAPI(title="Flash Agents", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    agent_id: str
    input: str = Field(default="", max_length=80_000)
    images: list[str] = Field(default_factory=list, max_length=5)


class SetupKeyRequest(BaseModel):
    api_key: str = Field(..., min_length=20, max_length=256)


class RunResponse(BaseModel):
    agent_id: str
    agent_name: str
    model: str
    result: dict
    latency_ms: float
    queue_wait_ms: float
    rate_headers: dict[str, str]
    next_available_in_sec: float
    how_to: list[str] = []
    next_steps: list[str] = []


@app.get("/api/health")
async def health():
    has_key = bool(load_key())
    return {
        "ok": has_key,
        "cerebras_key": has_key,
        "env_file": str(ENV_PATH),
        "next_available_in_sec": round(next_available_in(), 1),
        "rate_interval_sec": float(os.getenv("FLASH_RATE_INTERVAL_SEC", "15")),
    }


@app.post("/api/setup/key")
async def setup_key(req: SetupKeyRequest):
    """Enregistre la clé dans .env (gitignoré), valide auprès de Cerebras."""
    try:
        await validate_key(req.api_key)
        path = save_key(req.api_key)
        return {
            "ok": True,
            "message": "Clé validée et enregistrée localement.",
            "path": str(path),
            "hint": "Fichier .env gitignoré — pas dans .venv",
        }
    except ValueError as e:
        raise HTTPException(400, str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(502, f"Cerebras inaccessible : {e.response.status_code}")
    except Exception as e:
        raise HTTPException(502, str(e))


@app.get("/api/agents")
async def agents():
    return {"agents": list_agents()}


@app.post("/api/run", response_model=RunResponse)
async def run(req: RunRequest):
    try:
        agent = get_agent(req.agent_id)
    except KeyError:
        raise HTTPException(404, f"Agent '{req.agent_id}' introuvable")

    if agent.requires_image and not req.images:
        raise HTTPException(400, "Cet agent Gemma requiert au moins une image (PNG/JPEG).")
    if not agent.requires_image and len(req.input.strip()) < 3:
        raise HTTPException(400, "Texte trop court (min 3 caractères).")
    if len(req.images) > agent.max_images:
        raise HTTPException(400, f"Maximum {agent.max_images} images.")

    for url in req.images:
        if not url.startswith("data:image/"):
            raise HTTPException(400, "Images : data URI base64 PNG/JPEG uniquement.")

    wait = await acquire()
    try:
        raw, latency, rate_hdrs = await chat(
            model=agent.model,
            system=agent.system,
            user=req.input.strip() or "Analyse l'image fournie.",
            images=req.images or None,
            max_tokens=agent.max_tokens,
            temperature=agent.temperature,
            json_mode=True,
            extra=agent.extra,
        )
    except httpx.HTTPStatusError as e:
        body = e.response.text[:500]
        if e.response.status_code == 429:
            raise HTTPException(
                429,
                "Cerebras saturé (queue) — réessaie dans 30s. Le rate-gate local est actif.",
            )
        raise HTTPException(e.response.status_code, body)
    except Exception as e:
        if "429" in str(e):
            raise HTTPException(429, "Rate limit Cerebras — réessaie dans quelques secondes")
        raise HTTPException(502, str(e))

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Modèles reasoning : extraire le dernier bloc JSON
        import re
        blocks = re.findall(r"\{[^{}]*\}", raw, re.DOTALL)
        if not blocks:
            raise HTTPException(502, f"JSON invalide : {raw[:300]}")
        result = json.loads(blocks[-1])

    guide = get_guide(agent.id)
    return RunResponse(
        agent_id=agent.id,
        agent_name=agent.name,
        model=agent.model,
        result=result,
        latency_ms=round(latency * 1000, 1),
        queue_wait_ms=round(wait * 1000, 1),
        rate_headers=rate_hdrs,
        next_available_in_sec=round(next_available_in(), 1),
        how_to=guide["how_to"],
        next_steps=guide["next_steps"],
    )
