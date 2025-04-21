from hypothesis import given, strategies as st
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.event_handler import handle_event

@given(st.text(min_size=1), st.sampled_from(["INFO", "WARN", "ERROR"]))
def test_event_handler(event_data, severity):
    """Property-based test for event handler. Checks all severity levels and random event data."""
    result = handle_event({"data": event_data, "severity": severity})
    assert result in {"processed", "ignored", "error"}
