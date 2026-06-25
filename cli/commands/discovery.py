import asyncio

from rich.console import Console

from shared.models.discovery import DiscoveryRequest
from cli.services.lci_client import LCIClient

console = Console()


def discover(provider: str):

    asyncio.run(
        run_discovery(provider)
    )


async def run_discovery(
    provider: str
):

    client = LCIClient()
    console.print(
        f"[blue]Starting discovery for provider:[/blue] {provider}"
    )

    result = await client.start_discovery(
        DiscoveryRequest(
            provider=provider
        )
    )

    console.print(
    f"[green]Plan:[/green]"
    )

    for task in result["plan"]:
        console.print(
            f" - {task}"
        )

    # console.print(
    #     f"[green]Workflow:[/green] {result['workflow_id']}"
    # )
    # console.print(
    #     f"[green]Status:[/green] {result['status']}"
    # )
    # console.print(
    #     f"[green]Workflow Type:[/green] {result['workflow_type']}"
    # )