import asyncio
from aiohttp import ClientSession
from json import loads
from main import get_permutations
import time
from os import environ

environ["GEVENT_SUPPORT"] = "True"
environ["PYDEVD_USE_FRAME_EVAL"] = "NO"

from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)


async def hello(url, i):
    async with ClientSession() as session:
        async with session.post(url, data={"q": i},timeout=30) as response:
            # await asyncio.sleep(0.1)
            response = await response.read()
            print(loads(response)["query"])

loop = asyncio.get_event_loop()

tasks = []
url = "https://allo.ua/ua/catalogsearch/ajax/suggest/?currentTheme=main&currentLocale=uk_UA"
perms = get_permutations()
for i, perm in enumerate(perms):
    task = asyncio.ensure_future(hello(url, perm))
    tasks.append(task)
    # if i%10 == 0:
    #     time.sleep(1)
loop.run_until_complete(asyncio.wait(tasks))