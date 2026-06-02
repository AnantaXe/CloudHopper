# Agentic Autonomous Data Synchronization Subsystem

## Overview

This repository extension implements a production-ready, cloud-agnostic data synchronization subsystem for the CloudHopper platform. It is built as an independent module within the larger migration ecosystem and is focused on:

- Data Synchronization
- Snapshot Migration
- CDC Synchronization
- Continuous Replication
- Data Validation
- Conflict Resolution
- Cutover Readiness
- Synchronization Intelligence

The subsystem is designed to support future migrations across AWS, Azure, GCP, On-Prem, Hybrid, Database-to-Database, Storage-to-Storage, and Kubernetes-to-Kubernetes with no architectural change.

---

## Phase Plan

### Phase 1

1. Snapshot Engine
2. Temporal workflow layer with metadata orchestration
3. PostgreSQL metadata and checkpointing store
4. Sync Control Plane
5. Core domain and adapter contracts

### Phase 2

1. Debezium CDC pipeline
2. Kafka event backbone
3. CDC connector manager
4. Schema evolution and replay services
5. Event processor, ordering, and idempotency

---

## Architecture Diagram (ASCII)

```
                       +--------------------------+
                       |  Sync Control Plane      |
                       |--------------------------|
                       | Policy Engine            |
                       | Workflow Orchestrator    |
                       | Health / Metrics         |
                       +-----------+--------------+
                                   |
                       +-----------v--------------+
                       |  Temporal Workflow Layer  |
+--------------------->--------------------------+-----------------------------+
|                      | SnapshotWorkflow         |                             |
|                      | CDCWorkflow              |                             |
|                      | ValidationWorkflow       |                             |
|                      | ConflictResolutionWorkflow|                            |
|                      | CutoverWorkflow          |                             |
|                      | RecoveryWorkflow         |                             |
|                      +-----------+--------------+                             |
|                                  |                                            |
|          +-----------------------+----------------------+                     |
|          |                                              |                     |
|    +-----v------+                                +------v---------+           |
|    | Snapshot    |                                | CDC Engine     |           |
|    | Engine      |                                |                |           |
|    |             |                                | Debezium +     |           |
|    | Chunking    |                                | Kafka consumer |           |
|    | Parallel    |                                +------^---------+           |
|    | Checkpoint  |                                       |                     |
|    +-----+------+                                       |                     |
|          |                                              |                     |
|          |                                              |                     |
|    +-----v-------------------+                    +-----v---------------+     |
|    | PostgreSQL State Store   |                    |  Kafka Event Backbone |     |
|    | schema, metadata, audit  |                    |-----------------------|     |
|    | checkpoints, offsets     |                    | topics + retry + dlq  |     |
|    +--------------------------+                    +------+----------------+     |
|                                                              |              |
|           +--------------------------------------------------+--------------+|
|           |                                                                 ||
| +---------v---------+   +--------------------+   +----------------------+   ||
| | SourceAdapter     |   | CDCAdapter         |   | TargetAdapter        |   ||
| | cloud / on-prem   |   | Debezium connectors|   | cloud / database     |   ||
| +---------+---------+   +---------+----------+   +----------+-----------+   ||
|           |                        |                         |              ||
|           |                        |                         |              ||
|  +--------v--------+       +-------v--------+        +-------v--------+     ||
|  | Source Systems   |       | Kafka / Debezium|       | Target Systems  |     ||
|  | DB / Storage     |       +----------------+       | DB / Storage    |     ||
|  +------------------+                               +----------------+     ||
+------------------------------------------------------------------------------+
```

---

## Folder Structure

```
CloudHopper/
  docs/
    data_sync_subsystem.md
  sync_subsystem/
    __init__.py
    configs/
      settings.py
    domain/
      models.py
      events.py
    application/
      agents/
        base.py
        sync_planning_agent.py
        conflict_resolution_agent.py
        validation_agent.py
        recovery_agent.py
      services/
        sync_control_plane.py
    infrastructure/
      kafka/
        topics.py
        producer.py
        consumer.py
      postgres/
        repository.py
        schema.sql
      temporal/
        activities.py
        workflows.py
      debezium/
        connector_manager.py
        event_processor.py
        offset_tracker.py
        replay_service.py
        schema_evolution.py
      adapters/
        base.py
        source.py
        target.py
        storage.py
        cdc.py
        aws_adapter.py
        azure_adapter.py
        gcp_adapter.py
        onprem_adapter.py
    validation/
      validators.py
    reconciliation/
      report.py
    workers/
      snapshot_worker.py
      cdc_worker.py
      validation_worker.py
    monitoring/
      metrics.py
      tracing.py
      logging.py
    api/
      routes.py
      schemas.py
    tests/
      unit/
      integration/
```

---

## Domain Model

### Core entities

- `SyncJob`: orchestration unit for a migration sync operation.
- `SyncCheckpoint`: persistent snapshot progress and CDC offsets.
- `SyncPolicy`: rules for consistency, parallelism, and cutover.
- `SyncEvent`: domain event published to Kafka and state store.
- `ValidationReport`: data quality and readiness decision output.
- `ConflictResolutionPlan`: action plan for duplicates, ordering, schema mismatch.

### Enums

- `SyncPhase`: `DISCOVERY`, `SNAPSHOT`, `CDC`, `VALIDATION`, `CUTOVER`, `RECOVERY`
- `SyncStrategy`: `FULL_SNAPSHOT`, `CDC_ONLY`, `HYBRID`, `REPLAY`
- `AdapterType`: `AWS`, `AZURE`, `GCP`, `ONPREM`, `DATABASE`, `STORAGE`, `KUBERNETES`

---

## Temporal Workflow Definitions

### Workflows

