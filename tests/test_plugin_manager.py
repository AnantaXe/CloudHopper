import pytest

from control_plane.plugins.plugin_manager import (
    PluginManager
)

@pytest.mark.asyncio
async def test_plugin():
    
    manager = PluginManager()
    
    plugin = await manager.validate_plugin(
        provider="aws"
    )

    assert plugin.name == "aws-discovery"