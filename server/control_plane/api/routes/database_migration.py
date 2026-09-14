from fastapi import APIRouter, Depends, HTTPException
from agent_runtime.database.domain.model import DatabaseMigrationContext, DatabaseMigrationRequest
import uuid

from agent_runtime.database.workflow.database_migration_workflow import DatabaseMigrationWorkflow
from control_plane.services.temporal_client import TemporalClient

router = APIRouter(
    prefix="/api/v1/database-migrations",
    tags=["Database Migrations"],
)

@router.post("")
async def create_database_migration(request: DatabaseMigrationRequest):
    """
    Create a new database migration request.
    """
    migration_id = str(uuid.uuid4())

    context = DatabaseMigrationContext(migration_id=migration_id, request=request)

    client = await TemporalClient.get_client()
    
    await client.start_workflow(
        DatabaseMigrationWorkflow.run,
        context,
        id=f"database-migration-{migration_id}",
        task_queue="database_migration_task_queue",
    )

    return {"migration_id": migration_id, "status": "started"}