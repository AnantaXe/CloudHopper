from pydantic import BaseModel

from shared.models.resources.base import Resource

class DiscoveryResult(BaseModel):

    resources: list[Resource]