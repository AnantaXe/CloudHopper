from __future__ import annotations

from typing import Any


class SnapshotActivities:
    async def capture_chunk(self, job_id: str, object_path: str, chunk_index: int, chunk_size: int) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "object_path": object_path,
            "chunk_index": chunk_index,
            "chunk_size": chunk_size,
            "status": "captured",
        }

    async def persist_checkpoint(self, job_id: str, object_path: str, checkpoint: dict[str, Any]) -> None:
        return None


class CDCActivities:
    async def consume_changes(self, job_id: str, topic: str, partition: int, offset: int) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "topic": topic,
            "partition": partition,
            "offset": offset,
            "status": "consumed",
        }

    async def apply_change(self, job_id: str, event: dict[str, Any]) -> None:
        return None
