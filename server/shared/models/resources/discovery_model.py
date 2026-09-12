from pydantic import BaseModel

from server.shared.models.resources.base import Resource

class DiscoveryResult(BaseModel):

    resources: list[Resource]