import asyncio
import requests

from requests import adapters
from functools import partial
from pyppeteer import launch
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor


class AsyncSession(requests.Session):
    def __init__(self, loop=None, workers=1):
        super(AsyncSession, self).__init__()

        adapter = adapters.HTTPAdapter(
            # The number of urllib3 connection pools to cache.
            pool_connections=workers,
            # The maximum number of connections to save in the pool (Set by
            # user)
            pool_maxsize=workers,
            pool_block=True,  # Block number of connections
        )

        self.mount("http://", adapter)
        self.mount("https://", adapter)
        self.loop = loop or asyncio.get_event_loop()
        self.thread_pool = ThreadPoolExecutor(max_workers=workers)

    async def request(self, *args, **kwargs):
        """Send request to the concurrent executor.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.thread_pool, partial(super().request, *args, **kwargs)
        )

class Response:
    pass

class Browser:
    def __init__(
        self,
        scope: str = "",
        loop=None,
        workers: int = 5, 
        from_json: dict = None
    ):
        self.set_scope(scope)
        self.session = AsyncSession(loop=loop, workers=workers)
        self.history = []


    def set_scope(self, url):
        """Correct and set the scope.

        Parameter:
            url: target base url
        """
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"
        if url.endswith("/"):
            url = url[:-1]
        self.scope = url

    async def request(self, method, url: str, *args, **kwargs):
        parsed_url = urlparse(url)
        
        if not parsed_url.host:
            if self.scope:
                url = urljoin(self.scope, parsed_url.path)
            if not self.scope:
                raise Exception(
                    "Cannot resolve local url if the scope has not been defined."
                )
                
        return await self.session.request(method, url, *args, **kwargs)

    async def requests(self, method: str, urls: list, *args, **kwargs):
        futures = [
            asyncio.create_task(self.request(method, url, *args, **kwargs))
            for url in urls
        ]
        return [
            await future
            for future in asyncio.as_completed(futures)
        ]

    def get(self, url: str, *args, **kwargs):
        return self.request("GET", url, *args, **kwargs)

    def gets(self, urls: list, *args, **kwargs):
        return self.requests("GET", urls, *args, **kwargs)

    async def post(self, url: str, *args, **kwargs):
        return await self.request("POST", url, *args, **kwargs)

    async def posts(self, urls: list, *args, **kwargs):
        return await self.requests("GET", urls, *args, **kwargs)

    async def head(self, url: str, *args, **kwargs):
        return await self.request("HEAD", url, *args, **kwargs)

    async def head(self, urls: list, *args, **kwargs):
        return await self.requests("HEAD", urls, *args, **kwargs)

    async def posts(self, urls: list):
        responses = []
        return responses

    def goto(self, url):
        """
        """
        pass

    def prev(self):
        """Go on previous page
        """
        pass

    def next(self):
        """Go on next page
        """
        pass

    def goparent(self):
        """Go back in web tree
        """
        pass

    async def crawl(self):
        pass

    def save(self, output: str = ""):
        pass

    async def close(self):
        self.session.close()
