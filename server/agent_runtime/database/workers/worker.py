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
from agent_runtime.database.activities.compatibility import (
    compatibility
)
from agent_runtime.database.activities.architecture_recommender import (
    recommend_architect
)
from agent_runtime.database.activities.strategy import (
    determine_strategy
)
from agent_runtime.database.activities.migration_plan import (
    generate_mig_plan
)
from agent_runtime.database.activities.validate_migration import (
    validate_mig_plan
)
from agent_runtime.database.activities.provision_target import (
    provision_target_database
)
from agent_runtime.database.activities.request_approval import (
    request_migration_approval
) 

async def run_worker():

    print("Connecting to Temporal...", flush=True)
    client = await Client.connect("localhost:7233", data_converter=pydantic_data_converter,)

    print("Connected to Temporal", flush=True)

    print("Creating Worker...", flush=True)

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
            generate_mig_plan,
            validate_mig_plan,
            provision_target_database,
            request_migration_approval,
            compatibility,
            recommend_architect,
            determine_strategy,
        ],
    )

    print(f"Worker created : {worker}", flush=True)

    await worker.run()

    print("Worker running...", flush=True)

if __name__ == "__main__":
    asyncio.run(run_worker())