from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .dependencies import (
    sync_control_plane_service,
    validation_service,
    reconciliation_service,
    decision_engine,
)
from .schemas import (
    ValidationPayload,
    ReconciliationPayload,
    RecoveryPayload,
    AgentDecisionPayload,
)
from ..domain.models import SyncJobMetadata

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/jobs", response_model=SyncJobMetadata)
async def create_sync_job(job: SyncJobMetadata) -> SyncJobMetadata:
    return await sync_control_plane_service.create_job(job)


@router.get("/jobs/{job_id}", response_model=SyncJobMetadata)
async def get_sync_job(job_id: str) -> SyncJobMetadata:
    job = await sync_control_plane_service.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Sync job not found")
    return job


@router.post("/jobs/{job_id}/cutover")
async def request_cutover(job_id: str) -> dict[str, object]:
    await sync_control_plane_service.mark_phase(job_id, "CUTOVER")
    return {"job_id": job_id, "status": "cutover_requested"}


@router.post("/jobs/{job_id}/validate")
async def validate_sync_job(job_id: str, payload: ValidationPayload) -> dict[str, object]:
    result = await validation_service.validate_row_counts(job_id, payload.source_rows, payload.target_rows)
    if payload.source_checksum is not None and payload.target_checksum is not None:
        checksum_result = await validation_service.validate_checksums(job_id, payload.source_checksum, payload.target_checksum)
        result.update(checksum_result)
    if payload.drift_score is not None:
        result["drift_score"] = payload.drift_score
    if payload.sample_mismatch_count is not None:
        result["sample_mismatch_count"] = payload.sample_mismatch_count
    plan = await decision_engine.plan_validation(job_id, result)
    return {"job_id": job_id, "validation": result, "plan": plan}


@router.get("/jobs/{job_id}/validation")
async def get_validation(job_id: str) -> dict[str, object]:
    result = await sync_control_plane_service.get_validation_result(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Validation result not found")
    return result


@router.post("/jobs/{job_id}/reconcile")
async def reconcile_sync_job(job_id: str, payload: ReconciliationPayload) -> dict[str, object]:
    report = {}
    if payload.source_count is not None and payload.target_count is not None:
        report["row_count"] = await reconciliation_service.reconcile_row_counts(job_id, payload.source_count, payload.target_count)
    if payload.source_checksum is not None and payload.target_checksum is not None:
        report["checksum"] = await reconciliation_service.reconcile_checksums(job_id, payload.source_checksum, payload.target_checksum)
    if payload.drift_score is not None and payload.drift_threshold is not None:
        report["drift"] = await reconciliation_service.reconcile_drift(job_id, payload.drift_score, payload.drift_threshold)
    return {"job_id": job_id, "reports": report}


@router.get("/jobs/{job_id}/reconciliation")
async def get_reconciliation(job_id: str) -> dict[str, object]:
    reports = await sync_control_plane_service.get_reconciliation_reports(job_id)
    return {"job_id": job_id, "reports": reports}


@router.post("/jobs/{job_id}/recover")
async def recover_sync_job(job_id: str, payload: RecoveryPayload) -> dict[str, object]:
    plan = await decision_engine.plan_recovery(job_id, payload.dict())
    return {"job_id": job_id, "recovery_plan": plan}


@router.post("/jobs/{job_id}/agents/{agent_name}/decision")
async def get_agent_decision(job_id: str, agent_name: str, payload: AgentDecisionPayload) -> dict[str, object]:
    if agent_name == "sync_planning":
        plan = await decision_engine.plan_sync({"job_id": job_id, **payload.context})
    elif agent_name == "validation":
        plan = await decision_engine.plan_validation(job_id, payload.context)
    elif agent_name == "conflict_resolution":
        plan = await decision_engine.plan_conflict_resolution(job_id, payload.context)
    elif agent_name == "recovery":
        plan = await decision_engine.plan_recovery(job_id, payload.context)
    else:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"job_id": job_id, "agent": agent_name, "plan": plan}
