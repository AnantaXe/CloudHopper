from fastapi import APIRouter, FastAPI

from shared.models.discovery import (
    DiscoveryRequest,
)

from control_plane.services.workflow_service import (
    WorkflowService
)

router = APIRouter()

app = FastAPI()
workflow_service = WorkflowService()


# @app.post("/discover")
# async def discover(
#     request: DiscoveryRequest
# ):

#     from control_plane.workflows.discovery_workflow import (
#         start_discovery_workflow
#     )

#     workflow_id = await start_discovery_workflow(
#         request.provider
#     )

#     return {
#         "workflow_id": workflow_id,
#         "status": "STARTED"
#     }

@router.post("/discover")
async def discover(
    request: DiscoveryRequest
):
    
    workflow = await workflow_service.create_discovery_workflow(
        provider=request.provider
    )

    return workflow