from __future__ import annotations

from ..configs.settings import SyncSettings
from ..domain.models import SyncJobMetadata
from ..infrastructure.postgres.repository import PostgresMetadataRepository


class SyncControlPlaneService:
    def __init__(self, settings: SyncSettings, repository: PostgresMetadataRepository):
        self.settings = settings
        self.repository = repository

    async def create_job(self, job: SyncJobMetadata) -> SyncJobMetadata:
        await self.repository.insert_sync_job(job)
        return job

    async def get_job(self, job_id: str) -> SyncJobMetadata | None:
        return await self.repository.get_sync_job(job_id)

    async def mark_phase(self, job_id: str, phase: str) -> None:
        await self.repository.update_job_phase(job_id, phase)

    async def publish_snapshot_started(self, job_id: str, payload: dict[str, object]) -> None:
        await self.repository.insert_audit_event(job_id, "SNAPSHOT_STARTED", payload)

    async def publish_snapshot_completed(self, job_id: str, payload: dict[str, object]) -> None:
        await self.repository.insert_audit_event(job_id, "SNAPSHOT_COMPLETED", payload)
