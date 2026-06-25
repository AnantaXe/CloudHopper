from datetime import UTC, datetime
from datetime import timedelta

from uuid import uuid4

from control_plane.security.models import (
    TemporaryToken
)

from control_plane.security.exception import (
    TokenExpiredException,
)

datetime.now(UTC)

class TokenBroker:

    TOKEN_TTL_MINUTES = 5

    async def issue_token(
            self,
            provider: str
    ) -> TemporaryToken:
        
        return TemporaryToken(
            token_id=str(uuid4()),
            provider=provider,
            expires_at=datetime.now(UTC) + timedelta(minutes=self.TOKEN_TTL_MINUTES)
        )
    
    async def validate_token(
            self,
            token: TemporaryToken
    ):
        
        if datetime.now(UTC) > token.expires_at:
            raise TokenExpiredException("Token has expired")
        
        return True