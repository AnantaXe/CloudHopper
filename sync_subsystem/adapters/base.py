from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SourceAdapter(ABC):
    @abstractmethod
    async def discover_schema(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def read_snapshot(self, object_path: str, chunk_size: int) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def describe_source(self) -> dict[str, Any]:
        raise NotImplementedError


class TargetAdapter(ABC):
    @abstractmethod
    async def apply_snapshot_batch(self, records: list[dict[str, Any]]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def apply_cdc_event(self, event: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def validate_target(self, sample_size: int) -> dict[str, Any]:
        raise NotImplementedError


class StorageAdapter(ABC):
    @abstractmethod
    async def checkpoint(self, job_id: str, payload: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_checkpoint(self, job_id: str) -> dict[str, Any] | None:
        raise NotImplementedError


class CDCAdapter(ABC):
    @abstractmethod
    async def register_source(self, source_definition: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe_source(self, source_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_changes(self, source_name: str, offset: dict[str, Any]) -> list[dict[str, Any]]:
        raise NotImplementedError
