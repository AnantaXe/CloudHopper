from __future__ import annotations

from .base import SourceAdapter, TargetAdapter, StorageAdapter, CDCAdapter
from typing import Any


class AWSSourceAdapter(SourceAdapter):
    async def discover_schema(self) -> dict[str, Any]:
        return {"provider": "aws", "type": "database_or_storage"}

    async def read_snapshot(self, object_path: str, chunk_size: int) -> list[dict[str, Any]]:
        return []

    async def describe_source(self) -> dict[str, Any]:
        return {"source": "aws", "description": "AWS source adapter placeholder"}


class AWSTargetAdapter(TargetAdapter):
    async def apply_snapshot_batch(self, records: list[dict[str, Any]]) -> None:
        return None

    async def apply_cdc_event(self, event: dict[str, Any]) -> None:
        return None

    async def validate_target(self, sample_size: int) -> dict[str, Any]:
        return {"sample_size": sample_size, "status": "ok"}


class AWSStorageAdapter(StorageAdapter):
    async def checkpoint(self, job_id: str, payload: dict[str, Any]) -> None:
        return None

    async def read_checkpoint(self, job_id: str) -> dict[str, Any] | None:
        return None


class AWSCDCAdapter(CDCAdapter):
    async def register_source(self, source_definition: dict[str, Any]) -> dict[str, Any]:
        return {"status": "registered", "provider": "aws"}

    async def unsubscribe_source(self, source_name: str) -> None:
        return None

    async def read_changes(self, source_name: str, offset: dict[str, Any]) -> list[dict[str, Any]]:
        return []
