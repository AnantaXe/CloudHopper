from shared.models.resources.base import Resource

class ServerResource(Resource):
    
    cpu_count: int | None = None
    memory_gb: float | None = None
    operating_system: str | None = None
    ip_address: str | None = None