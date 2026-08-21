from providers.aws.discovery_plugin import (
    AWSDiscoveryPlugin
)

async def discover_resources(
        provider: str,
        token_id: str
):
    
    """
    Discovers resources for the given provider using the discovery plugin.
    """
    
    if provider == "aws":
        plugin = AWSDiscoveryPlugin()
        resources = await plugin.discover(token_id)
        return resources
    else:
        raise Exception(f"Unsupported provider: {provider}")