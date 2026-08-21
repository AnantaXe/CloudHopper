from temporalio.client import Client


class TemporalClient:

    _client = None

    @classmethod
    async def get_client(cls):

        if cls._client is None:

            cls._client = await Client.connect(
                "localhost:7233"
            )

        return cls._client