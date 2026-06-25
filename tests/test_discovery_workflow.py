import pytest

from control_plane.activities.discovery_activity import (
    run_discovery
)

@pytest.mark.asyncio
async def test_discovery_activity():
    
    result = await run_discovery(
        provider="aws"
    )

# return [
#             ServerResource(
#                 resource_id="aws-server-1",
#                 resource_type="server",
#                 provider="aws",
#                 name="AWS Server 1",
#                 region="us-east-1",
#                 discovered_at=datetime.utcnow(),
#                 cpu_count=4,
#                 memory_gb=16.0,
#             ),

#             DatabaseResource(
#                 resource_id="aws-db-1",
#                 resource_type="database",
#                 provider="aws",
#                 name="AWS Database 1",
#                 region="us-east-1",
#                 discovered_at=datetime.utcnow(),
#                 engine="PostgreSQL",
#                 version="13.3",
#                 endpoint="aws-db-1.cleardb.com:5432"
#             )
#         ]

    print(result)
    # assert result["resources"] == [
    #     {
    #         "resource_id": "aws-server-1",
    #         "resource_type": "server",
    #         "provider": "aws",
    #         "name": "AWS Server 1",
    #         "region": "us-east-1",
    #         "cpu_count": 4,
    #         "memory_gb": 16.0,
    #     },
    #     {
    #         "resource_id": "aws-db-1",
    #         "resource_type": "database",
    #         "provider": "aws",
    #         "name": "AWS Database 1",
    #         "region": "us-east-1",
    #         "engine": "PostgreSQL",
    #         "version": "13.3",
    #         "endpoint": "aws-db-1.cleardb.com:5432"
    #     }
    # ]