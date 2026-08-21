from shared.models.resources.base import Resource

class SecurityGroupResource(Resource):
    
    inbound_rules: list = []
    outbound_rules: list = []