from pydantic import BaseModel


class DiscoveryRequest(BaseModel):
    provider: str


class DiscoveryResponse(BaseModel):
    workflow_id: str
    status: str