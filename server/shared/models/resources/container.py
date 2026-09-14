from shared.models.resources.base import Resource

class ContainerResource(Resource):
    
    image: str | None = None
    cpu_count: int | None = None
    memory_gb: float | None = None
    environment_variables: dict | None = None