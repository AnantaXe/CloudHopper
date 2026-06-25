from __future__ import annotations

from typing import Any


class ReconciliationReportBuilder:
    def build_row_count_report(self, source_count: int, target_count: int) -> dict[str, Any]:
        return {
            "row_count_passed": source_count == target_count,
            "source_count": source_count,
            "target_count": target_count,
        }

    def build_checksum_report(self, source_checksum: str, target_checksum: str) -> dict[str, Any]:
        return {
            "checksum_passed": source_checksum == target_checksum,
            "source_checksum": source_checksum,
            "target_checksum": target_checksum,
        }

    def build_drift_report(self, drift_score: float, drift_threshold: float) -> dict[str, Any]:
        return {
            "drift_score": drift_score,
            "drift_threshold": drift_threshold,
            "drift_detected": drift_score > drift_threshold,
        }
