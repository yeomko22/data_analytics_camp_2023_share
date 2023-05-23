import asyncio
import random


async def remote_request():
    await asyncio.sleep(1)
    return random.randint(0, 10)


async def main():
    result = await asyncio.gather(*[remote_request() for x in range(10)])
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
