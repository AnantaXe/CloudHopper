from temporalio import activity

@activity.defn
async def start_cdc(request, plan) -> None:

    provider = get_cdc_provider(request.source.engine, request.target_service)

    await provider.prepare(request.source, request.target)

    await provider.start()

    return {
        "status": "running",
        "checkpoint": await provider.get_checkpoint(),
    }