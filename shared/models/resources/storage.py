from shared.models.resources.base import Resource

class StorageResource(Resource):
    
    storage_type: str | None = None
    capacity_gb: float | None = None
    encrypted: bool | None = None