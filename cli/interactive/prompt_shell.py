import asyncio

from rich.console import Console
from rich.prompt import Prompt
from rich.live import Live

from cli.ui.live_console import (
    LiveDiscoveryView
)

from shared.events.event_bus import (
    subscribe
)

from agent_runtime.supervisor.intent_agent import (
    classify_intent
)

from control_plane.activities.discovery_activity import (
    run_discovery
)

console = Console()

# async def stream_events(view):

#     async for event in subscribe():

#         view.add_event(
#             event.agent,
#             event.message
#         )

def prompt():

    asyncio.run(
        run_prompt()
    )

async def run_prompt():

    goal = Prompt.ask(
        "[cyan]CloudHopper > [/cyan]"
    )

    intent = await classify_intent(
        goal
    )

    if intent["workflow"] != "DISCOVERY":

        console.print(
            "[red]Unsupported workflow[/red]"
        )

        return

    view = LiveDiscoveryView()

    # listener = asyncio.create_task(
    #     stream_events(view)
    # )

    with Live(
        view.render(),
        refresh_per_second=4
    ) as live:
        
        listener = asyncio.create_task(
            stream_events(view, live)
        )

        await run_discovery(
            intent["provider"]
        )

        await asyncio.sleep(2)

    listener.cancel()

async def stream_events(
    view,
    live
):

    async for event in subscribe():

        view.add_event(
            event.agent,
            event.message
        )

        live.update(
            view.render()
        )