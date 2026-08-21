# from agent_runtime.supervisor.agent import (
#     graph
# )
from shared.llm.factory import get_llm

class Planner:

    async def create_plan(
        self,
        goal: str
    ):

        llm = get_llm("ollama")

        response = await llm.ainvoke(
            goal
        )

        return response.content