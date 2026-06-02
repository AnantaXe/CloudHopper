from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class SyncEventType(str, Enum):
    SNAPSHOT_STARTED = "sync.snapshot.started"
    SNAPSHOT_COMPLETED = "sync.snapshot.completed"
    CDC_EVENT = "sync.cdc.events"
    VALIDATION_EVENT = "sync.validation.events"
    CONFLICT_EVENT = "sync.conflict.events"
    RECOVERY_EVENT = "sync.recovery.events"
    CUTOVER_EVENT = "sync.cutover.events"
    AUDIT_EVENT = "sync.audit.events"


class EventEnvelope(BaseModel):
    event_type: SyncEventType
    job_id: str
    timestamp: str
    payload: dict[str, object] = Field(default_factory=dict)
    metadata: dict[str, object] = Field(default_factory=dict)


class SnapshotStartedEvent(EventEnvelope):
    event_type: SyncEventType = SyncEventType.SNAPSHOT_STARTED


class SnapshotCompletedEvent(EventEnvelope):
    event_type: SyncEventType = SyncEventType.SNAPSHOT_COMPLETED


class CDCEvent(EventEnvelope):
    event_type: SyncEventType = SyncEventType.CDC_EVENT


class ValidationEvent(EventEnvelope):
    event_type: SyncEventType = SyncEventType.VALIDATION_EVENT


class ConflictEvent(EventEnvelope):
    event_type: SyncEventType = SyncEventType.CONFLICT_EVENT


class RecoveryEvent(EventEnvelope):
    event_type: SyncEventType = SyncEventType.RECOVERY_EVENT


class CutoverEvent(EventEnvelope):
    event_type: SyncEventType = SyncEventType.CUTOVER_EVENT
