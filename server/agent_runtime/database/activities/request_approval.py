from temporalio import activity

@activity.defn
async def request_migration_approval(request) -> None:


    try:
        activity.logger.info("Starting migration approval request activity.")
    except Exception as e:
        activity.logger.error(f"Error during migration approval request: {e}")
        raise e
    return {
        "status": "completed",
    }
