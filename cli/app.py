from cli.commands.login import login
import typer

from cli.commands.discovery import discover
from cli.commands.signup import signup
from cli.commands.workflow import status
from cli.interactive.prompt_shell import prompt

app = typer.Typer()

app.command()(discover)
app.command()(status)
app.command()(prompt)
app.command()(login)
app.command()(signup)


if __name__ == "__main__":
    app()