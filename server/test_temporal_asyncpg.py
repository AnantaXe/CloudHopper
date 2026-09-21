import asyncio

import asyncpg

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from datetime import timedelta


@activity.defn
async def test_database_connection() -> str:
    print("ACTIVITY: starting", flush=True)

    conn = await asyncpg.connect(
        user="cloudhopper",
        password="password",
        database="cloudhopper",
        host="localhost",
        port=5432,
        ssl=False,
    )

    print("ACTIVITY: PostgreSQL connected", flush=True)

    version = await conn.fetchval(
        "SHOW server_version"
    )

    print(
        f"ACTIVITY: PostgreSQL version = {version}",
        flush=True,
    )

    await conn.close()

    print("ACTIVITY: PostgreSQL connection closed", flush=True)

    return version


@workflow.defn
class TestWorkflow:

    @workflow.run
    async def run(self) -> str:
        return await workflow.execute_activity(
            test_database_connection,
            start_to_close_timeout=timedelta(seconds=30),
        )


async def main():
    print("Connecting to Temporal...", flush=True)

    client = await Client.connect(
        "localhost:7233"
    )

    print("Connected to Temporal", flush=True)

    worker = Worker(
        client,
        task_queue="asyncpg_test_queue",
        workflows=[TestWorkflow],
        activities=[test_database_connection],
    )

    print("Worker created", flush=True)

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())