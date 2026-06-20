from __future__ import annotations

from typing import Any
from ..agents import (
    SyncPlanningAgent,
    ValidationAgent,
    ConflictResolutionAgent,
    RecoveryAgent,
)
from ..infrastructure.postgres.repository import PostgresMetadataRepository


class AgentDecisionEngine:
    def __init__(self, repository: PostgresMetadataRepository):
        self.repository = repository
        self.planner = SyncPlanningAgent()
        self.validator = ValidationAgent()
        self.conflict_resolver = ConflictResolutionAgent()
        self.recovery_agent = RecoveryAgent()

    async def record_decision(self, job_id: str, agent_name: str, decision: dict[str, Any], confidence: float = 0.0) -> None:
        await self.repository.insert_agent_decision(job_id, agent_name, decision, confidence)

    async def plan_sync(self, context: dict[str, Any]) -> dict[str, Any]:
        plan = self.planner.plan(context)
        await self.record_decision(context["job_id"], "SyncPlanningAgent", plan, 0.9)
        return plan

    async def plan_validation(self, job_id: str, context: dict[str, Any]) -> dict[str, Any]:
        reason = self.validator.reason(context)
        plan = self.validator.plan(context)
        await self.record_decision(job_id, "ValidationAgent", {"reason": reason, "plan": plan}, 0.95)
        return plan

    async def plan_conflict_resolution(self, job_id: str, context: dict[str, Any]) -> dict[str, Any]:
        plan = self.conflict_resolver.plan(context)
        await self.record_decision(job_id, "ConflictResolutionAgent", plan, 0.92)
        return plan

    async def plan_recovery(self, job_id: str, context: dict[str, Any]) -> dict[str, Any]:
        plan = self.recovery_agent.plan(context)
        await self.record_decision(job_id, "RecoveryAgent", plan, 0.95)
        return plan
