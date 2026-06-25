from control_plane.plugins.models import (
    PluginMetadata
)

PLUGIN_REGISTRY = {

    "aws": PluginMetadata(
        name="aws-discovery",
        version="1.0.0",
        signatures="VALID",
        permissions=[
            "ec2:Describe",
            "rds:Describe",
        ],
        sandboxed=True
    )
}