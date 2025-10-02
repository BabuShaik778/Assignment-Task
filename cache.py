

import aioredis
import json
from functools import wraps

redis = None

async def get_redis():
    global redis
    if redis is None:
        redis = await aioredis.from_url("redis://localhost")
    return redis

def cache_response(ttl: int = 60, key_builder=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = await get_redis()
            key = key_builder(*args, **kwargs) if key_builder else f"cache:{func.__name__}"
            cached = await redis.get(key)
            if cached:
                return {"data": json.loads(cached), "cached": True}
            result = await func(*args, **kwargs)
            await redis.set(key, json.dumps(result), ex=ttl)
            return {"data": result, "cached": False}
        return wrapper
    return decorator
