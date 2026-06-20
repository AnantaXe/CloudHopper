from __future__ import annotations

from typing import Any
from ..infrastructure.postgres.repository import PostgresMetadataRepository
from ..reconciliation.report import ReconciliationReportBuilder


class ReconciliationService:
    def __init__(self, repository: PostgresMetadataRepository):
        self.repository = repository
        self.builder = ReconciliationReportBuilder()

    async def reconcile_row_counts(self, job_id: str, source_count: int, target_count: int) -> dict[str, Any]:
        report = self.builder.build_row_count_report(source_count, target_count)
        await self.repository.insert_reconciliation_report(job_id, "row_count", report)
        return report

    async def reconcile_checksums(self, job_id: str, source_checksum: str, target_checksum: str) -> dict[str, Any]:
        report = self.builder.build_checksum_report(source_checksum, target_checksum)
        await self.repository.insert_reconciliation_report(job_id, "checksum", report)
        return report

    async def reconcile_drift(self, job_id: str, drift_score: float, drift_threshold: float) -> dict[str, Any]:
        report = self.builder.build_drift_report(drift_score, drift_threshold)
        await self.repository.insert_reconciliation_report(job_id, "drift", report)
        return report
