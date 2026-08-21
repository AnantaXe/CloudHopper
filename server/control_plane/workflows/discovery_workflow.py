from datetime import timedelta
from uuid import uuid4

from temporalio import workflow



@workflow.defn
class DiscoveryWorkflow:

    @workflow.run
    async def run(
        self,
        provider: str
    ):

        return await workflow.execute_activity(
            "run_discovery",
            provider,
            start_to_close_timeout=timedelta(minutes=5)
        )


async def start_discovery_workflow(
    provider: str
):

    workflow_id = str(uuid4())

    print(
        f"Workflow Started: {workflow_id}"
    )

    return workflow_id