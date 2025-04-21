"""
Circuit Breaker for Redis/Service Calls
- Uses tenacity for retry
- Uses circuitbreaker for open/close logic
- Exposes Prometheus metrics
"""
from circuitbreaker import circuit
from tenacity import Retrying, stop_after_attempt, wait_exponential
import prometheus_client
from prometheus_client import Gauge

circuit_state = Gauge('windsrf_circuit_state', 'Circuit state for services', ['service'])

@circuit(failure_threshold=5, recovery_timeout=30)
def redis_operation(execute_redis_command):
    service = 'redis'
    try:
        with Retrying(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1)
        ) as retry:
            retry(execute_redis_command)
        circuit_state.labels(service=service).set(0)  # 0 = closed
    except Exception:
        circuit_state.labels(service=service).set(1)  # 1 = open
        raise
