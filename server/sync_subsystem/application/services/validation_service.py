from __future__ import annotations

from typing import Any
from ..domain.models import ValidationResult
from ..validation.validators import DataValidator
from ..infrastructure.postgres.repository import PostgresMetadataRepository


class DataValidationService:
    def __init__(self, repository: PostgresMetadataRepository):
        self.repository = repository
        self.validator = DataValidator()

    async def validate_row_counts(self, job_id: str, source_rows: int, target_rows: int) -> dict[str, Any]:
        result = await self.validator.compare_row_counts(source_rows, target_rows, job_id)
        await self.repository.insert_validation_result(job_id, result)
        return result

    async def validate_checksums(self, job_id: str, source_checksum: str, target_checksum: str) -> dict[str, Any]:
        result = await self.validator.compare_checksums(source_checksum, target_checksum, job_id)
        await self.repository.insert_validation_result(job_id, result)
        return result

    async def build_validation_result(self, job_id: str, details: dict[str, Any]) -> ValidationResult:
        return await self.validator.build_validation_result(job_id, details)
