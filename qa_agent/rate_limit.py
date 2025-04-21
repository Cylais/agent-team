from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as aioredis

async def setup_rate_limiter(app):
    redis = aioredis.from_url("redis://localhost:6379/0", encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)
    app.dependency_overrides[RateLimiter] = lambda: RateLimiter(times=10, seconds=60)  # Default: 10 req/min
