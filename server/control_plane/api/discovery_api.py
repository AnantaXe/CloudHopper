from fastapi import APIRouter, FastAPI

from shared.models.discovery import (
    DiscoveryRequest,
)

from control_plane.services.workflow_service import (
    WorkflowService
)

router = APIRouter()

workflow_service = WorkflowService()

@router.post("/discover")
async def discover(
    request: DiscoveryRequest
):
    
    workflow = await workflow_service.create_discovery_workflow(
        provider=request.provider
    )

    return workflow