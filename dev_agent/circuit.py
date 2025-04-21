import os
import logging
from aiobreaker import CircuitBreaker
from datetime import timedelta

logger = logging.getLogger("dev_agent.circuit")

# Helper to create a circuit breaker with env-configurable params
def create_redis_circuit_breaker():
    fail_max = int(os.getenv("DEV_AGENT_REDIS_CIRCUIT_FAIL_MAX", 5))
    timeout_sec = float(os.getenv("DEV_AGENT_REDIS_CIRCUIT_TIMEOUT", 60))
    breaker = CircuitBreaker(fail_max=fail_max, timeout_duration=timedelta(seconds=timeout_sec))

    # Attach logging for state changes
    def on_open_cb():
        logger.warning("Redis circuit breaker OPEN: Redis operations will be blocked.")
    def on_close_cb():
        logger.info("Redis circuit breaker CLOSED: Redis operations restored.")
    def on_half_open_cb():
        logger.info("Redis circuit breaker HALF-OPEN: Testing Redis connectivity.")
    breaker.add_open_handler(on_open_cb)
    breaker.add_close_handler(on_close_cb)
    breaker.add_half_open_handler(on_half_open_cb)
    return breaker

# Singleton circuit breaker for Redis operations
redis_circuit_breaker = create_redis_circuit_breaker()
