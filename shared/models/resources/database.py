from shared.models.resources.base import Resource

class DatabaseResource(Resource):
    
    engine: str 
    version: str | None = None
    endpoint: str | None = None