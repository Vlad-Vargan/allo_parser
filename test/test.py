import asyncio
from aiohttp import ClientSession
from main import get_permutations
from json import loads, dumps

async def fetch(url, session, perm):
    async with session.post(url, data={"q":perm},timeout=30) as response:
        print(dumps(response.read())["query"])
        return await response.read()


async def bound_fetch(sem, url, session, perm):
    # Getter function with semaphore.
    async with sem:
        await asyncio.sleep(0.1)
        await fetch(url, session, perm)


async def run():
    url = "https://allo.ua/ua/catalogsearch/ajax/suggest/?currentTheme=main&currentLocale=uk_UA"
    perms = get_permutations()
    # create instance of Semaphore
    sem = asyncio.Semaphore(1)

    tasks = []
    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for perm in perms:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session, perm))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run())
loop.run_until_complete(future)