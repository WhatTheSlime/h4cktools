import os
import sys
import pytest

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.display import Logger


class TestLogger:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        path = d / "test.log"
        self.logger = Logger(filename=path, colors=True, verbosity=3)

    def test_success(self):
        self.logger.success("success")
    
    def test_partial(self):
        self.logger.partial("partial")

    def test_fail(self):
        self.logger.fail("fail")

    def test_info(self):
        self.logger.info("info")

    @pytest.mark.parametrize(
        "verbosity", [1, pytest.param(0, marks=pytest.mark.xfail)]
    )
    def test_verbose(self, verbosity):
        self.logger.verbose("verbose", v=verbosity)

    def test_warning(self):
        self.logger.warning("warning")
        
    def test_error(self):
        self.logger.error("error")
