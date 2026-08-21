# tests/test_supervisor.py

import pytest

from agent_runtime.supervisor.agent import (
    supervisor_agent
)


@pytest.mark.asyncio
async def test_supervisor():

    result = []
    async for event in supervisor_agent.astream_events(
        {
            "provider": "aws",
            "goal": "Discover AWS environment",
            "plan": [],
            "resources": []
        }
    ):
        if event["event"] == "on_plan_update":
            result = event["plan"]

    

    assert len(
        result
    ) > 0