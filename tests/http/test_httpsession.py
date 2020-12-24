import sys
import os
import pytest
from urllib.parse import urljoin
h4cktools = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools)

from h4cktools.http.httpsession import HTTPSession

WEBSITE = "http://test.com"
WEBSITE2 = "http://test2.com"

PARENTPATH = "/parent"
CHILDPATH = "/child"


class TestHTTPSession:
    """Test HTTPSession class"""

    def test_agent(self):
        session = HTTPSession()
        session.agent = "test"
        assert session.agent == "test"

    def test_workers(self):
        session = HTTPSession()
        session.workers = 10
        assert session.workers == 10

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "host, path, result", 
        [
            (WEBSITE, "test", urljoin(WEBSITE, "test")),
            pytest.param("", "test", "", marks=pytest.mark.xfail)
        ]
    )
    async def test_request(self, requests_mock, host, path, result):
        session = HTTPSession()
        requests_mock.get("/".join([WEBSITE, "test"]))
        session.host = host
        response = await session.get(path)
        assert response.url == result


    def test_run(self, requests_mock):
        requests_mock.get(WEBSITE)
        session = HTTPSession()
        request = session.get(WEBSITE)
        assert session.run(request).pop().code == 200


    def test_goto(self, requests_mock):
        requests_mock.get(WEBSITE)
        session = HTTPSession()
        session.goto(WEBSITE)
        assert session.page.isok and session.host == WEBSITE


    def test_follow(self, requests_mock):
        requests_mock.get(
            WEBSITE, status_code=301, headers={"Location": WEBSITE2}
        )
        requests_mock.get(WEBSITE2)
        session = HTTPSession()
        session.goto(WEBSITE)
        session.follow()
        assert session.host == WEBSITE2
    

    def test_goin(self, requests_mock):
        #: http://test.com/parent/child
        fullurl = "".join([WEBSITE, PARENTPATH, CHILDPATH])
        #: http://test.com/parent
        parenturl = "".join([WEBSITE, PARENTPATH])
        requests_mock.get(WEBSITE)
        requests_mock.get(parenturl)
        requests_mock.get(fullurl)
        session = HTTPSession()
        session.goto(WEBSITE)
        # Test goin from root
        assert session.goin(PARENTPATH).path == PARENTPATH
        # Test goin from parent
        assert session.goin(CHILDPATH).path == "".join([PARENTPATH, CHILDPATH])

    def test_goout(self, requests_mock):
        #: http://test.com/parent/child
        fullurl = "".join([WEBSITE, PARENTPATH, CHILDPATH])
        #: http://test.com/parent
        parenturl = "".join([WEBSITE, PARENTPATH])
        requests_mock.get(WEBSITE)
        requests_mock.get(fullurl)
        requests_mock.get(parenturl)
        session = HTTPSession()
        session.goto(fullurl)
        assert session.goout().path == PARENTPATH
        # Test goout to root
        assert session.goout().path == "/"
        # Test goout to root when already in root 
        assert session.goout().path == "/"

    def test_prev(self, requests_mock):
        requests_mock.get(WEBSITE)
        requests_mock.get(WEBSITE2)
        session = HTTPSession()
        session.goto(WEBSITE)
        session.goto(WEBSITE2)
        assert session.prev().host == WEBSITE


    def test_next(self, requests_mock):
        requests_mock.get(WEBSITE)
        requests_mock.get(WEBSITE2)
        session = HTTPSession()
        session.goto(WEBSITE)
        session.goto(WEBSITE2)
        session.prev()
        assert session.next().host == WEBSITE2
    
