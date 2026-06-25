from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

snapshot_jobs_started = Counter(
    "cloudhopper_sync_snapshot_jobs_started_total",
    "Total number of snapshot sync jobs started",
)
snapshot_jobs_completed = Counter(
    "cloudhopper_sync_snapshot_jobs_completed_total",
    "Total number of snapshot sync jobs completed",
)
cdc_events_processed = Counter(
    "cloudhopper_sync_cdc_events_processed_total",
    "Total number of CDC events processed",
)
sync_lag_seconds = Gauge(
    "cloudhopper_sync_lag_seconds",
    "Current replication lag in seconds",
)
validation_success_ratio = Gauge(
    "cloudhopper_sync_validation_success_ratio",
    "Ratio of successful validations to total validations",
)
workflow_duration_seconds = Histogram(
    "cloudhopper_sync_workflow_duration_seconds",
    "Duration of sync workflows",
    buckets=[1, 5, 15, 30, 60, 120, 300, 600],
)
