from datetime import datetime

from shared.models.resources.server import ServerResource
from shared.models.resources.database import DatabaseResource

class AWSDiscoveryPlugin:

    async def discover(
            self,
            token_id: str,
    ):
        return [
            ServerResource(
                resource_id="aws-server-1",
                resource_type="server",
                provider="aws",
                name="AWS Server 1",
                region="us-east-1",
                discovered_at=datetime.utcnow(),
                cpu_count=4,
                memory_gb=16.0,
            ),

            DatabaseResource(
                resource_id="aws-db-1",
                resource_type="database",
                provider="aws",
                name="AWS Database 1",
                region="us-east-1",
                discovered_at=datetime.utcnow(),
                engine="PostgreSQL",
                version="13.3",
                endpoint="aws-db-1.cleardb.com:5432"
            )
        ]