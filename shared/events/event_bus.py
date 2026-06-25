import asyncio

event_queue = asyncio.Queue()


# async def publish(event):

#     await event_queue.put(event)

async def publish(event):

    print("PUBLISH:", event)

    await event_queue.put(event)

async def subscribe():

    while True:

        event = await event_queue.get()

        print("RECEIVED:", event)

        yield event