import os
import sys
import pytest

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.parse.versions import extract_version, extract_versions, Version


@pytest.mark.parametrize(
    "quantifier, result", 
    [
        (1, "1.2.3.4"), 
        (3, "1.2.3"), 
        pytest.param(0, "1.2.3", marks=pytest.mark.xfail)
    ]
)
def test_extract_version(quantifier, result):
    """Test extract_version function"""
    text = "Some text1.2.3.4Some text"
    assert str(extract_version(text, quantifier=quantifier)) == result


def test_extract_versions():
    """Test extract_versions function"""
    text = "Some text1.2.3.4Some text3.2.1Some text"

    assert [str(v) for v in extract_versions(text)] == ["1.2.3.4", "3.2.1"]


class TestVersion:
    """Test Version class"""
    @pytest.fixture(autouse=True)
    def setup(self):
        self.v1 = Version("1.2.3")
        self.v2 = Version("1.2.4")
        self.v3 = Version("1.2.3.4")
        self.v4 = Version("3.1.2")

    def test__init__(self):
        """Test Version.__init__ method"""
        with pytest.raises(AttributeError):
            Version(12346)

    def test__eq__(self):
        """Test Version.__eq__ method"""
        assert self.v1 == Version("1.2.3")
        assert self.v1 != self.v3
        assert self.v1 != self.v4

    def test__lt__(self):
        """Test Version.__lt__ method"""
        assert self.v1 < self.v2
        assert not (self.v4 < self.v1)
        assert not(self.v1 < Version("1.2.3"))

    def test__la__(self):
        """Test Version.__la__ method"""
        assert self.v1 <= Version("1.2.3")
        assert self.v1 <= self.v4

    def test__repr__(self):
        """Test Version.__repr__ method"""
        assert repr(self.v1) == "1.2.3" 