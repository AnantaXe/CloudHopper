import pytest
from unittest.mock import AsyncMock, patch

from control_plane.services.workflow_service import (
    WorkflowService
)


@pytest.mark.asyncio
async def test_create_workflow():

    service = WorkflowService()

    result = await service.create_discovery_workflow(
        provider="aws"
    )

    assert result["status"] == "STARTED"