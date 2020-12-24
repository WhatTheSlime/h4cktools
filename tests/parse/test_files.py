import argparse
import os
import sys

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.parse.files import loadlist

def test_loadlist(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.lst"
    p.write_text("#test0?\ntest1?\ntest2?\ntest3?")

    lst = loadlist(p, separator=":", replace={"?": ""}, ignores=["#"])
    assert lst == ["test1", "test2", "test3"]