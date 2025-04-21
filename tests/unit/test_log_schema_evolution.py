"""
Hypothesis-based test for log schema evolution and backward compatibility.
"""
from hypothesis import given, strategies as st, builds
import json
from jsonschema import validate
from .. import log_schema_v1

schema_v1 = log_schema_v1.schema

class LogSchemaV1:
    def __init__(self, timestamp, correlation_id, severity, agent_id=None, event_type=None, message=None, extra=None):
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
    def __init__(self, *args, deprecated_field=None, new_field=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['deprecated_field'] = deprecated_field
        self.extra['new_field'] = new_field
    def downgrade(self):
        # Remove v2-only fields for v1 compatibility
        v1_dict = self.asdict()
        v1_dict['extra'].pop('deprecated_field', None)
        v1_dict['extra'].pop('new_field', None)
        return v1_dict

@given(builds(
    LogSchemaV2,
    timestamp=st.datetimes().map(lambda d: d.isoformat()),
    correlation_id=st.uuids().map(str),
    severity=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR"]),
    agent_id=st.none() | st.text(min_size=1),
    event_type=st.none() | st.sampled_from(["TASK_START", "BACKUP_INIT"]),
    message=st.none() | st.text(),
    extra=st.none() | st.dictionaries(st.text(), st.text()),
    deprecated_field=st.none() | st.text(),
    new_field=st.none() | st.text()
))
def test_backward_compatibility(entry):
    validate(instance=entry.downgrade(), schema=schema_v1)
