from uuid import uuid4

from control_plane.services.temporal_client import (
    TemporalClient
)

from control_plane.workflows.discovery_workflow import (
    DiscoveryWorkflow
)


class WorkflowService:

    async def create_discovery_workflow(
        self,
        provider: str
    ):

        workflow_id = str(uuid4())

        client = await TemporalClient.get_client()

        handle = await client.start_workflow(
            DiscoveryWorkflow.run,
            provider,
            id=workflow_id,
            task_queue="discovery"
        )

        return {
            "workflow_id": handle.id,
            "run_id": handle.result_run_id,
            "status": "STARTED"
        }