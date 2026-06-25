import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from control_plane.workflows.discovery_workflow import (
    DiscoveryWorkflow
)

from control_plane.activities.discovery_activity import (
    run_discovery
)


async def main():

    print("Connecting to Temporal...")

    client = await Client.connect(
        "localhost:7233"
    )

    print("Connected to Temporal")

    worker = Worker(
        client,
        task_queue="discovery",
        workflows=[
            DiscoveryWorkflow
        ],
        activities=[
            run_discovery
        ]
    )

    print("Worker polling queue: discovery")

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())