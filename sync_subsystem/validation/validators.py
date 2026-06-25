from __future__ import annotations

from typing import Any

from ..domain.models import ValidationResult


class DataValidator:
    async def compare_row_counts(self, source_rows: int, target_rows: int, job_id: str) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "row_count_match": source_rows == target_rows,
            "source_rows": source_rows,
            "target_rows": target_rows,
        }

    async def compare_checksums(self, source_checksum: str, target_checksum: str, job_id: str) -> dict[str, Any]:
        return {
            "job_id": job_id,
            "checksum_match": source_checksum == target_checksum,
            "source_checksum": source_checksum,
            "target_checksum": target_checksum,
        }

    async def build_validation_result(self, job_id: str, details: dict[str, Any]) -> ValidationResult:
        return ValidationResult(job_id=job_id, details=details)
