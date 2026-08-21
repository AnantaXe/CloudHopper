from temporalio import activity

from agent_runtime.supervisor.agent import (
    supervisor_agent
)

from agent_runtime.dispatcher.dispatcher import (
    dispatch
)

from shared.events.models import AgentEvent
from shared.events.event_bus import publish


@activity.defn
async def run_discovery(
    provider: str
):
    
    await publish(
        AgentEvent(
            agent="supervisor",
            event_type="STARTED",
            message="Creating discovery plan"
        )
    )

    plan_result = await supervisor_agent.ainvoke(
        {
            "provider": provider,
            "goal": f"Discover {provider}",
            "plan": [],
            "resources": []
        }
    )   

    # print(type(plan_result))
    # print(plan_result)

    resources = await dispatch(
        provider=provider,
        tasks=plan_result["plan"]
    )
    
    await publish(
        AgentEvent(
            agent="supervisor",
            event_type="PLAN_CREATED",
            message=f"{len(plan_result['plan'])} tasks generated"
        )
    )

    return {
        "plan": plan_result["plan"],
        "resources": resources
    }