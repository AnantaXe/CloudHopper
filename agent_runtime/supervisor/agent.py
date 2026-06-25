import json

from langgraph.graph import (
    StateGraph,
    END
)

from agent_runtime.supervisor.state import (
    SupervisorState
)

from agent_runtime.supervisor.prompts import (
    DISCOVERY_PLANNER_PROMPT
)

from shared.llm.factory import (
    get_llm
)


async def planning_node(
    state: SupervisorState
):

    llm = get_llm("ollama")

    response = await llm.ainvoke(
        f"""
        {DISCOVERY_PLANNER_PROMPT}

        Goal:
        {state['goal']}
        """
    )

    content = response.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "", 1)

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()
    plan = json.loads(content)

    state["plan"] = plan["tasks"]

    return state

graph = StateGraph(
    SupervisorState
)

graph.add_node(
    "planning",
    planning_node
)

graph.set_entry_point(
    "planning"
)

graph.add_edge(
    "planning",
    END
)

supervisor_agent = graph.compile()