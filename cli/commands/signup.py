import asyncio
import httpx
from rich.console import Console
import typer

console = Console()

def signup(
    username: str,
    email: str,
    password: str
):
    if not username or not email or not password:
        username = typer.prompt("Enter your username : ")
        email = typer.prompt("Enter your email : ")
        password = typer.prompt("Enter your password : ", hide_input=True)

    perform_signup(username, email, password)

def perform_signup(
    username: str,
    email: str,
    password: str
):

    async def signup_request():
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/auth/register",
                json={"username": username, "email": email, "password": password}
            )
            return response

    response = asyncio.run(signup_request())

    if response.status_code == 200:
        console.print("[green]Signup successful![/green]")
    else:
        console.print(f"[red]Signup failed: {response.text}[/red]")