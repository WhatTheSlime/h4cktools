import urllib3

from pathlib import Path
from urllib.parse import (
	urlparse,
	urljoin,
	urlencode as qurlencode,
)

from .http import HTTPSession, AsyncSession
from .encoder import *
from .cipher import *
from .versions import (
	version_regex, 
	extract_version, 
	extract_versions, 
	Version as ver
)
from .xss import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)