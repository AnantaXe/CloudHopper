from temporalio import activity

@activity.defn
async def start_cdc(request, plan) -> None:

    try:
        activity.logger.info("Starting CDC activity.")
        provider = get_cdc_provider(request.source.engine, request.target_service)
        activity.logger.info(f"Using provider: {provider.__class__.__name__} for source engine: {request.source.engine} and target service: {request.target_service}")
        await provider.prepare(request.source, request.target)
        activity.logger.info("Preparation for CDC completed. Starting the CDC process.")
        await provider.start()
        activity.logger.info("CDC process started. Monitoring progress until completion.")
    except Exception as e:
        activity.logger.error(f"Error during CDC: {e}")
        raise e

    return {
        "status": "running",
        "checkpoint": await provider.get_checkpoint(),
    }

async def get_cdc_provider(source_engine, target_service):

    pass