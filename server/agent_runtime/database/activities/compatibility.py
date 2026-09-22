from temporalio import activity

@activity.defn
async def compatibility(request) -> None:


    try:
        activity.logger.info("Starting compatibility activity.")
    except Exception as e:
        activity.logger.error(f"Error during compatibility check: {e}")
        raise e
    # return {
    #     "status": "completed",
    # }
