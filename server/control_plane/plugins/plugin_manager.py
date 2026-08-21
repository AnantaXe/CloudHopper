from control_plane.plugins.registry import (
    PLUGIN_REGISTRY
)

class PluginManager:

    async def validate_plugin(
            self,
            provider: str
    ):
        plugin = PLUGIN_REGISTRY.get(provider)

        if not plugin:
            raise Exception("plugin not found")
        
        if plugin.signatures != "VALID":
            raise Exception("invalid plugin signature")
        
        if not plugin.sandboxed:
            raise Exception("sandbox policy violation")
        
        return plugin