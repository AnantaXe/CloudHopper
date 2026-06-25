from fastapi import APIRouter

from control_plane.services.temporal_client import TemporalClient

router = APIRouter()

workflows = {}


# @router.get(
#     "/workflows/{workflow_id}"
# )
# async def get_workflow(
#     workflow_id: str
# ):

#     return workflows.get(
#         workflow_id,
#         {"error": "not found"}
#     )

@router.get("/workflows/{workflow_id}")
async def get_workflow_status(
    workflow_id: str
):
    client = await TemporalClient.get_client()

    handle = client.get_workflow_handle(workflow_id)

    desc = await handle.describe()

    return {
        "workflow_id": workflow_id,
        "status": desc.status.name
    }