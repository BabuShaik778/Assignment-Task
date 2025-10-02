import aioredis
import os
import asyncio
from fastapi import Request, HTTPException, status
from .logging_config import logger

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "100"))  # default 100 requests
BURST = int(os.getenv("RATE_BURST", "200"))  # max bucket size
REFILL_SEC = int(os.getenv("RATE_REFILL_SEC", "60"))  # refill window in seconds

redis = None

async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    return redis

async def token_bucket(request: Request):
    """
    Keying: priority: Authorization token.sub -> IP
    """
    r = await get_redis()
    auth = request.headers.get("authorization", "")
    key = "rl:" + (auth.split()[-1] if auth else request.client.host)
    # Lua-like token bucket implemented via single Redis key storing "tokens:last_ts"
    async with r.client() as conn:
        now = int(asyncio.get_event_loop().time())
        data = await conn.get(key)
        if data:
            tokens, last = map(int, data.split(":"))
        else:
            tokens, last = BURST, now
        # refill
        delta = max(0, now - last)
        refill_amount = (delta * RATE_LIMIT) // REFILL_SEC
        tokens = min(BURST, tokens + refill_amount)
        last = now
        if tokens <= 0:
            # store updated state
            await conn.set(key, f"{tokens}:{last}", ex=REFILL_SEC*2)
            logger.info(f"rate-limit: blocked key={key}")
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
        tokens -= 1
        await conn.set(key, f"{tokens}:{last}", ex=REFILL_SEC*2)
