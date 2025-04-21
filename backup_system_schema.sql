-- Backup System Schema for Autonomous Agent Platform
-- Optimized for right-sized, versioned, and reliable backups

-- Table: agent_backups
-- Tracks each agent's latest backup and associated metadata
CREATE TABLE IF NOT EXISTS agent_backups (
    agent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(), -- Unique agent identifier (UUID for storage efficiency)
    last_backup TIMESTAMP NOT NULL, -- Last backup time
    storage_path TEXT NOT NULL, -- S3/B2 path to backup
    checksum TEXT NOT NULL, -- Blake3 hash for integrity
    restored BOOLEAN DEFAULT FALSE, -- Restore status
    backup_version INTEGER NOT NULL, -- For versioned backups
    backup_size INTEGER, -- Size in bytes
    error_msg TEXT, -- Last error if any
    priority SMALLINT NOT NULL DEFAULT 2 CHECK (priority BETWEEN 1 AND 5), -- Backup priority tier
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_agent_backups_last_backup ON agent_backups(last_backup);
CREATE INDEX IF NOT EXISTS idx_agent_backups_version ON agent_backups(backup_version);

-- Table: backup_history
-- Stores all historical backups for auditing and rollback
CREATE TABLE IF NOT EXISTS backup_history (
    backup_id SERIAL PRIMARY KEY,
    agent_id UUID NOT NULL,
    backup_time TIMESTAMP NOT NULL,
    storage_path TEXT NOT NULL,
    checksum TEXT NOT NULL,
    backup_version INTEGER NOT NULL,
    backup_size INTEGER,
    restored BOOLEAN DEFAULT FALSE,
    error_msg TEXT,
    correlation_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_id) REFERENCES agent_backups(agent_id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_backup_history_correlation_id ON backup_history(correlation_id);

-- Partitioned version for scalable time-series history
CREATE TABLE IF NOT EXISTS backup_history_partitioned (
    LIKE backup_history INCLUDING ALL
) PARTITION BY RANGE (backup_time);

-- Example: Create a monthly partition
-- CREATE TABLE backup_history_2025_04 PARTITION OF backup_history_partitioned
--     FOR VALUES FROM ('2025-04-01') TO ('2025-05-01');

-- BRIN index for space-efficient time queries
CREATE INDEX IF NOT EXISTS idx_backup_history_brin ON backup_history_partitioned 
USING BRIN (backup_time, agent_id) WITH (pages_per_range=128);

CREATE INDEX IF NOT EXISTS idx_backup_history_agent_time ON backup_history(agent_id, backup_time);
CREATE INDEX IF NOT EXISTS idx_backup_history_version ON backup_history(backup_version);

-- Table: backup_integrity_checks
-- Tracks results of periodic backup integrity checks
CREATE TABLE IF NOT EXISTS backup_integrity_checks (
    check_id SERIAL PRIMARY KEY,
    agent_id UUID NOT NULL,
    backup_version INTEGER NOT NULL,
    check_time TIMESTAMP NOT NULL,
    passed BOOLEAN NOT NULL,
    details TEXT,
    FOREIGN KEY (agent_id) REFERENCES agent_backups(agent_id)
);

CREATE INDEX IF NOT EXISTS idx_integrity_checks_agent_version ON backup_integrity_checks(agent_id, backup_version);

-- Table: restore_events
-- Audits restores for compliance and troubleshooting
CREATE TABLE IF NOT EXISTS restore_events (
    restore_id SERIAL PRIMARY KEY,
    agent_id UUID NOT NULL,
    backup_version INTEGER NOT NULL,
    restore_time TIMESTAMP NOT NULL,
    status TEXT NOT NULL, -- e.g., 'success', 'failure'
    error_msg TEXT,
    message_queue_id TEXT, -- For Redis Streams/message queue integration
    correlation_id TEXT,
    FOREIGN KEY (agent_id) REFERENCES agent_backups(agent_id)
);
CREATE INDEX IF NOT EXISTS idx_restore_events_correlation_id ON restore_events(correlation_id);

-- Partial index for recent restore failures (performance boost)
CREATE INDEX IF NOT EXISTS idx_restore_events_recent_failures ON restore_events(agent_id)
WHERE status = 'failure' AND restore_time > NOW() - INTERVAL '7 days';
CREATE INDEX IF NOT EXISTS idx_restore_events_queue ON restore_events(message_queue_id);

CREATE INDEX IF NOT EXISTS idx_restore_events_agent_version ON restore_events(agent_id, backup_version);

-- All tables are designed for right-sized Postgres deployments. Consider partitioning backup_history for large-scale rollouts.
-- Use periodic VACUUM/ANALYZE for performance.
