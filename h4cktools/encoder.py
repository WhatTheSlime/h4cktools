from base64 import (
	urlsafe_b64encode, 
	urlsafe_b64decode, 
	b64encode as _b64encode, 
	b64decode as _b64decode
)
import cgi
from urllib.parse import (
	quote_plus,
	unquote_plus
)

def b64encode(obj, encoding="utf-8"):
	_obj = obj
	if not isinstance(obj, bytes):
		_obj = str(obj).encode(encoding)
	return _b64encode(_obj).decode(encoding)

def b64decode(obj, encoding="utf-8"):
	_obj = obj
	if not isinstance(obj, bytes):
		_obj = str(obj).encode(encoding)
	return _b64decode(_obj).decode(encoding)

def urlencode(s: str, safe: str = "", encoding: str = "utf-8", errors: str = "replace"):
	return quote_plus(s, safe=safe, encoding=encoding, errors=errors)

def urldecode(s: str, encoding: str = "utf-8", errors: str = "replace"):
	"""Url and base64 encode characters of a string 

	Args:
		s: string to encode

	Returns:
		str: encoded string
	"""
	return unquote_plus(s, encoding=encoding, errors=errors)

def urlb64encode(obj, encoding="utf-8"):
	"""Url and base64 encode characters of a string 

	Args:
		s: string to encode

	Returns:
		str: encoded string
	"""
	_obj = obj
	if not isinstance(obj, bytes):
		_obj = str(obj).encode(encoding)
	return urlsafe_b64encode(_obj).decode(encoding)

def urlb64decode(obj, encoding="utf-8"):
	"""Url and base 64 decode characters of a string

	Args:
		s: string to encode

	Returns:
		str: encoded string
	"""
	_obj = obj
	if not isinstance(obj, bytes):
		_obj = str(obj).encode(encoding)
	return urlsafe_b64decode(_obj).decode(encoding)

def furlencode(s: str):
	"""Url encode all characters of a string

	Args:
		s: string to encode

	Returns:
		str: encoded string
	"""
	return "".join("%{0:0>2}".format(
		format(ord(c), "x")) for c in s
	)

def furldecode(s):
	return "".join("%{0:0>2}".format(
		format(ord(c), "x")
	) for c in s)

def htmlencode(s):
	return cgi.escape(s).encode("ascii", "xmlcharrefreplace")

