from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
import os

REDIS_URL = os.getenv("DEV_AGENT_RATE_LIMIT_REDIS_URL", "redis://localhost:6379/1")

async def init_rate_limiter(app):
    redis_conn = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_conn)

# Default rate limiter dependency: 10 requests per minute per user (adjust as needed)
def default_rate_limiter():
    return RateLimiter(times=10, seconds=60)
