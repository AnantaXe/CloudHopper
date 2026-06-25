import pytest

from shared.models.discovery import DiscoveryRequest


@pytest.mark.asyncio
async def test_request():

    req = DiscoveryRequest(
        provider="aws"
    )

    assert req.provider == "aws"