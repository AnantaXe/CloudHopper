from __future__ import annotations

from typing import Any


class CDCEventProcessor:
    async def transform_event(self, raw_event: dict[str, Any]) -> dict[str, Any]:
        return {
            "transformed": True,
            "raw_event": raw_event,
        }

    async def validate_ordering(self, event: dict[str, Any]) -> bool:
        return True

    async def publish_to_target(self, event: dict[str, Any]) -> None:
        return None
