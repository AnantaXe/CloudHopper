from __future__ import annotations

from enum import Enum
from typing import Any
from pydantic import BaseModel, Field


class SyncPhase(str, Enum):
    DISCOVERY = "DISCOVERY"
    SNAPSHOT = "SNAPSHOT"
    CDC = "CDC"
    VALIDATION = "VALIDATION"
    CUTOVER = "CUTOVER"
    RECOVERY = "RECOVERY"


class SyncStrategy(str, Enum):
    FULL_SNAPSHOT = "FULL_SNAPSHOT"
    CDC_ONLY = "CDC_ONLY"
    HYBRID = "HYBRID"
    REPLAY = "REPLAY"


class AdapterType(str, Enum):
    AWS = "AWS"
    AZURE = "AZURE"
    GCP = "GCP"
    ON_PREM = "ON_PREM"
    DATABASE = "DATABASE"
    STORAGE = "STORAGE"
    KUBERNETES = "KUBERNETES"


class SyncJobMetadata(BaseModel):
    job_id: str
    tenant_id: str
    source_adapter: AdapterType
    target_adapter: AdapterType
    strategy: SyncStrategy
    phase: SyncPhase = SyncPhase.DISCOVERY
    started_at: str | None = None
    completed_at: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class SyncCheckpoint(BaseModel):
    job_id: str
    object_path: str
    completed_chunks: int = 0
    total_chunks: int = 0
    last_processed_key: str | None = None
    last_updated_at: str | None = None


class OffsetCheckpoint(BaseModel):
    job_id: str
    source_name: str
    topic: str
    partition: int
    offset: int
    updated_at: str | None = None


class ValidationResult(BaseModel):
    job_id: str
    phase: SyncPhase = SyncPhase.VALIDATION
    row_count_match: bool = False
    checksum_match: bool = False
    drift_score: float = 0.0
    sample_mismatch_count: int = 0
    details: dict[str, Any] = Field(default_factory=dict)


class ConflictResolutionAction(BaseModel):
    job_id: str
    conflict_id: str
    resolution_type: str
    reason: str
    details: dict[str, Any] = Field(default_factory=dict)
