from fastapi_limiter import FastAPILimiter
from fastapi import FastAPI
import redis.asyncio as redis
import os

REDIS_URL = os.getenv("TA_AGENT_REDIS_URL", "redis://localhost:6379/0")

async def setup_rate_limiter(app: FastAPI):
    redis_conn = await redis.from_url(REDIS_URL, encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis_conn)
    app.state.rate_limiter = FastAPILimiter
