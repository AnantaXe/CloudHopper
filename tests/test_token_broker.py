import pytest

from control_plane.security.token_broker import (
    TokenBroker
)

@pytest.mark.asyncio
async def test_issue_token():

    broker = TokenBroker()

    token = await broker.issue_token(
        provider="aws"
    )

    assert token.provider == "aws"