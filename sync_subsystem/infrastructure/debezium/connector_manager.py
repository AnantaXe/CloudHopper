from __future__ import annotations

from typing import Any


class CDCConnectorManager:
    def __init__(self, connect_url: str) -> None:
        self.connect_url = connect_url

    async def register_connector(self, connector_definition: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": "registered",
            "connector_name": connector_definition.get("name"),
        }

    async def deregister_connector(self, name: str) -> None:
        return None

    async def get_connector_status(self, name: str) -> dict[str, Any]:
        return {
            "name": name,
            "status": "running",
        }
