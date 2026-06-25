from rich.console import Console
from rich.status import Status

console = Console()

class Animation:

    @staticmethod
    def thinking(text: str):

        return console.status(
            f"[cyan]{text}[/cyan]"
        )