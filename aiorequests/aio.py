import asyncio
import requests
from requests import adapters
from functools import partial
from concurrent.futures import ThreadPoolExecutor


class Session(requests.Session):
    """Allow user to use request.Session with the asyncio lib 
    """

    def __init__(self, workers=1):
        super(Session, self).__init__()

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
        self.executor = ThreadPoolExecutor(max_workers=workers)

    async def request(self, *args, **kwargs):
        """Send request to the concurrent executor.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.executor, partial(super().request, *args, **kwargs)
        )
