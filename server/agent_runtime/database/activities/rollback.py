"""Developer Notes: For production, rollback needs to account for writes made after cutover. 
You should therefore have a RollbackPlan generated during planning rather than treating rollback as a generic reverse operation."""

from temporalio import activity

@activity.defn
async def rollback(request):

    activity.logger.info("Starting rollback activity.")
    source = get_source_provider(request)
    target = get_target_provider(request)

    # 1. Stop writes
    await target.freeze_writes(request.target)
    activity.logger.info("Writes to the target database have been frozen.")
    # Switch back application endpoints to source
    await switch_application_to_source(request)
    activity.logger.info("Application endpoints have been switched back to the source database.")

    source_healthy = await source.health_check(request.source)
    activity.logger.info("Source database health check completed.")

    if not source_healthy:
        raise Exception("Source database health check failed after rollback.")

    # return {
    #     "status": "rolled_back",
    # }


async def get_source_provider(request):
    # Logic to determine and return the source provider based on the request
    pass

async def get_target_provider(request):
    # Logic to determine and return the target provider based on the request
    pass

async def switch_application_to_source(request):
    # Logic to switch application endpoints back to the source database
    pass