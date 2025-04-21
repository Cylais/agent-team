from prometheus_client import Gauge
from dev_agent.circuit import redis_circuit_breaker

# Gauge for Redis circuit breaker state: 0=closed, 1=half-open, 2=open
redis_circuit_state = Gauge(
    "dev_agent_redis_circuit_state",
    "State of the Redis circuit breaker (0=closed, 1=half-open, 2=open)"
)

def update_redis_circuit_metric():
    state = redis_circuit_breaker.current_state
    # Map state string to int
    mapping = {"closed": 0, "half-open": 1, "open": 2}
    redis_circuit_state.set(mapping.get(state, -1))
