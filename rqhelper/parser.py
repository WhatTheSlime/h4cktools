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