- `SnapshotWorkflow`
- `CDCWorkflow`
- `ValidationWorkflow`
- `ConflictResolutionWorkflow`
- `CutoverWorkflow`
- `RecoveryWorkflow`

### Workflow behavior

- `signals()` used for cutover approval, schema change notifications, and manual recovery triggers.
- `timers()` used for health checks, lag windows, checkpoint timeouts.
- `child workflows()` used to split large sync jobs into table-level or object-level subtasks.
- `workflow versioning` is enabled through version constants and `workflow_version()` calls.

---

## Kafka Topic Design

### Topics

- `sync.snapshot.started`
- `sync.snapshot.completed`
- `sync.cdc.events`
- `sync.validation.events`
- `sync.conflict.events`
- `sync.recovery.events`
- `sync.audit.events`
- `sync.cutover.events`

### Design rules

- Partition by sync job ID and source namespace.
- Use compacted topics for offsets and reconciliation state.
- Use retry topics and DLQ for processor failures.
- Enforce idempotent producer configuration.
- Decouple workload from temporal signals using event-backed state.

---

## PostgreSQL Schema

### Responsibilities

- workflow metadata
- sync checkpoints
- CDC offset tracking
- migration metadata
- audit logs
- reconciliation reports
- agent decisions

### Schema artifacts

- `sync_jobs`
- `sync_checkpoints`
- `sync_offsets`
- `sync_audit_logs`
- `sync_reconciliation_reports`
- `sync_agent_decisions`

---

## Agent Architecture

### Agent contract

- `reason()` returns the decision context and confidence.
- `plan()` generates an actionable execution plan.
- `execute()` applies plan decisions to the system.
- `evaluate()` scores results and adjusts future decisions.

### Agents

- `SyncPlanningAgent`
- `ConflictResolutionAgent`
- `ValidationAgent`
- `RecoveryAgent`

Each agent is built as a policy-driven service with a pluggable evaluation engine.

---

## API Contracts

### REST endpoints (FastAPI)

- `POST /sync/jobs` — start a new sync job
- `GET /sync/jobs/{job_id}` — inspect sync metadata
- `POST /sync/jobs/{job_id}/cutover` — request cutover readiness
- `GET /sync/jobs/{job_id}/validation` — fetch validation results
- `POST /sync/jobs/{job_id}/recover` — trigger recovery workflow
- `GET /sync/agents/{agent_name}/plan` — inspect agent plan

### Event API

- Domain events are published to Kafka with serialized envelope metadata.
- Temporal signals are mapped to event stream actions for audit and replay.

---

## Sequence Diagrams

### Snapshot flow

1. API receives sync request.
2. Sync Control Plane creates job metadata in PostgreSQL.
3. Temporal `SnapshotWorkflow` starts.
4. Snapshot Engine snapshots source in chunks.
5. Checkpoints are persisted.
6. Snapshot completion event published to Kafka.
7. Validation agent starts child validation workflow.

### CDC flow

1. Debezium captures source changes.
2. CDC connector publishes events to `sync.cdc.events`.
3. Sync Processor consumes events.
4. Ordering and idempotency enforcement occurs.
5. Target adapter applies changes.
6. Offsets persist in PostgreSQL.
7. ConflictResolutionAgent evaluates and emits remediation.

---

## Failure Recovery Design

- Workflows use retry and backoff policies.
- Checkpoints allow snapshot resume after partial failure.
- CDC offset store provides at-least-once recovery and replay.
- Dead-letter and retry topics isolate poisoned events.
- Recovery workflows rebuild state using stored metadata and replay.
- Agentic recovery chooses between `replay`, `rollback`, or `pause` based on failure type.

---

## Scaling Strategy

- Horizontal workers for snapshot chunks and CDC partitions.
- Kafka consumer groups for `sync.cdc.events`.
- Partition-aware target execution.
- Multi-tenant sync job isolation by job ID and namespace.
- Auto-scale worker pools based on lag, throughput, and error rate.
- PostgreSQL write scaling via optimized batch checkpoints and indices.

---

## Deployment Architecture

- Independent subsystem module deployable as containerized service.
- Temporal workflows executed in Temporal cluster.
- Kafka cluster for events and retries.
- PostgreSQL for state store and operational metadata.
- Observability via OpenTelemetry + Prometheus + Grafana.
- External connectors for Neo4j and Vector DB remain outside the sync path.

---

## Future Extensibility Plan

- Add new adapters for new cloud providers without changing core engine.
- Add storage sync and Kubernetes object sync adapters.
- Add policy templating for compliance and data residency.
- Add ML-based anomaly detection for drift and cutover risk.
- Add adaptive autoscaling into the Agent Decision Layer.

---

## Production Readiness Checklist

- [ ] Modular domain-driven architecture
- [ ] Proven Temporal workflow patterns
- [ ] Kafka event backbone and DLQ strategy
- [ ] PostgreSQL persistence for metadata, checkpoints, offsets
- [ ] Adapter boundary for cloud-agnostic behavior
- [ ] Observability hooks for metrics & distributed tracing
- [ ] Recovery workflow and replay support
- [ ] Schema migration artifacts and SQL scripts
- [ ] API contract for job lifecycle and control plane
- [ ] Autonomous agent contract and decision model

---

## Repository Integration Notes

This subsystem is intentionally self-contained under `CloudHopper/sync_subsystem`. It is designed to integrate with the existing platform by:

- calling the same PostgreSQL state store used by `control-plane`
- emitting standard Kafka domain events
- exposing a FastAPI-based control plane extension
- implementing Temporal workflows that can be orchestrated from the platform's workflow engine

The next step is to wire the module into the existing deployment manifests and connect it to the platform's service discovery and ingress path.
