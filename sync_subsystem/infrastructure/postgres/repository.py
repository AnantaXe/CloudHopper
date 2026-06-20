from __future__ import annotations

import asyncpg
from typing import Any

from ...domain.models import SyncJobMetadata
from ...configs.settings import PostgresSettings


class PostgresMetadataRepository:
    def __init__(self, settings: PostgresSettings):
        self.settings = settings
        self.pool: asyncpg.pool.Pool | None = None

    @property
    def schema(self) -> str:
        return self.settings.schema

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
        query = f"""
            INSERT INTO {self.schema}.sync_jobs
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
            f"SELECT job_id, tenant_id, source_adapter, target_adapter, strategy, phase, started_at, completed_at, metadata FROM {self.schema}.sync_jobs WHERE job_id = $1",
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
            f"UPDATE {self.schema}.sync_jobs SET phase = $1, updated_at = NOW() WHERE job_id = $2",
            phase,
            job_id,
        )

    async def insert_audit_event(self, job_id: str, event_type: str, payload: dict[str, Any]) -> None:
        await self.connect()
        assert self.pool is not None
        await self.pool.execute(
            f"INSERT INTO {self.schema}.sync_audit_logs (job_id, event_type, event_payload) VALUES ($1, $2, $3)",
            job_id,
            event_type,
            payload,
        )

    async def insert_validation_result(self, job_id: str, validation_result: dict[str, Any]) -> None:
        await self.connect()
        assert self.pool is not None
        await self.pool.execute(
            f"INSERT INTO {self.schema}.sync_validation_results (job_id, row_count_match, checksum_match, drift_score, sample_mismatch_count, details) VALUES ($1, $2, $3, $4, $5, $6)",
            job_id,
            validation_result.get("row_count_match"),
            validation_result.get("checksum_match"),
            validation_result.get("drift_score"),
            validation_result.get("sample_mismatch_count"),
            validation_result,
        )

    async def get_validation_result(self, job_id: str) -> dict[str, Any] | None:
        await self.connect()
        assert self.pool is not None
        row = await self.pool.fetchrow(
            f"SELECT job_id, row_count_match, checksum_match, drift_score, sample_mismatch_count, details FROM {self.schema}.sync_validation_results WHERE job_id = $1 ORDER BY created_at DESC LIMIT 1",
            job_id,
        )
        return dict(row) if row else None

    async def insert_reconciliation_report(self, job_id: str, report_type: str, report_payload: dict[str, Any]) -> None:
        await self.connect()
        assert self.pool is not None
        await self.pool.execute(
            f"INSERT INTO {self.schema}.sync_reconciliation_reports (job_id, report_type, report_payload, status) VALUES ($1, $2, $3, $4)",
            job_id,
            report_type,
            report_payload,
            "created",
        )

    async def get_reconciliation_reports(self, job_id: str) -> list[dict[str, Any]]:
        await self.connect()
        assert self.pool is not None
        rows = await self.pool.fetch(
            f"SELECT report_id, job_id, report_type, report_payload, status, created_at, updated_at FROM {self.schema}.sync_reconciliation_reports WHERE job_id = $1 ORDER BY created_at DESC",
            job_id,
        )
        return [dict(row) for row in rows]

    async def insert_agent_decision(self, job_id: str, agent_name: str, decision_payload: dict[str, Any], confidence_score: float) -> None:
        await self.connect()
        assert self.pool is not None
        await self.pool.execute(
            f"INSERT INTO {self.schema}.sync_agent_decisions (job_id, agent_name, decision_type, decision_payload, confidence_score) VALUES ($1, $2, $3, $4, $5)",
            job_id,
            agent_name,
            "decision",
            decision_payload,
            confidence_score,
        )
