"""
Model-based property test for quorum consensus
- Validates Python-side and Postgres-side logic
"""
from hypothesis import given, strategies as st
import psycopg2

# Python-side validation function
validate_quorum_py = lambda votes, threshold: (sum(votes)/len(votes) >= threshold) if votes else False

@given(st.lists(st.booleans(), min_size=3))
def test_quorum_consensus(votes):
    threshold = 0.6
    # Python logic
    result_py = validate_quorum_py(votes, threshold)
    # Postgres logic
    conn = psycopg2.connect("dbname=testdb user=postgres password=postgres host=localhost")
    with conn.cursor() as cur:
        cur.execute("SELECT validate_quorum(%s, %s)", (votes, threshold))
        result_pg = cur.fetchone()[0]
    assert result_py == result_pg
