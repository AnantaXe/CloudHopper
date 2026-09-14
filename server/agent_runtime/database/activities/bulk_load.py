from temporalio import activity

@activity.defn
async def initial_bulk_load(request, plan) -> None:

    provider = get_bulk_load_provider(request.source.engine, request.target_service)

    await provider.prepare(request.source, request.target)

    await provider.start(request.source, request.target)

    await provider.wait_until_complete()

    return {
        "status": "completed",
    }

def get_bulk_load_provider(source_engine, target_service):

    pass