import asyncio

from agent_runtime.database.domain.model import DatabaseEndpoint
from providers.database.postgresql.connector import PostgreSQLProvider


async def main():
    endpoint = DatabaseEndpoint(
        engine="postgresql",
        version="16",
        host="localhost",
        port=5432,
        username="cloudhopper",
        password="password",
        database_name="cloudhopper",
        provider="local",
        service_name="postgresql",
    )

    provider = PostgreSQLProvider()

    print("Starting provider assessment...", flush=True)

    result = await provider.assess_database(endpoint)

    print("Assessment completed:", result, flush=True)


asyncio.run(main())