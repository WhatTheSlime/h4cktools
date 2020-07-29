import urllib3

from .http import HTTPSession, AsyncSession
from .coder import *
from .cipher import *
from .versions import (
	version_regex, 
	extract_version, 
	extract_versions, 
	Version as ver
)
from pathlib import Path
from .xss import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)