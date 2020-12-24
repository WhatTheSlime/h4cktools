import os
import sys
import pytest

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.parse.http import (
    headers2dict, dict2headers, query2dict, dict2query
)

def test_headers2dict():
    raw = """
    User-Agent: test
    Connection: test
    """
    assert headers2dict(raw) == {"Connection": "test", "User-Agent": "test"}

def test_dict2headers():
    dict2headers({})

def test_query2dict():
    assert query2dict("a=1&b=2&c=3&d") == {"a": "1", "b": "2", "c": "3"}

def test_dict2query():
    dict2query({})