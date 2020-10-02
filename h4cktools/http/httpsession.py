import asyncio
import time
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor

from .asyncsession import AsyncSession
from .httpresponse import HTTPResponse

USERAGENT = (
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) "
    "Gecko/20100101 Firefox/78.0"
)


class LocalPathException(Exception):
    """Raised when path is local and host is not defined"""
    pass


class HTTPSession(AsyncSession):
    """Psoeudo browser to make requests easier and faster.
    """
    def __init__(
        self,
        host: str = "",
        agent: str = USERAGENT,
        loop=None,
        workers: int = 5,
        verify: bool = False,
        delay: int = 0
    ):
        super(HTTPSession, self).__init__(loop=loop, workers=workers)
        self.hist = []
        self.page = None
        self.page_index = 0
        self.agent = USERAGENT
        self.host = host
        self.verify = verify
        self.delay = delay


    @property
    def agent(self) -> str:
        """User-Agent property
        """
        return self.headers["User-Agent"]


    @agent.setter
    def agent(self, user_agent: str):
        self.headers["User-Agent"] = user_agent


    @property
    def host(self) -> str:
        """Host property
        """
        return self._host


    @host.setter
    def host(self, url: str):
        parsed = urlparse(url)
        self._host = "://".join([parsed.scheme or "http", parsed.netloc or url])


    @host.deleter
    def host(self):
        self._host = ""


    @property
    def workers(self) -> int:
        return self.thread_pool


    @workers.setter
    def workers(self, max_workers: int):
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)


    def request(self, method: str, url: str, redirects=False, **kwargs):
        parsed = urlparse(url)

        if not parsed.netloc:
            if self.host:
                url = urljoin(self.host, parsed.path)
            if not self.host:
                raise LocalPathException

        del kwargs["allow_redirects"]
        return super().request(method, url, allow_redirects=redirects, **kwargs)
    

    def run(self, *coros):
        """
        """
        responses = super().run(*coros)
        if len(responses) == 1:
            return HTTPResponse(responses[0])
        return [HTTPResponse(response) for response in responses]


    def goto(self, url: str):
        """Go to new url and set it as new host

        Args:
            url (str): 
        Returns:
            HTTPResponse: 
        """
        self.page = self.run(self.get(url, allow_redirects=False))[0]
        self.hist.append(self.page)
        self.page_index = len(self.hist) - 1
        self.host = (self.page.host)
        return self.page

    def follow(self):
        """Follow redirection
        """
        if "Location" in self.page.headers.keys():
            return self.goto(self.page.headers.get("Location"))

    def prev(self):
        """Go on previous page
        """
        if self.page_index > 0:
            self.page_index -= 1
            self.page = self.sendall(
                self.get(self.hist[self.page_index].url, allow_redirects=False)
            )[0]
        return self.page

    def next(self):
        """Go on next page
        """
        if self.page_index < len(self.hist) - 1:
            self.page_index += 1
            self.page = self.sendall(
                self.get(self.hist[self.page_index].url, allow_redirects=False)
            )[0]
        return self.page

    def goin(self, sub_path: str):
        """Go in child local path
        """
        if sub_path.startswith("/"):
            sub_path = sub_path[1:]
        return self.goto("/".join([self.page.path, sub_path]))

    def goout(self):
        """Go in parent path
        """
        return self.goto("/".join(self.page.path.split("/")[:-1]))
