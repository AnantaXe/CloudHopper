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

    async def persist_validation_result(self, job_id: str, validation_result: dict[str, object]) -> None:
        await self.repository.insert_validation_result(job_id, validation_result)

    async def get_validation_result(self, job_id: str) -> dict[str, object] | None:
        return await self.repository.get_validation_result(job_id)

    async def persist_reconciliation_report(self, job_id: str, report_type: str, report_payload: dict[str, object]) -> None:
        await self.repository.insert_reconciliation_report(job_id, report_type, report_payload)

    async def get_reconciliation_reports(self, job_id: str) -> list[dict[str, object]]:
        return await self.repository.get_reconciliation_reports(job_id)

    async def persist_agent_decision(self, job_id: str, agent_name: str, decision_payload: dict[str, object], confidence_score: float) -> None:
        await self.repository.insert_agent_decision(job_id, agent_name, decision_payload, confidence_score)
