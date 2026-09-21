from temporalio import activity

@activity.defn
async def initial_bulk_load(request) -> None:


    try:
        activity.logger.info("Starting initial bulk load activity.")
        provider = get_bulk_load_provider(request.source.engine, request.target_service)
        activity.logger.info(f"Using provider: {provider.__class__.__name__} for source engine: {request.source.engine} and target service: {request.target_service}")
        await provider.prepare(request.source, request.target)
        activity.logger.info("Preparation for bulk load completed. Starting the bulk load process.")
        await provider.start(request.source, request.target)
        activity.logger.info("Bulk load process started. Monitoring progress until completion.")
        await provider.wait_until_complete()
        activity.logger.info("Bulk load process completed successfully.")

    except Exception as e:
        activity.logger.error(f"Error during initial bulk load: {e}")
        raise e
    return {
        "status": "completed",
    }

def get_bulk_load_provider(source_engine, target_service):

    pass