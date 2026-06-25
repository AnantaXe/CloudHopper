from shared.events.event_bus import publish
from shared.events.models import AgentEvent

from providers.aws.discovery_plugin import (
    AWSDiscoveryPlugin
)

async def run_compute_discovery(
    provider: str
):
    
    await publish(
        AgentEvent(
            agent="compute",
            event_type="STARTED",
            message="Scanning EC2 instances"
        )
    )

    if provider != "aws":
        return []
    
    plugin = AWSDiscoveryPlugin()

    resources = await plugin.discover("temp-token")

    await publish(
        AgentEvent(
            agent="compute",
            event_type="COMPLETED",
            message=f"{len(resources)} resources found"
        )
    )

    return [

        resource

        for resource in resources

        if resource.resource_type == "VM"
    ]