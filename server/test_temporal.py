import asyncio

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker


@workflow.defn
class TestWorkflow:

    @workflow.run
    async def run(self, name: str) -> str:
        return f"Hello {name}"


async def main():
    print("Connecting...", flush=True)

    client = await Client.connect("localhost:7233")

    print("Connected...", flush=True)

    worker = Worker(
        client,
        task_queue="test-task-queue",
        workflows=[TestWorkflow],
    )

    print("Worker created...", flush=True)

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
