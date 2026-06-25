from shared.models.resources.base import Resource

class NetworkResource(Resource):
    
    cidr_block: str | None = None
    # vpc_id: str | None = None
    # subnet_id: str | None = None