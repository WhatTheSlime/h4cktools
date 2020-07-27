import re
import lxml.html
from urllib.parse import urlparse, urljoin


def remove_domain(url):
    """Retrive begin of an url whatever if it start by http or https
    Args:
        url (str): Url to remove domain

    Returns:
        str: local path
    """
    if url.startswith("http://"):
        url = url[7:]
    if url.startswith("https://"):
        url = url[8:]

    return "".join(("/", "/".join(url.split("/")[1:])))

def is_local_url(url, session):
    """Return true if the url parameter is a local url and false otherwise.

    Args:
        session (lib.ScoppedSession): Current Session object.
        url: url to check

    Returns:
        bool: True if the url is local, else otherwise.
    """
    parsed_url = urlparse(url)

    return (
        not parsed_url.netloc
        or session.domain.replace("www.", "") in parsed_url.netloc
    )

def headers_list_to_dict(headers_list):
    """Converted a list of strings, each representing an http header, 
    into a dictionary.

    Args:
        headers_list (list): list of http headers to convert.

    Returns:
        dict: headers dict.
    """
    headers_dict = {}

    for header in headers_list:
        name, value = header.split(":", 1)
        headers_dict[name.strip()] = value.strip()

    return headers_dict