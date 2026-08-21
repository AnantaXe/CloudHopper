from datetime import datetime
from pydantic import BaseModel

class TemporaryToken(BaseModel):
    token_id: str
    provider: str
    expires_at: datetime