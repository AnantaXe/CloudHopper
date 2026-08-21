import pytest

from agent_runtime.discovery.agent import (
    discovery_agent
)

@pytest.mark.asyncio
async def test_discovery_agent():

    result = await discovery_agent.ainvoke(
        {
            "provider": "aws",
            "token_id": "test_token_id",
            "plugin_validated": False,
            "resources": []
        }
    )

    assert len(result["resources"]) > 0