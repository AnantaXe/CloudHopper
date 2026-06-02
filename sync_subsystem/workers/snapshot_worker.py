from __future__ import annotations

from typing import Any


class SnapshotWorker:
    async def execute_snapshot_chunk(self, job_id: str, object_path: str, chunk_index: int, chunk_size: int) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "object_path": object_path,
            "chunk_index": chunk_index,
            "chunk_size": chunk_size,
            "status": "completed",
        }

    async def resume_snapshot(self, job_id: str, checkpoint: dict[str, Any]) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "resume_from": checkpoint,
            "status": "resumed",
        }
