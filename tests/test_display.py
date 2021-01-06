import os
import sys

h4cktools_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools_path)

from h4cktools.display import Logger

def test_logger(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    path = d / "test.log"
    logger = Logger(filename=path, colors=True, verbosity=3)

    logger.success("success")
    logger.partial("partial")
    logger.fail("fail")
    logger.info("info")
    logger.debug("debug")
    logger.warning("warning")
    logger.error("error")