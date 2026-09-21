import asyncio

from temporalio.client import Client

from test_temporal_asyncpg import TestWorkflow


async def main():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        TestWorkflow.run,
        id="asyncpg-test-1",
        task_queue="asyncpg_test_queue",
    )

    print("RESULT:", result)


asyncio.run(main())
