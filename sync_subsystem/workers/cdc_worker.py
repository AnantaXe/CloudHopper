from __future__ import annotations

from typing import Any


class CDCWorker:
    async def process_event(self, job_id: str, event: dict[str, Any]) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "event_id": event.get("id"),
            "status": "processed",
        }

    async def handle_replay(self, job_id: str, event_batch: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "replay_count": len(event_batch),
            "status": "replayed",
        }
