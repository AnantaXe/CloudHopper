from __future__ import annotations

from pydantic import BaseModel
from typing import Any


class ValidationPayload(BaseModel):
    source_rows: int
    target_rows: int
    source_checksum: str | None = None
    target_checksum: str | None = None
    drift_score: float | None = None
    sample_mismatch_count: int | None = None
    details: dict[str, Any] = {}


class ReconciliationPayload(BaseModel):
    source_count: int | None = None
    target_count: int | None = None
    source_checksum: str | None = None
    target_checksum: str | None = None
    drift_score: float | None = None
    drift_threshold: float | None = None
    details: dict[str, Any] = {}


class RecoveryPayload(BaseModel):
    failure_type: str
    max_attempts: int | None = 5
    backoff_seconds: int | None = 30
    details: dict[str, Any] = {}


class AgentDecisionPayload(BaseModel):
    context: dict[str, Any]
