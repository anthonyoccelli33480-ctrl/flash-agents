"""Rate gate — respecte les limites Cerebras free tier (≈5 req/min)."""

import asyncio
import os
import time

_interval = float(os.getenv("FLASH_RATE_INTERVAL_SEC", "15"))
_last_call = 0.0
_lock = asyncio.Lock()


async def acquire() -> float:
    """Attend si nécessaire, retourne le temps d'attente en secondes."""
    global _last_call
    async with _lock:
        now = time.monotonic()
        elapsed = now - _last_call
        wait = max(0.0, _interval - elapsed)
        if wait > 0:
            await asyncio.sleep(wait)
        _last_call = time.monotonic()
        return wait


def next_available_in() -> float:
    """Secondes avant la prochaine requête autorisée."""
    elapsed = time.monotonic() - _last_call
    return max(0.0, _interval - elapsed)