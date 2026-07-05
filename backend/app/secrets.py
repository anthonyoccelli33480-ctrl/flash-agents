"""Stockage local de la clé Cerebras — .env gitignoré, jamais dans .venv."""

import os
import re
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT / ".env"


def _parse_env(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip("'\"")
    return out


def _render_env(data: dict[str, str], comments: list[str] | None = None) -> str:
    lines = [
        "# Flash Agents — secrets locaux (NE PAS committer)",
        "# Généré par l'onboarding — fichier dans .gitignore",
        "",
    ]
    if comments:
        lines.extend(comments)
        lines.append("")
    order = ["CEREBRAS_API_KEY", "FLASH_RATE_INTERVAL_SEC", "FLASH_PORT"]
    seen = set()
    for k in order:
        if k in data:
            lines.append(f"{k}={data[k]}")
            seen.add(k)
    for k, v in sorted(data.items()):
        if k not in seen:
            lines.append(f"{k}={v}")
    lines.append("")
    return "\n".join(lines)


def load_key() -> str:
    return os.getenv("CEREBRAS_API_KEY", "")


def save_key(api_key: str) -> Path:
    key = api_key.strip()
    if len(key) < 20:
        raise ValueError("Clé trop courte — vérifie ta clé Cerebras.")
    if not re.match(r"^csk-[\w-]+$", key):
        raise ValueError("Format invalide — une clé Cerebras commence par csk-")

    existing: dict[str, str] = {}
    if ENV_PATH.exists():
        existing = _parse_env(ENV_PATH.read_text(encoding="utf-8"))

    existing["CEREBRAS_API_KEY"] = key
    existing.setdefault("FLASH_RATE_INTERVAL_SEC", "15")

    ENV_PATH.write_text(_render_env(existing), encoding="utf-8")
    os.chmod(ENV_PATH, 0o600)
    os.environ["CEREBRAS_API_KEY"] = key
    return ENV_PATH


async def validate_key(api_key: str) -> bool:
    """Ping Cerebras pour vérifier que la clé fonctionne."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(
            "https://api.cerebras.ai/v1/models",
            headers={
                "Authorization": f"Bearer {api_key.strip()}",
                "User-Agent": "Mozilla/5.0 FlashAgents/1.0",
            },
        )
        if r.status_code == 401:
            raise ValueError("Clé refusée par Cerebras (401) — vérifie sur cloud.cerebras.ai")
        r.raise_for_status()
        return True