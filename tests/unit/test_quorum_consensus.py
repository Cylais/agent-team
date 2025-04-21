"""
Model-based property test for quorum consensus (Python and Postgres).
"""
from hypothesis import given, strategies as st
from hypothesis.strategies import composite
import psycopg2

@composite
def quorum_inputs(draw):
    n = draw(st.integers(3, 7))
    threshold = draw(st.floats(0.5, 0.9))
    return ([draw(st.booleans()) for _ in range(n)], threshold)

def quorum_python(votes, threshold):
    return sum(votes)/len(votes) >= threshold if votes else False

def quorum_postgres(votes, threshold):
    conn = psycopg2.connect("dbname=testdb user=postgres password=Winterbottom93! host=localhost")
    with conn.cursor() as cur:
        cur.execute("SELECT validate_quorum(%s, %s)", (votes, threshold))
        return cur.fetchone()[0]

@given(quorum_inputs())
def test_quorum_consensus(inputs):
    votes, threshold = inputs
    assert quorum_python(votes, threshold) == quorum_postgres(votes, threshold)
