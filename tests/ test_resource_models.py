from datetime import datetime

from shared.models.resources.server import (
    ServerResource
)


def test_server_resource():

    resource = ServerResource(
        resource_id="1",
        resource_type="VM",
        provider="AWS",
        name="server",
        region="us-east-1",
        discovered_at=datetime.utcnow()
    )

    assert resource.provider == "AWS"