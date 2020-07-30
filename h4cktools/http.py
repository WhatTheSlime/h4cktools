import asyncio
import requests
from lxml import html
from requests import adapters
from functools import partial
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from os.path import join as path_join

from typing import TypeVar

HTTP_METHODS = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    "PATCH"
]

USERAGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"

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

    def _request(self, *args, **kwargs):
        return Page(super(AsyncSession, self).request(*args, **kwargs))

    def request(self, *args, **kwargs):
        """Send request to the concurrent executor.
        """
        func = partial(self._request, *args, **kwargs)
        return self.loop.run_in_executor(self.thread_pool, func)

    def run(self, *coros):
        """ Pass in all the coroutines you want to run, it will wrap each one
            in a task, run it and wait for the result. Return a list with all
            results, this is returned in the same order coros are passed in. """
        done, _ = self.loop.run_until_complete(asyncio.wait(coros))
        return [t.result() for t in done]


class HTTPSession:
    def __init__(
        self,
        host: str = "",
        loop=None,
        workers: int = 5,
        verify: bool = False,
    ):
        self._session = AsyncSession(loop=loop, workers=workers)
        self._session.verify = verify
        self.host = host
        self.agent = USERAGENT
        self.hist = []
        self.page = None
        self.page_index = 0

    def __getattr__(self, attr):
        orig_attr = getattr(self._session, attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                # prevent wrapped object from becoming unwrapped
                if result == self._session:
                    return self
                return result
            return hooked
        else:
            return orig_attr

    def __setattr__(self, name, value):
        if name == "agent" and isinstance(value, str):
            self._session.headers["User-Agent"] = value
        elif name == "proxy" and isinstance(value, str):
            if value:
                parsed = urlparse(value)
                proxy = "://".join([parsed.scheme, parsed.netloc])
                self._session.proxies = {
                    "http": proxy,
                    "https": proxy
                }
            else:
                self._session.proxies = {}
        elif name == "workers":
            self._session.thread_pool = ThreadPoolExecutor(max_workers=value)
        elif name == "headers":
            pass
        elif name == "host":
            self.__dict__[name] = self._parse_host(value)
        else:
            self.__dict__[name] = value

    def _parse_host(self, url):
        """Correct and set the host.

        Parameter:
            url: target base url
        """
        parsed = urlparse(url)

        return "://".join([parsed.scheme or "http", parsed.netloc])

    # Requests
    def request(self, method: str, url: str, *args, **kwargs):
        parsed = urlparse(url)

        if not parsed.netloc:
            if self.host:
                url = urljoin(self.host, parsed.path)
            if not self.host:
                raise Exception(
                    "Cannot resolve local url if the host "
                    "has not been defined."
                )
        return self._session.request(method, url, *args, **kwargs)

    '''
    def strrequest(self, string: str, *args, **kwargs):
        """Create requests from full string requests
        """
        delimiter = "\n\n\n\n"

        if delimiter in string:


        headers = []

        headers, content = string.split("\n\n\n\n", 1)
        return  
    '''

    def get(self, url: str, *args, **kwargs):
        return self.request("GET", url, *args, **kwargs)


    def post(self, url: str, *args, **kwargs):
        """
        """
        return self.request("POST", url, *args, **kwargs)


    def head(self, url: str, *args, **kwargs):
        """
        """
        return self.request("HEAD", url, *args, **kwargs)


    def sendall(self, *coros):
        """
        """
        results = self._session.run(*coros)
        return results

    # Navigation
    def goto(self, url: str):
        """Go to new url and set it as new host
        """
        return self.sendall(self._goto(url))[0]


    async def _goto(self, url: str):
        """
        Args:

        Returns:
            Page: reached page
        """
        self.page = await self.get(url, allow_redirects=False)
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
                self.get(self.hist[self.page_index].url), allow_redirects=False
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
        return self.goto(path_join(self.page.path, sub_path))

    def goout(self):
        """Go in parent path
        """
        return self.goto("/".join(self.page.path.split("/")[:-1]))

    def crawl(
        self, 
        local_path: str = "/", 
        status_codes: list = [200], 
        include: list = [], 
        exclude: list = [],
        render=False
    ):
        pass

    def save(self, output_dir: str = ".", filename: str = "h4ckbrowser"):
        timestamp = datetime.timestamp(datetime.now())
        filename = "".join(["h4ckbrowser_", timestamp, ".pkl"])
        path = os.path.join(output_dir, filename)

        with open(path, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    async def http_methods(self):
        methods = {}
        
        futures = [
            asyncio.create_task(
                self.request(method, self.page.path, allow_redirects=False)
            ) 
            for method in HTTP_METHODS
        ]

        for i, future in enumerate(asyncio.as_completed(futures)):
            p = await future
            methods[p.response.request.method] = p.code

        return to_str(methods)

    def close(self):
        self._session.close()

class Page:
    """The class is a wrapper for requests.models.Response class.
    It implements helpful methods to analyse http(s) response.
    """
    def __init__(self, response):
        self._response = response
        parsed = urlparse(response.url)
        self.host = "://".join([parsed.scheme, parsed.netloc])
        self.path = parsed.path
        self.code = response.status_code
        self.isok = (self.code == 200)
        self.isforbidden = (self.code == 403)
        self.exists = self._exists()
        self.links = self._find_links()
        self.srcs = self._find_sources()
        self.paths = self._find_paths()

    def __getattr__(self, attr):
        orig_attr = getattr(self._response, attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                # prevent wrapped object from becoming unwrapped
                if result == self._response:
                    return self
                return result
            return hooked
        else:
            return orig_attr

    # Searching Methods
    def search(self, regex):
        """Use regular expression to search expression in the response content.
        regex: regular(s) expression to use. 
        """
        if isinstance(regex, str):
            return re.search(regex, self._response.text)
        elif isinstance(regex, tuple):
            for r in regex:
                match = re.search(r, self._response.text)
                if match:
                    return match


    def findall(self, regex):
        """Use regular expression to find all match of an expression in the 
        response content.
        regex: regular expression to use.
        """
        return re.findall(regex, self._response.text)


    def tag(self, *args, **kwargs):
        """Return http response searched tags.
        tag: tag name to find.
        """
        soup = BeautifulSoup(self._response.text, "lxml")
        return soup.find(*args, **kwargs)


    def tags(self, *args, **kwargs):
        """Return http response searched tags
        Args:
            BeautifulSoup.findall args
        """
        soup = BeautifulSoup(self._response.text, "lxml")
        return soup.findAll(*args, **kwargs)


    def xml(self):
        """Converts response into an XML object
        """
        if not isinstance(self._response, bytes) and self._response.content:
            return html.fromstring(self._response.text)
        return html.HtmlElement()


    def scripts(self):
        """Return all src values of scripts in content page
        """
        soup = BeautifulSoup(self._response.text, "lxml")
        scripts = [script.prettify() for script in soup.findAll("script")]
        return scripts


    def images(self):
        """Return all src values of img in centent page
        """
        return self.xml().xpath("//img/@src")


    def _find_sources(self):
        """Return all src values of scripts in content page
        """
        return [str(src) for src in self.xml().xpath("//script/@src")]


    def _find_links(self):
        """Return all href values links in content page.
        """
        return self.xml().xpath("//a/@href")


    def _find_paths(self):
        paths = set()
        hostname = urlparse(self.url).netloc

        for link in self.links:
            parsed = urlparse(link)
            if parsed.path and (parsed.netloc == hostname or not parsed.netloc):
                paths.add(parsed.path)
        return list(paths)


    def _exists(self):
        """Return True if the requested url exists but not necessarily 
        accessible, False otherwise.
        """
        url = self._response.url
        location = ""
        if self.is_redirect:
            location = self._response.headers.get("Location", None)
            if location:
                location = urlparse(location).path
                url = urlparse(url).path
        return self.code in (200, 401, 403) or location == "".join((url, "/"))


    def __repr__(self):
        return f"<[{self.code}] {self.url}>"