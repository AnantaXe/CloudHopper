"""Developer Notes: For production, rollback needs to account for writes made after cutover. 
You should therefore have a RollbackPlan generated during planning rather than treating rollback as a generic reverse operation."""

from temporalio import activity

@activity.defn
async def rollback(request, plan):

    source = get_source_provider(request)
    target = get_target_provider(request)

    # 1. Stop writes
    await target.freeze_writes(request.target)

    # Switch back application endpoints to source
    await switch_application_to_source(request)

    source_healthy = await source.health_check(request.source)

    if not source_healthy:
        raise Exception("Source database health check failed after rollback.")

    return {
        "status": "rolled_back",
    }


