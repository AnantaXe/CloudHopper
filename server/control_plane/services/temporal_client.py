from temporalio.client import Client
from temporalio.contrib.pydantic import pydantic_data_converter

class TemporalClient:

    _client: Client | None = None

    @classmethod
    async def get_client(cls):
        if cls._client is None:
            cls._client = await Client.connect(
                "localhost:7233",
                data_converter=pydantic_data_converter,
            )
        return cls._client

    # @classmethod
    # async def execute_workflow(cls, workflow_class, *args, **kwargs):
    #     client = await cls.get_client()

    #     return await client.execute_workflow(
    #         workflow_class,
    #         *args,
    #         **kwargs
    #     )
    