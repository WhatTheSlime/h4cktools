import asyncio
import json
import re
import time
from urllib.parse import quote
from urllib.parse import urlparse
from requests.cookies import RequestsCookieJar

from rqhelper import aio
from rqhelper.responsewrapper import WrappedResponse
from rqhelper.parser import headers_list_to_dict

class ScopedSession(aio.Session):
    """ScopedSession is use make asynchonous requests in specified scope.
    It allows user to request a target by using a scope and send cookies only 
    to the target domain name and port.
    """

    def __init__(self, scope, workers=1, timeout=0):
        """Scoped Session constructor.

        Args:
            scope (str): target base urls.

        Keywords:
            workers (int): number of maximum tcp sessions.
            timeout (float): timeout beetween requests.
        """
        super(ScopedSession, self).__init__(workers=workers)
        self.set_scope(scope)
        self.set_domain_from_scope(scope)
        self.set_port_from_scope(scope)
        self.index_response = None
        self.timeout = float(timeout)

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

    def set_domain_from_scope(self, scope):
        """Parse scope to get domain of the target.
        """
        self.domain = re.search("(https?://)?([^/]+)", scope).group(2)

    def set_port_from_scope(self, scope):
        """Use url to detect port (use http protocol on port 80 by default)
        """
        url_parsed = urlparse(scope)
        port = "80"
        if url_parsed.port:
            port = str(url_parsed.port)
        elif url_parsed.scheme == "https":
            port = "443"
        self.port = port

    async def set_index_response(self):
        """Get the response of the index page
        """
        self.index_response = await self.get("/")

    def set_headers(self, args):
        """Changing headers according to arguments

        Args:
            args: argparse object.
        """
        self.headers = headers_list_to_dict(args.headers)
        if args.add_headers:
            self.headers.update(headers_list_to_dict(args.add_headers))

    async def request(self, method, url, *args, **kwargs):
        time.sleep(self.timeout)
        return WrappedResponse(
            await super().request(method, self.scope + url, *args, **kwargs),
            self.scope,
        )
