from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..application.services.sync_control_plane import SyncControlPlaneService
from ..domain.models import SyncJobMetadata

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/jobs", response_model=SyncJobMetadata)
async def create_sync_job(job: SyncJobMetadata, service: SyncControlPlaneService) -> SyncJobMetadata:
    return await service.create_job(job)


@router.get("/jobs/{job_id}", response_model=SyncJobMetadata)
async def get_sync_job(job_id: str, service: SyncControlPlaneService) -> SyncJobMetadata:
    job = await service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Sync job not found")
    return job


@router.post("/jobs/{job_id}/cutover")
async def request_cutover(job_id: str, service: SyncControlPlaneService) -> dict[str, object]:
    await service.mark_phase(job_id, "CUTOVER")
    return {"job_id": job_id, "status": "cutover_requested"}
