import pytest
from pact import Consumer, Provider
import requests

PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 1234
PACT_URL = f'http://{PACT_MOCK_HOST}:{PACT_MOCK_PORT}'

@pytest.fixture(scope='module')
def pact():
    pact = Consumer('dev-agent-consumer').has_pact_with(
        Provider('dev-agent-provider'),
        host_name=PACT_MOCK_HOST,
        port=PACT_MOCK_PORT,
    )
    pact.start_service()
    yield pact
    pact.stop_service()


def test_create_task_contract(pact):
    expected = {
        'id': 'devtask_123',
        'description': 'Implement login feature',
        'assigned_to': 'developer1',
        'status': 'pending',
        'priority': 2
    }
    (
        pact
        .given('Task creation endpoint is available')
        .upon_receiving('a request to create a task')
        .with_request(
            method='POST',
            path='/dev/create_task',
            headers={'Content-Type': 'application/json'},
            body={
                'description': 'Implement login feature',
                'assigned_to': 'developer1',
                'context': {},
                'dependencies': [],
                'priority': 2
            }
        )
        .will_respond_with(200, body={'task_id': 'devtask_123'})
    )
    with pact:
        response = requests.post(
            f'{PACT_URL}/dev/create_task',
            json={
                'description': 'Implement login feature',
                'assigned_to': 'developer1',
                'context': {},
                'dependencies': [],
                'priority': 2
            }
        )
        assert response.status_code == 200
        assert 'task_id' in response.json()


def test_get_task_status_contract(pact):
    (
        pact
        .given('A task exists with ID devtask_123')
        .upon_receiving('a request for task status')
        .with_request(
            method='GET',
            path='/dev/status/devtask_123',
        )
        .will_respond_with(200, body={'task': {
            'id': 'devtask_123',
            'description': 'Implement login feature',
            'assigned_to': 'developer1',
            'status': 'pending',
            'priority': 2
        }})
    )
    with pact:
        response = requests.get(f'{PACT_URL}/dev/status/devtask_123')
        assert response.status_code == 200
        assert response.json()['task']['id'] == 'devtask_123'
