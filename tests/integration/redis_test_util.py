import os
import redis.asyncio as redis

# Utility to get a Redis connection for testing (local or in-memory)
def get_test_redis_url():
    # Prefer REDIS_URL from env, fallback to localhost
    return os.getenv("TEST_REDIS_URL", "redis://localhost:6379/0")

def get_redis():
    url = get_test_redis_url()
    return redis.from_url(url, decode_responses=True)
