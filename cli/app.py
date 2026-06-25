import typer

from cli.commands.discovery import discover
from cli.commands.workflow import status
from cli.interactive.prompt_shell import prompt

app = typer.Typer()

app.command()(discover)
app.command()(status)
app.command()(prompt)


if __name__ == "__main__":
    app()