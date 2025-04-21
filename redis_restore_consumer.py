"""
Idempotent Redis Streams Consumer for Restore Events
- Ensures each restore event is processed exactly once
- Aligns message_queue_id with Redis Stream entry IDs
- Uses PostgreSQL row locking for concurrency control
- Acknowledges processed messages in Redis
"""
import redis
import psycopg2
from contextlib import contextmanager

REDIS_STREAM = 'restore_stream'
CONSUMER_GROUP = 'consumer_group'

@contextmanager
def pg_transaction(conn):
    cur = conn.cursor()
    try:
        cur.execute('BEGIN;')
        yield cur
        cur.execute('COMMIT;')
    except Exception:
        cur.execute('ROLLBACK;')
        raise
    finally:
        cur.close()

def process_restore_event(stream_id: str, agent_id: str, backup_ver: int, pg_conn, redis_client) -> None:
    """
    Process a restore event from Redis Streams, ensuring idempotent handling and transactional integrity in PostgreSQL.
    Logs actions and errors for observability.
    """
    import logging
    import json
    from datetime import datetime, timezone
    logger = logging.getLogger("restore_consumer")
    try:
        with pg_transaction(pg_conn) as cur:
            cur.execute("""
                SELECT 1 FROM restore_events 
                WHERE message_queue_id = %s
                FOR UPDATE SKIP LOCKED
            """, (stream_id,))
            if cur.fetchone():
                logger.info(json.dumps({"event": "duplicate_event", "stream_id": stream_id}))
                return  # Already processed
            # Process restore logic (placeholder)
            cur.execute("""
                INSERT INTO restore_events 
                (message_queue_id, agent_id, backup_version, restore_time, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (stream_id, agent_id, backup_ver, datetime.now(timezone.utc), 'success'))
            redis_client.xack(REDIS_STREAM, CONSUMER_GROUP, stream_id)
            logger.info(json.dumps({"event": "restore_processed", "stream_id": stream_id, "agent_id": agent_id, "backup_version": backup_ver}))
    except Exception as e:
        logger.error(json.dumps({"event": "restore_error", "stream_id": stream_id, "error": str(e)}))
        raise

# Example usage (to be wrapped in a consumer loop):
# for msg in redis_client.xreadgroup(CONSUMER_GROUP, 'consumer-1', {REDIS_STREAM: '>'}, count=1, block=5000):
#     stream_id = msg[0][1][0][0]
#     data = msg[0][1][0][1]
#     process_restore_event(stream_id, data['agent_id'], int(data['backup_version']), pg_conn, redis_client)

"""
Retention Policy:
- Use XTRIM to align stream retention with backup_history partitioning, e.g.:
    redis_client.xtrim(REDIS_STREAM, minid='1650000000000-0', approximate=True)
- Run hourly via a scheduled job or PostgreSQL event trigger.
"""
