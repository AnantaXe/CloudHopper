-- PostgreSQL schema for CloudHopper sync subsystem

CREATE SCHEMA IF NOT EXISTS sync_subsystem;

CREATE TABLE IF NOT EXISTS sync_subsystem.sync_jobs (
    job_id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    source_adapter TEXT NOT NULL,
    target_adapter TEXT NOT NULL,
    strategy TEXT NOT NULL,
    phase TEXT NOT NULL,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    metadata JSONB DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sync_subsystem.sync_checkpoints (
    checkpoint_id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES sync_subsystem.sync_jobs(job_id) ON DELETE CASCADE,
    object_path TEXT NOT NULL,
    completed_chunks INT NOT NULL DEFAULT 0,
    total_chunks INT NOT NULL DEFAULT 0,
    last_processed_key TEXT,
    last_updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (job_id, object_path)
);

CREATE TABLE IF NOT EXISTS sync_subsystem.sync_offsets (
    offset_id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES sync_subsystem.sync_jobs(job_id) ON DELETE CASCADE,
    source_name TEXT NOT NULL,
    topic TEXT NOT NULL,
    partition INT NOT NULL,
    offset BIGINT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (job_id, source_name, topic, partition)
);

CREATE TABLE IF NOT EXISTS sync_subsystem.sync_audit_logs (
    audit_id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES sync_subsystem.sync_jobs(job_id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    event_payload JSONB NOT NULL,
    metadata JSONB DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sync_subsystem.sync_reconciliation_reports (
    report_id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES sync_subsystem.sync_jobs(job_id) ON DELETE CASCADE,
    report_type TEXT NOT NULL,
    report_payload JSONB NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sync_subsystem.sync_validation_results (
    result_id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES sync_subsystem.sync_jobs(job_id) ON DELETE CASCADE,
    row_count_match BOOLEAN,
    checksum_match BOOLEAN,
    drift_score NUMERIC(7,4) DEFAULT 0,
    sample_mismatch_count INT DEFAULT 0,
    details JSONB NOT NULL DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sync_subsystem.sync_agent_decisions (
    decision_id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES sync_subsystem.sync_jobs(job_id) ON DELETE CASCADE,
    agent_name TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    decision_payload JSONB NOT NULL,
    confidence_score NUMERIC(5,4) DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sync_checkpoints_job_id ON sync_subsystem.sync_checkpoints(job_id);
CREATE INDEX IF NOT EXISTS idx_sync_offsets_job_id ON sync_subsystem.sync_offsets(job_id);
CREATE INDEX IF NOT EXISTS idx_sync_audit_logs_job_id ON sync_subsystem.sync_audit_logs(job_id);
CREATE INDEX IF NOT EXISTS idx_sync_reconciliation_reports_job_id ON sync_subsystem.sync_reconciliation_reports(job_id);
CREATE INDEX IF NOT EXISTS idx_sync_agent_decisions_job_id ON sync_subsystem.sync_agent_decisions(job_id);
