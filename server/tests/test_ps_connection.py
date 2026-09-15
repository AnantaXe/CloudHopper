import asyncio
import asyncpg


async def main():
    print("Connecting...")

    conn = await asyncpg.connect(
        host="localhost",
        port=5434,
        user="changeit",
        password="changeitit",
        database="target_db",
        ssl=False,
        timeout=10,
    )

    print("Connected")

    result = await conn.fetchval("SELECT 1")

    print("Result:", result)

    await conn.close()
    print("Closed")


if __name__ == "__main__":
    asyncio.run(main())