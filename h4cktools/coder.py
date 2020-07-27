from base64 import (
	urlsafe_b64encode, 
	urlsafe_b64decode, 
	b64encode, 
	b64decode
)
import cgi
from urllib.parse import (
	quote_plus,
	unquote_plus
)


def b64enc(s, altchars=None):
	return b64encode(s, altchars=altchars)

def b64dec(s, altchars=None, validate=False):
	return b64decode(s, altchars=altchars, validate=validate)

def urlenc(s, safe="", encoding="utf-8", errors="replace"):
	return quote_plus(s, safe=safe, encoding=encoding, errors=errors)

def urldec(s, encoding="utf-8", errors="replace"):
	return unquote_plus(s, encoding=encoding, errors=errors)

def urlb64enc(s):
	return urlsafe_b64encode(s)

def urlb64dec(s):
	return urlsafe_b64decode(s)

def durlenc(s, safe="", encoding="utf-8", errors="replace"):
	url = urlenc(s, safe=safe, encoding=encoding, errors=errors)
	return urlenc(url, safe=safe, encoding=encoding, errors=errors)

def htmlenc(s):
	return cgi.escape(s).encode("ascii", "xmlcharrefreplace")