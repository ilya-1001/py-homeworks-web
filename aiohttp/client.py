import asyncio

import aiohttp


async def main():

    async with aiohttp.ClientSession() as session:

        # response = await session.get("http://127.0.0.1:8080/ads/3")
        # print(response.status)
        # print(await response.json())

        # response = await session.post(
        #     "http://127.0.0.1:8080/ads",
        #     json={"title": "ad_8", "description": "seller", "owner": "user"},
        # )
        # print(response.status)
        # print(await response.json())

        # response = await session.patch(
        #       "http://127.0.0.1:8080/ads/2",
        #       json={"title": "buy cur", "description": "no new", "owner": "user_15"},
        # )
        # print(response.status)
        # print(await response.json())

        # response = await session.get("http://127.0.0.1:8080/ads/1")
        # print(response.status)
        # print(await response.json())

        response = await session.delete("http://127.0.0.1:8080/ads/1")
        print(response.status)
        print(await response.json())

        response = await session.get("http://127.0.0.1:8080/ads/1")
        print(response.status)
        print(await response.json())


asyncio.run(main())