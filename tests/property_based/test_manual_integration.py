import os

def test_manual_integration():
    assert os.path.exists('scripts/merge_schema')
    with open('.gitattributes') as f:
        assert 'log_schema_v*.json merge=log_schema' in f.read()
