"""
Property-based test for log schema compliance
- Uses Hypothesis to generate log entries and validate against schema
"""
from hypothesis import given, strategies as st
from hypothesis.strategies import builds
import json
from jsonschema import validate
import os, json
with open(os.path.join(os.path.dirname(__file__), '../../log_schema_v1.json')) as f:
    schema = json.load(f)

class LogSchema:
    def __init__(self, timestamp, correlation_id, severity, agent_id=None, event_type=None, message=None, extra=None):
        if timestamp is None:
            raise ValueError("timestamp is required and cannot be None")
        if correlation_id is None:
            raise ValueError("correlation_id is required and cannot be None")
        if severity is None:
            raise ValueError("severity is required and cannot be None")
        self.timestamp = timestamp
        self.correlation_id = correlation_id
        self.severity = severity
        self.agent_id = agent_id
        self.event_type = event_type
        self.message = message
        self.extra = extra

    def asdict(self):
        return self.__dict__

@given(builds(
    LogSchema,
    timestamp=st.datetimes().map(lambda d: d.isoformat()),  # always non-None
    correlation_id=st.uuids().map(str),  # always non-None
    severity=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR"]),  # always non-None
    agent_id=st.text(min_size=1),
    event_type=st.sampled_from(["TASK_START", "BACKUP_INIT"]),
    message=st.text(),
    extra=st.dictionaries(st.text(), st.text())
))
def test_log_schema_compliance(log_entry):
    validate(instance=log_entry.asdict(), schema=schema)
