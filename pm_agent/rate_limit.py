# PM Agent: API Rate Limiting (FastAPI-Limiter integration)
import os
from fastapi import Request, HTTPException
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as aioredis

REDIS_URL = os.getenv("PM_AGENT_REDIS_URL", "redis://localhost:6379/0")

async def init_rate_limiter(app):
    redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
    app.state.rate_limiter = FastAPILimiter

# Usage in FastAPI endpoint:
# from fastapi import Depends
# @router.get("/endpoint", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
# async def endpoint(...): ...
