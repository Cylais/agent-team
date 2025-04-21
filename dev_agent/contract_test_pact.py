# Dev Agent API Contract Test (Pact-style stub)
# NOTE: This is a placeholder for actual Pact integration. Replace with real Pact test as needed.

import pytest
from pact import Consumer, Provider
import requests
import os

PACT_MOCK_HOST = os.getenv("PACT_MOCK_HOST", "localhost")
PACT_MOCK_PORT = int(os.getenv("PACT_MOCK_PORT", 1234))

@pytest.fixture(scope="module")
def pact():
    pact = Consumer('DevAgentConsumer').has_pact_with(
        Provider('DevAgentProvider'),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT
    )
    pact.start_service()
    yield pact
    pact.stop_service()

# Example contract for /dev/status/{task_id}
def test_get_task_status_contract(pact):
    expected = {
        'task': {
            'id': 'devtask_123',
            'description': 'Implement login feature',
            'assigned_to': 'developer1',
            'status': 'pending',
            'priority': 2
        }
    }
    (pact
     .given('Task exists')
     .upon_receiving('a request for a task status')
     .with_request('get', '/dev/status/devtask_123')
     .will_respond_with(200, body=expected))

    with pact:
        result = requests.get(f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}/dev/status/devtask_123')
        assert result.json() == expected
