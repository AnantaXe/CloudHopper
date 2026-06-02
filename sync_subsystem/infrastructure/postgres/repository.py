from __future__ import annotations

import asyncpg
from typing import Any

from ...domain.models import SyncJobMetadata
from ...configs.settings import PostgresSettings


class PostgresMetadataRepository:
    def __init__(self, settings: PostgresSettings):
        self.settings = settings
        self.pool: asyncpg.pool.Pool | None = None

    async def connect(self) -> None:
        if self.pool is None:
            self.pool = await asyncpg.create_pool(dsn=self.settings.dsn, max_size=self.settings.max_connections)

    async def close(self) -> None:
        if self.pool is not None:
            await self.pool.close()
            self.pool = None

    async def insert_sync_job(self, job: SyncJobMetadata) -> None:
        await self.connect()
        assert self.pool is not None
        query = """
            INSERT INTO sync_subsystem.sync_jobs
            (job_id, tenant_id, source_adapter, target_adapter, strategy, phase, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (job_id) DO UPDATE SET updated_at = NOW()
        """
        await self.pool.execute(
            query,
            job.job_id,
            job.tenant_id,
            job.source_adapter.value,
            job.target_adapter.value,
            job.strategy.value,
            job.phase.value,
            job.metadata,
        )

    async def get_sync_job(self, job_id: str) -> SyncJobMetadata | None:
        await self.connect()
        assert self.pool is not None
        row = await self.pool.fetchrow(
            "SELECT job_id, tenant_id, source_adapter, target_adapter, strategy, phase, started_at, completed_at, metadata FROM sync_subsystem.sync_jobs WHERE job_id = $1",
            job_id,
        )
        if row is None:
            return None
        return SyncJobMetadata(
            job_id=row["job_id"],
            tenant_id=row["tenant_id"],
            source_adapter=row["source_adapter"],
            target_adapter=row["target_adapter"],
            strategy=row["strategy"],
            phase=row["phase"],
            started_at=row["started_at"].isoformat() if row["started_at"] else None,
            completed_at=row["completed_at"].isoformat() if row["completed_at"] else None,
            metadata=row["metadata"],
        )

    async def update_job_phase(self, job_id: str, phase: str) -> None:
        await self.connect()
        assert self.pool is not None
        await self.pool.execute(
            "UPDATE sync_subsystem.sync_jobs SET phase = $1, updated_at = NOW() WHERE job_id = $2",
            phase,
            job_id,
        )

    async def insert_audit_event(self, job_id: str, event_type: str, payload: dict[str, Any]) -> None:
        await self.connect()
        assert self.pool is not None
        await self.pool.execute(
            "INSERT INTO sync_subsystem.sync_audit_logs (job_id, event_type, event_payload) VALUES ($1, $2, $3)",
            job_id,
            event_type,
            payload,
        )
