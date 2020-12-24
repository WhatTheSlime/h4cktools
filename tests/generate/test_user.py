import os
import sys
import pytest

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.generate.user import password

@pytest.mark.parametrize(
    "length, punc", [
        (20, "!"),
        pytest.param(20, "", marks=pytest.mark.xfail),
        pytest.param(0, "!", marks=pytest.mark.xfail)
    ]
)
def test_password(length, punc):
    password(length=length, punc=punc)