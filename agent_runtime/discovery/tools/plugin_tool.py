from control_plane.plugins.plugin_manager import (
    PluginManager
)

manager = PluginManager()

async def validate_plugin(
        provider: str
):
    
    """
    Validates the plugin for the given provider.
    """
    
    plugin = await manager.validate_plugin(provider)

    return plugin