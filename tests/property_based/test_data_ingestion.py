from hypothesis import given, strategies as st
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import app

client = TestClient(app)

@given(st.dictionaries(st.text(min_size=1), st.integers()))
def test_data_ingestion(payload):
    """Property-based test for /ingest endpoint. Verifies status and payload acceptance."""
    response = client.post("/ingest", json=payload)
    assert response.status_code == 200
    # TODO: Add DB/Redis verification for full integration
