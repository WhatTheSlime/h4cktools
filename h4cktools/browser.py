import asyncio
import requests
from lxml import html
from requests import adapters
from functools import partial
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


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
        return Page(await loop.run_in_executor(
            self.thread_pool, partial(super().request, *args, **kwargs)
        ))

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
        self.scode = response.status_code
        self.isok = (self.scode == 200)
        self.isforbidden = (self.scode == 403)
        self.isredirect = response.is_redirect

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

    # Status Code Methods
    def ok(self):
        """Return True if the requested url exists and is accessible, 
        False otherwise.
        """
        return self.response.status_code == 200

    def forbid(self):
        """Return True if the requested url is forbidden, False otherwise.
        """
        return self.response.status_code == 403

    def exists(self):
        """Return True if the requested url exists but not necessarily 
        accessible, False otherwise.
        """
        url = self.response.url
        location = ""
        if self.is_redirect:
            location = self.headers.get("Location", None)
            if location:
                location = remove_domain(location)
                url = remove_domain(url)
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
        if not isinstance(self.response, bytes):
            response = self.response.content
        return html.fromstring(response)

    def src(self):
        """Return all src values of scripts in content page.
        """
        return [str(src) for src in self.xml().xpath("//script/@src")]

    def scripts(self):
        """Return all src values of scripts in content page.
        """
        soup = BeautifulSoup(self.response.text, "lxml")
        scripts = [script.prettify() for script in soup.findAll("script")]
        return scripts

    def links(self):
        """Return all href values links in content page.
        """
        return self.xml().xpath("//link/@href")

    def images(self):
        """Return all src values of img in centent page.
        """
        return self.xml().xpath("//img/@src")

    def __repr__(self):
        return f"<[{self.scode}] {self.url}>"

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
        self.hist = []
        self.page = None
        self.page_index = 0

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

    def request(self, method, url: str, *args, **kwargs):
        parsed_url = urlparse(url)

        if not parsed_url.netloc:
            if self.scope:
                url = urljoin(self.scope, parsed_url.path)
            if not self.scope:
                raise Exception(
                    "Cannot resolve local url if the scope has not been defined."
                )
                
        return self.session.request(method, url, *args, **kwargs)

    def requests(self, method: str, urls: list, *args, **kwargs):
        futures = [
            asyncio.create_task(self.request(method, url, *args, **kwargs))
            for url in urls
        ]
        return [future for future in asyncio.as_completed(futures)]

    def get(self, url: str, *args, **kwargs):
        return self.request("GET", url, *args, **kwargs)

    def gets(self, urls: list, *args, **kwargs):
        return self.requests("GET", urls, *args, **kwargs)

    def post(self, url: str, *args, **kwargs):
        return self.request("POST", url, *args, **kwargs)

    def posts(self, urls: list, *args, **kwargs):
        return self.requests("GET", urls, *args, **kwargs)

    def head(self, url: str, *args, **kwargs):
        return self.request("HEAD", url, *args, **kwargs)

    def heads(self, urls: list, *args, **kwargs):
        return self.requests("HEAD", urls, *args, **kwargs)

    async def goto(self, url):
        """Go to new url and set it as new scope
        """ 
        self.page = await self.get(url)
        self.hist.append(self.page)
        self.page_index = len(self.hist) - 1
        self.set_scope(self.page.host)

    async def prev(self):
        """Go on previous page
        """
        if self.page_index > 0:
            self.page_index -= 1
            self.page = await self.get(self.hist[self.page_index].url)

    async def next(self):
        """Go on next page
        """
        if self.page_index < len(self.hist) - 1:
            self.page_index += 1
            self.page = await self.get(self.hist[self.page_index].url)

    def goin(self, sub_path: str):
        """Go in child local path
        """
        if not sub_path.startswith("/"):
            sub_path = "".join(["/", sub_path])
        path = "".join([self.page.path, sub_path])
        return self.goto(path)

    def goout(self):
        """Go in parent path
        """
        return self.goto("/".join(self.page.path.split("/")[:-1]))

    async def crawl(
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

    async def close(self):
        self.session.close()
