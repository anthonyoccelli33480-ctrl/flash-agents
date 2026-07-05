"""Client Cerebras Inference (OpenAI-compatible)."""

import asyncio
import os
import time
from typing import Any

import httpx

BASE_URL = "https://api.cerebras.ai/v1"
UA = "Mozilla/5.0 FlashAgents/1.0"


def _user_content(text: str, images: list[str] | None) -> str | list[dict[str, Any]]:
    if not images:
        return text
    parts: list[dict[str, Any]] = [{"type": "text", "text": text or "Analyse cette image."}]
    for url in images[:5]:
        parts.append({"type": "image_url", "image_url": {"url": url}})
    return parts


async def chat(
    *,
    model: str,
    system: str,
    user: str,
    images: list[str] | None = None,
    max_tokens: int = 2048,
    temperature: float = 0.2,
    json_mode: bool = True,
    extra: dict[str, Any] | None = None,
) -> tuple[str, float, dict[str, str]]:
    """Appelle Cerebras, retourne (content, latency_s, rate_headers)."""
    key = os.getenv("CEREBRAS_API_KEY", "")
    if not key:
        raise ValueError("CEREBRAS_API_KEY manquante — copie .env.example → .env")

    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": _user_content(user.strip(), images)},
        ],
        "temperature": temperature,
        "max_completion_tokens": max_tokens,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    if extra:
        payload.update(extra)

    t0 = time.perf_counter()
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = None
        for attempt in range(3):
            resp = await client.post(
                f"{BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                    "User-Agent": UA,
                },
                json=payload,
            )
            if resp.status_code != 429:
                break
            await asyncio.sleep(5 * (attempt + 1))
        assert resp is not None
        resp.raise_for_status()
        data = resp.json()

    latency = time.perf_counter() - t0
    msg = data["choices"][0]["message"]
    content = msg.get("content") or msg.get("reasoning") or ""
    if not content.strip():
        raise ValueError("Réponse vide du modèle")

    rate_hdrs = {
        k: v
        for k, v in resp.headers.items()
        if "ratelimit" in k.lower() or k.lower() == "retry-after"
    }
    return content, latency, rate_hdrs