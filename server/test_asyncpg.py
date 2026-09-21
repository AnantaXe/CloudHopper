import asyncio
import asyncpg


async def main():
    print("Connecting to PostgreSQL...", flush=True)

    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="cloudhopper",
        password="password",
        database="cloudhopper",
    )

    print("Connected!", flush=True)

    result = await conn.fetchval("SELECT 1")

    print(f"Result: {result}", flush=True)

    await conn.close()

    print("Connection closed", flush=True)


asyncio.run(main())
