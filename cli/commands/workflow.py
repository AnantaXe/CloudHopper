import asyncio

import httpx

from rich.console import Console

console = Console()


def status(
    workflow_id: str
):

    asyncio.run(
        get_status(workflow_id)
    )


async def get_status(
    workflow_id: str
):

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"http://localhost:8000/workflows/{workflow_id}"
        )

        console.print(
            f"[green]Workflow :[/green] {response.json()}"
        )