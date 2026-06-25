from datetime import datetime
from pydantic import BaseModel

class Resource(BaseModel):
    
    resource_id: str
    resource_type: str
    provider: str
    name: str
    region: str | None = None
    discovered_at: datetime