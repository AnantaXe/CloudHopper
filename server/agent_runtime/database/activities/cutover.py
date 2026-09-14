from temporalio import activity

@activity.defn
async def cutover(request, plan):

    source = get_source_provider(request)
    target = get_target_provider(request)

    # 1. Stop writes
    await source.freeze_writes(request.source)

    # 2. Wait for CDC to Drain
    cdc_provider = get_cdc_provider(request.source.engine, request.target_service)

    while True:
        lag = await cdc_provider.get_lag()
        if lag <= 0:
            break
        await activity.sleep(5)

    # 3. Final Validation
    result = await validate_final_state(request)

    if not result.passed:
        raise Exception("Final validation failed. Cutover cannot proceed.")

    # 4. Switch application endpoints
    await switch_database_endpoints(request)

    # 5. Target Health Check
    target_healthy = await target.health_check(request.target)

    if not target_healthy:
        raise Exception("Target database health check failed after cutover.")

    return {
        "status": "completed",
    }