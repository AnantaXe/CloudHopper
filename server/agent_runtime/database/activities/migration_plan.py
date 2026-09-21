from temporalio import activity

@activity.defn
async def generate_mig_plan(request) -> None:


    try:
        activity.logger.info("Starting migration plan generation activity.")
    except Exception as e:
        activity.logger.error(f"Error during migration plan generation: {e}")
        raise e
    return {
        "status": "completed",
    }
