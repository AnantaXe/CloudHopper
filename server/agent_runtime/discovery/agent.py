from langgraph.graph import (
    StateGraph,
    END
)

from agent_runtime.discovery.state import (
    DiscoveryState
)

from agent_runtime.discovery.tools.token_tool import (
    issue_token
)

from agent_runtime.discovery.tools.plugin_tool import (
    validate_plugin
)

from agent_runtime.discovery.tools.discovery_tool import (
    discover_resources
)


"""
Node 1: Issue Token
"""

async def token_node(
        state: DiscoveryState
):
    token = await issue_token(
        state["provider"]
    )

    state["token_id"] = token.token_id

    return state


"""
Node 2: Validate Plugin
"""

async def plugin_node(
        state: DiscoveryState
):
    await validate_plugin(
        state["provider"]
    )

    state["plugin_validated"] = True

    return state


"""
Node 3: Discover Resources
"""

async def discovery_node(
        state: DiscoveryState
):
    result = await discover_resources(
        state["provider"],
        state["token_id"]
    )

    state["resources"] = result

    return state


graph = StateGraph(
    DiscoveryState,
)

graph.add_node(
    "token",
    token_node
)

graph.add_node(
    "plugin",
    plugin_node
)

graph.add_node(
    "discovery",
    discovery_node
)

graph.set_entry_point("token")

graph.add_edge("token", "plugin")

graph.add_edge("plugin", "discovery")

graph.add_edge("discovery", END)

discovery_agent = graph.compile()