import bs4
import html
import lxml.html
import re
import types

from lib.utils.parser import remove_domain


class WrappedResponse:
    """The class is a wrapper for requests.models.Response class.
    It implements helpful methods to analyse http(s) response.
    """

    def __init__(self, response, scope):
        self.response = response
        self.scope = scope
        self.local_url = response.url[len(scope) :]

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

    def is_ok(self):
        """Return True if the requested url exists and is accessible, 
        False otherwise.
        """
        return self.response.status_code == 200

    def is_forbidden(self):
        """Return True if the requested url is forbidden, False otherwise.
        """
        return self.response.status_code == 403

    def is_present(self):
        """Return True if the requested url exists but not necessarily 
        accessible, False otherwise.
        """
        url = self.response.url
        location = ""
        if self.response.is_redirect:
            location = self.response.headers.get("Location", None)
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
        soup = bs4.BeautifulSoup(self.response.text, "lxml")
        return soup.find(*args, **kwargs)

    def tags(self, *args, **kwargs):
        """Return http response searched tags.

        tag: tag name to find.
        """
        soup = bs4.BeautifulSoup(self.response.text, "lxml")
        return soup.findAll(*args, **kwargs)

    def xml(self):
        """Converts response into an XML object.
        """
        if not isinstance(self.response, bytes):
            response = self.response.content

        return lxml.html.fromstring(response)

    def src(self):
        """Return all src values of scripts in content page.
        """
        return [str(src) for src in self.xml().xpath("//script/@src")]

    def scripts(self):
        """Return all src values of scripts in content page.
        """
        soup = bs4.BeautifulSoup(self.response.text, "lxml")
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
