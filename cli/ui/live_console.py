from rich.console import Console
from rich.live import Live
from rich.table import Table

console = Console()


class LiveDiscoveryView:

    def __init__(self):

        self.rows = []

    def add_event(
        self,
        agent,
        message
    ):

        self.rows.append(
            (agent, message)
        )

    def render(self):

        table = Table()

        table.add_column("Agent")
        table.add_column("Status")

        for agent, message in self.rows:

            table.add_row(
                agent,
                message
            )

        return table