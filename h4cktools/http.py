import asyncio
import requests
from lxml import html
from requests import adapters
from functools import partial
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from .display import to_str

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
        scope: str = "",
        loop=None,
        workers: int = 5, 
        from_json: dict = None,
        verify: bool = False,
    ):
        self.set_scope(scope)
        self.__session = AsyncSession(loop=loop, workers=workers)
        self.__session.verify = verify
        self.hist = []
        self.headers = self.session.headers
        self.page = None
        self.page_index = 0

    def set_scope(self, url):
        """Correct and set the scope.

        Parameter:
            url: target base url
        """
        parsed = urlparse(url)

        self.scope = "://".join([parsed.scheme or "http", parsed.netloc])

    def set_proxy(self, url: str):
        parsed = urlparse(url)
        proxy = "://".join([parsed.scheme, parsed.netloc])
        self.__session.proxies = {
            "http": proxy,
            "https": proxy
        }

    def unset_proxy(self):
        self.__session.proxies = {}

    def headers(self):
        return to_str(self.__session.headers)

    # Requests
    def request(self, method: str, url: str, *args, **kwargs):
        parsed = urlparse(url)

        if not parsed.netloc:
            if self.scope:
                url = urljoin(self.scope, parsed.path)
            if not self.scope:
                raise Exception(
                    "Cannot resolve local url if the scope "
                    "has not been defined."
                )
        return self.__session.request(method, url, *args, **kwargs)

    def get(self, url: str, *args, **kwargs):
        return self.request("GET", url, *args, **kwargs)

    def post(self, url: str, *args, **kwargs):
        return self.request("POST", url, *args, **kwargs)

    def head(self, url: str, *args, **kwargs):
        return self.request("HEAD", url, *args, **kwargs)

    def run(self, *coros):
        results = self.__session.run(*coros)

        return results

    # Navigation
    def goto(self, url: str):
        """Go to new url and set it as new scope
        """
        return self.run(self.__goto(url))

    async def __goto(self, url: str):
        self.page = await self.get(url, allow_redirects=False)
        self.hist.append(self.page)
        self.page_index = len(self.hist) - 1
        self.set_scope(self.page.host)
        self.headers = self.__session.headers
        return self.page

    def follow(self):
        """Follow redirection
        """
        if "Location" in self.page.response.headers.keys():
            return self.goto(self.page.response.headers.get("Location"))

    def prev(self):
        """Go on previous page
        """
        if self.page_index > 0:
            self.page_index -= 1
            self.page = self.run(self.get(self.hist[self.page_index].url))[0]
        return self.page

    def next(self):
        """Go on next page
        """
        if self.page_index < len(self.hist) - 1:
            self.page_index += 1
            self.page = self.run(self.get(self.hist[self.page_index].url))[0]
        return self.page

    def goin(self, sub_path: str):
        """Go in child local path
        """
        if sub_path.startswith("/"):
            sub_path = sub_path[1:]
        return self.goto(urljoin(self.page.path, sub_path))

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
        self.__session.close()

class Page:
    """The class is a wrapper for requests.models.Response class.
    It implements helpful methods to analyse http(s) response.
    """
    def __init__(self, response):
        self.response = response
        self.url = self.response.url
        parsed = urlparse(self.response.url)
        self.host = "://".join([parsed.scheme, parsed.netloc])
        self.path = parsed.path
        self.code = response.status_code
        self.is_ok = (self.code == 200)
        self.is_forbidden = (self.code == 403)
        self.exists = self.__exists()
        self.links = self.__find_links()
        self.srcs = self.__find_sources()
        self.paths = self.__find_paths()

    def __getattr__(self, attr):
        orig_attr = getattr(self.response, attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                # prevent wrapped response from becoming unwrapped
                if result == self.response:
                    return self
                return result
            return hooked
        else:
            return orig_attr

    def __exists(self):
        """Return True if the requested url exists but not necessarily 
        accessible, False otherwise.
        """
        url = self.response.url
        location = ""
        if self.is_redirect:
            location = self.response.headers.get("Location", None)
            if location:
                location = urlparse(location).path
                url = urlparse(url).path
        return self.response.status_code in (
            200,
            401,
            403,
        ) or location == "".join((url, "/"))

    # Searching Methods
    def search(self, regex):
        """Use regular expression to search expression in the response content.
        regex: regular(s) expression to use. 
        """
        if isinstance(regex, str):
            return re.search(regex, self.response.text)
        elif isinstance(regex, tuple):
            for r in regex:
                match = re.search(r, self.response.text)
                if match:
                    return match
    def findall(self, regex):
        """Use regular expression to find all match of an expression in the 
        response content.
        regex: regular expression to use.
        """
        return re.findall(regex, self.response.text)

    def extract_version(self):
        """Extract version number from a text string.
        """
        # Remove HTML
        text = re.sub("<[^>]+>", "", self.response.text)
        match = re.search(r"\b[vV]?(\d+(\.\d+){1,3})\b", text)
        return match.group(1) if match else None

    def tag(self, *args, **kwargs):
        """Return http response searched tags.
        tag: tag name to find.
        """
        soup = BeautifulSoup(self.response.text, "lxml")
        return soup.find(*args, **kwargs)

    def tags(self, *args, **kwargs):
        """Return http response searched tags.
        tag: tag name to find.
        """
        soup = BeautifulSoup(self.response.text, "lxml")
        return soup.findAll(*args, **kwargs)

    def xml(self):
        """Converts response into an XML object.
        """
        if not isinstance(self.response, bytes) and self.response.content:
            return html.fromstring(self.response.text)
        return html.HtmlElement()

    def scripts(self):
        """Return all src values of scripts in content page.
        """
        soup = BeautifulSoup(self.response.text, "lxml")
        scripts = [script.prettify() for script in soup.findAll("script")]
        return scripts

    def __find_sources(self):
        """Return all src values of scripts in content page.
        """
        return [str(src) for src in self.xml().xpath("//script/@src")]

    def __find_links(self):
        """Return all href values links in content page.
        """
        return self.xml().xpath("//a/@href")

    def __find_paths(self):
        paths = set()
        hostname = urlparse(self.url).netloc

        for link in self.links:
            parsed = urlparse(link)
            if parsed.path and (parsed.netloc == hostname or not parsed.netloc):
                paths.add(parsed.path)
        return list(paths)

    def images(self):
        """Return all src values of img in centent page.
        """
        return self.xml().xpath("//img/@src")

    def __repr__(self):
        return f"<[{self.code}] {self.url}>"