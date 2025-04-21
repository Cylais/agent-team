"""
Property-based test for log schema compliance
- Uses Hypothesis to generate log entries and validate against schema
"""
from hypothesis import given, strategies as st, builds
import json
from jsonschema import validate

with open("log_schema_v1.json") as f:
    schema = json.load(f)

class LogSchema:
    def __init__(self, timestamp, correlation_id, severity, agent_id=None, event_type=None, message=None, extra=None):
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
    timestamp=st.datetimes().map(lambda d: d.isoformat()),
    correlation_id=st.uuids().map(str),
    severity=st.sampled_from(["DEBUG", "INFO", "WARNING", "ERROR"]),
    agent_id=st.none() | st.text(min_size=1),
    event_type=st.none() | st.sampled_from(["TASK_START", "BACKUP_INIT"]),
    message=st.none() | st.text(),
    extra=st.none() | st.dictionaries(st.text(), st.text())
))
def test_log_schema_compliance(log_entry):
    validate(instance=log_entry.asdict(), schema=schema)
