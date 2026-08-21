from control_plane.security.token_broker import (
    TokenBroker,
)

broker = TokenBroker()

async def issue_token(
        provider: str,
):
    
    """Issues a token for the given provider."""
    
    token = await broker.issue_token(provider)

    return token