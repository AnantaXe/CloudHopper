import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.pydantic import pydantic_data_converter

from agent_runtime.database.workflow.database_migration_workflow import (
    DatabaseMigrationWorkflow,
)
from agent_runtime.database.activities.cutover import (
    cutover,
)
from agent_runtime.database.activities.cdc import (
    start_cdc,
)  

from agent_runtime.database.activities.assessment import (
    assess_database
)
from agent_runtime.database.activities.rollback import (
    rollback
)
from agent_runtime.database.activities.bulk_load import (
    initial_bulk_load
)

async def run_worker():

    print("Connecting to Temporal...")
    client = await Client.connect("localhost:7233", data_converter=pydantic_data_converter,)

    print("Connected to Temporal")

    worker = Worker(
        client,
        task_queue="database_migration_task_queue",
        workflows=[DatabaseMigrationWorkflow],
        activities=[
            assess_database,
            initial_bulk_load,
            start_cdc,
            cutover,
            rollback,
        ],
    )

    await worker.run()

if __name__ == "__main__":
    asyncio.run(run_worker())