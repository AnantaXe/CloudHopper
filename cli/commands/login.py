import asyncio
import httpx
from rich.console import Console
import typer

console = Console()

def login(
    username: str,
    password: str
):
    if not username or not password:
        username = typer.prompt("Enter your username : ")
        password = typer.prompt("Enter your password : ", hide_input=True)

    perform_login(username, password)

def perform_login(
    username: str,
    password: str
):

    async def login_request():
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/auth/login",
                json={"username": username, "password": password}
            )
            return response

    response = asyncio.run(login_request())

    if response.status_code == 200:
        console.print("[green]Login successful![/green]")
    else:
        console.print(f"[red]Login failed: {response.text}[/red]")
        console.print(f"Signup using [bold]cloudhopper signup[/bold] command if you don't have an account.")