import os
import sys

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.encode import (
    b64encode,
    hexencode,
    uhexencode,
    octencode,
    urlencode,
    urlb64encode,
    furlencode,
    durlencode,
    htmlencode,
    fhtmlencode,
    b64decode,
    htmldecode,
    urldecode,
    urlb64decode,
    autodecode
)

# Encode
def test_b64encode():
    assert b64encode("test") == "dGVzdA=="

def test_hexencode():
    assert hexencode("test") == "\\x74\\x65\\x73\\x74"

def test_uhexencode():
    assert uhexencode("test") == "\\u0074\\u0065\\u0073\\u0074"

def test_octencode():
    assert octencode("test") == "\\0o164\\0o145\\0o163\\0o164"

def test_urlencode():
    assert urlencode("test test") == "test+test"

def test_urlb64encode():
    assert urlb64encode("test test") == "dGVzdCt0ZXN0"

def test_furlencode():
    assert furlencode("test") == "%74%65%73%74"

def test_durlencode():
    assert durlencode("test") == "%25%37%34%25%36%35%25%37%33%25%37%34"

# Decode
def test_htmlencode():
    assert htmlencode("test &") == "test &amp;"

def test_fhtmlencode():
    assert fhtmlencode("test") == "&#116&#101&#115&#116"

def test_b64decode():
    assert b64decode("dGVzdA==") == "test"

def test_htmldecode():
    assert htmldecode("test &amp;") == "test &"

def test_urldecode():
    assert urldecode("test+test") == "test test"
    assert urldecode("%74%65%73%74") == "test"
    assert urldecode(
        urldecode("%25%37%34%25%36%35%25%37%33%25%37%34")
    ) == "test"

def test_urlb64decode():
    assert urlb64decode("dGVzdA%3D%3D") == "test"

def test_autodecode():
    autodecode("")