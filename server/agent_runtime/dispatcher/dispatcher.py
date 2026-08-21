from agent_runtime.compute.agent import (
    run_compute_discovery
)

from agent_runtime.network.agent import (
    run_network_discovery
)

from agent_runtime.storage.agent import (
    run_storage_discovery
)

from agent_runtime.database.agent import (
    run_database_discovery
)

from agent_runtime.security.agent import (
    run_security_discovery
)


TASK_MAP = {
    "discover_compute": run_compute_discovery,
    "discover_network": run_network_discovery,
    "discover_storage": run_storage_discovery,
    "discover_databases": run_database_discovery,
    "discover_security": run_security_discovery,
}


async def dispatch(
    provider: str,
    tasks: list[str]
):

    discovered_resources = []

    for task in tasks:

        fn = TASK_MAP.get(task)

        if not fn:
            continue

        result = await fn(
            provider
        )

        discovered_resources.extend(
            result
        )

    return discovered_resources