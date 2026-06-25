import httpx

from shared.models.discovery import DiscoveryRequest


class LCIClient:

    BASE_URL = "http://localhost:8000"

    async def start_discovery(
        self,
        request: DiscoveryRequest
    ):

        async with httpx.AsyncClient() as client:

            response = await client.post(
                f"{self.BASE_URL}/discover",
                json=request.model_dump()
            )

            return response.json()