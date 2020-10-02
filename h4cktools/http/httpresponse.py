import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
from lxml import etree

links_attributes = [
    "href",
    "codebase",
    "cite",
    "action",
    "background",
    "longdesc",
    "profile",
    "src",
    "formaction",
    "icon",
    "manifest",
    "poster",
    "srcset",
    "archive"
]

class SoupError(Exception):
    pass

class HTTPResponse:
    """The class is a wrapper for requests.models.Response class.
    It implements helpful methods to analyse http(s) response.
    """
    def __init__(self, response):
        self._response = response
        parsed = urlparse(response.url)

        self._host = "://".join([parsed.scheme, parsed.netloc])
        self._path = parsed.path
        self._code = response.status_code
        self._xml = self._xmltree()

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

    def __repr__(self):
        return f"<[{self.code}] {self.url}>"

    @property
    def host(self):
        """
        """
        return self._host

    @property
    def path(self):
        """
        """
        return self._path

    @property
    def code(self):
        """
        """
        return self._code

    @property
    def isok(self):
        """
        """
        return self.code == 200

    @property
    def isforbid(self):
        """
        """
        return self.code == 403

    @property
    def exists(self):
        """Return True if the requested url exists but not necessarily 
        accessible, False otherwise.
        """
        url = self.url
        location = ""
        if self.is_redirect:
            location = self._response.headers.get("Location", None)
            if location:
                location = urlparse(location).path
                url = urlparse(url).path
        return self.code in (200, 401, 403) or location == "".join((url, "/"))

    @property
    def delay(self):
        """Reteurn response time in seconds.
        """
        self._response.elapsed.total_seconds()

    def _xmltree(self):
        """Converts response into an XML object

        Returns:

        """
        return etree.HTML(self._response.content)

    def xpath(self, query):
        """Excute xpath on xmltree
        """
        return self._xml.xpath(query)

    def hrefs(self):
        """Return all href values links in content page.
        """
        return self.xpath("//@href")

    def scripts(self):
        """Return all src values of scripts in content page

        Returns:

        """
        soup = BeautifulSoup(self._response.text, "lxml")
        scripts = [script.prettify() for script in soup.findAll("script")]
        return scripts

    def srcs(self):
        """Return all src values in content page
        """
        return self.xpath("//@src")


    def links(self):
        links = set()
        for attr in links_attributes:
            for link in self.xpath(f"//@{attr}"):
                links.add(link)
        return list(links)

    
    def paths(self) -> list:
        """Find all host paths in the page

        Returns:
            list: host paths
        """
        paths = []
        host = urlparse(self.host).netloc

        for link in self.links():
            parsed = urlparse(link)
            if (
                parsed.path and 
                (parsed.netloc == host or not parsed.netloc)
            ):
                paths.append(parsed.path)
        return paths

    
    def search(self, regex: str):
        """Use regular expression to search expression in the response content.
        
        Args:
            regex: regular(s) expression to use. 
        """
        if isinstance(regex, str):
            return re.search(regex, self._response.text)
        if isinstance(regex, list):
            for r in regex:
                match = re.search(r, self._response.text)
                if match:               
                    return match


    def findall(self, regex):
        """Use regular expression to find all match of an expression in the 
        response content.
        
        Args:
            regex: regular expression to use.

        Return:
            list: 
        """
        return re.findall(regex, self._response.text)


    def soup(self):
        self._soup = BeautifulSoup(self._response.text, "lxml")


    def tag(self, *args, **kwargs):
        """Return http response searched tags.
        
        Args:
            tag: tag name to find.
        
        Return:

        """
        try:
            self._soup
        except AttributeError:
            raise SoupError("Call 'soup()' method first")
        return self._soup.find(*args, **kwargs)


    def tags(self, *args, **kwargs):
        """Return http response searched tags
        Args:
            BeautifulSoup.findall args

        Returns:

        """
        try:
            self._soup
        except AttributeError:
            raise SoupError("Call 'soup()' method first")
        return self._soup.findAll(*args, **kwargs)


    def formdict(self, **attrs):
        form_dict = {}
        form = self.tag("form", attrs=attrs)

        for inp in form.findAll("input"):
            if "name" in inp.attrs:
                form_dict[inp["name"]] = inp["value"]
        for texa in form.findAll("textarea"):
            if "name" in texa.attrs:
                form_dict[texa["name"]] = texa.text

        return form_dict