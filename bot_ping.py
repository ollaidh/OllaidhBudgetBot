import os
import asyncio
import aiohttp


async def ping_bot_endpoint(bot_url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(bot_url) as resp:
                print(await resp.text())
    except:
        print("EXCEPTION")