"""
Pre-commit hook for Windsurf: Validate log event schema against registry before commit.
- Uses the log_schema_v1.json for validation
- Fails commit on schema violation
"""
import json
import sys
from jsonschema import validate, ValidationError

SCHEMA_PATH = "log_schema_v1.json"
LOG_FILE = sys.argv[1] if len(sys.argv) > 1 else "log_event.json"

with open(SCHEMA_PATH) as schema_file:
    schema = json.load(schema_file)
with open(LOG_FILE) as f:
    log_event = json.load(f)
try:
    validate(instance=log_event, schema=schema)
except ValidationError as e:
    print(f"Log schema validation failed: {e}")
    sys.exit(1)
