from __future__ import annotations

from .base import AgentBase
from datetime import datetime
from typing import Any


class ConflictResolutionAgent(AgentBase):
    def reason(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "reason": "Analyze conflict signals to determine corrective remediation.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "context": context,
        }

    def plan(self, context: dict[str, Any]) -> dict[str, Any]:
        actions: list[dict[str, Any]] = []
        duplicate_count = context.get("duplicate_count", 0)
        out_of_order_count = context.get("out_of_order_count", 0)
        schema_mismatch = context.get("schema_mismatch", False)

        if duplicate_count:
            actions.append({"action": "deduplicate", "count": duplicate_count})
        if out_of_order_count:
            actions.append({"action": "reorder", "count": out_of_order_count})
        if schema_mismatch:
            actions.append({"action": "schema_migration", "details": context.get("schema_mismatch_details")})

        return {
            "resolution_actions": actions,
            "recommendation": "replay" if duplicate_count or out_of_order_count else "validate_schema",
        }

    def execute(self, plan: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": "conflict_resolution_applied",
            "plan": plan,
        }

    def evaluate(self, result: dict[str, Any]) -> dict[str, Any]:
        return {
            "evaluation": "conflict_resolution_complete",
            "resolved_actions": len(result.get("plan", {}).get("resolution_actions", [])),
        }
