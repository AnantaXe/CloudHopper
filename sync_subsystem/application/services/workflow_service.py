from __future__ import annotations

from typing import Any
from ..configs.settings import TemporalSettings

try:
    from temporalio.client import Client
    from temporalio.common import RetryPolicy
except ImportError:  # pragma: no cover
    Client = None
    RetryPolicy = None


class TemporalWorkflowService:
    def __init__(self, settings: TemporalSettings) -> None:
        self.settings = settings
        self.client: Client | None = None

    async def connect(self) -> None:
        if self.client is None and Client is not None:
            self.client = await Client.connect(self.settings.host, namespace=self.settings.namespace)

    async def start_workflow(self, workflow_name: str, job_id: str, payload: dict[str, Any]) -> Any:
        await self.connect()
        if self.client is None:
            return None
        return await self.client.start_workflow(
            workflow_name,
            job_id,
            payload,
            id=f"{workflow_name}-{job_id}",
            task_queue=self.settings.task_queue,
            retry_policy=RetryPolicy(maximum_attempts=3) if RetryPolicy else None,
        )
