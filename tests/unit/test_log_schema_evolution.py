"""
Hypothesis-based test for log schema evolution and backward compatibility.
"""
from hypothesis import given, strategies as st
from hypothesis.strategies import builds
import json
from jsonschema import validate
import os, json
with open(os.path.join(os.path.dirname(__file__), '../../log_schema_v1.json')) as f:
    schema_v1 = json.load(f)

class LogSchemaV1:
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
        self.extra = extra or {}

    def asdict(self):
        return self.__dict__

class LogSchemaV2(LogSchemaV1):
    def __init__(self, timestamp, correlation_id, severity, agent_id=None, event_type=None, message=None, extra=None, trace_id=None, deprecated_field=None, new_field=None):
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
        self.extra = extra or {}
        self.trace_id = trace_id
        self.extra['deprecated_field'] = deprecated_field
        self.extra['new_field'] = new_field

    def asdict(self):
        v2_dict = self.__dict__.copy()
        return v2_dict

    def downgrade(self):
        # Remove v2-only fields for v1 compatibility
        v1_dict = self.asdict()
        v1_dict['extra'].pop('deprecated_field', None)
        v1_dict['extra'].pop('new_field', None)
        return v1_dict

@given(builds(
    LogSchemaV1,
    timestamp=st.datetimes().map(lambda d: d.isoformat()),  # always non-None
    correlation_id=st.uuids().map(str),  # always non-None
    severity=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR"]),  # always non-None
    agent_id=st.text(min_size=1),
    event_type=st.sampled_from(["TASK_START", "BACKUP_INIT"]),
    message=st.text(),
    extra=st.none() | st.dictionaries(st.text(), st.text())
))
def test_backward_compatibility(log_entry):
    validate(instance=log_entry.asdict(), schema=schema_v1)

@given(builds(
    LogSchemaV2,
    timestamp=st.datetimes().map(lambda d: d.isoformat()),
    correlation_id=st.uuids().map(str),
    severity=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR"]),
    agent_id=st.text(min_size=1),
    event_type=st.sampled_from(["TASK_START", "BACKUP_INIT"]),
    message=st.text(),
    extra=st.dictionaries(st.text(), st.text()),
    deprecated_field=st.none() | st.text(),
    new_field=st.none() | st.text()
))
def test_backward_compatibility(entry):
    validate(instance=entry.downgrade(), schema=schema_v1)
