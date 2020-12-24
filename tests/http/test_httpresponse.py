import sys
import os
import pytest
import requests
import requests_mock
from urllib.parse import urljoin, urlparse

h4cktools = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools)

from h4cktools.http.httpresponse import HTTPResponse, links_attributes

WEBSITE = "http://test.com"
TESTFORM = """
<form action="/test_action" method="post" class="form-example">
    <div class="form-example">
        <input type="text" name="name" id="name" value="Test" required>
    </div>
    <div class="form-example">
        <input type="email" name="email" id="email" required>
    </div>
    <div class="form-example">
        <textarea name="description" id="desc">Testing</textarea>
    </div>
    <div class="form-example">
        <input type="submit" value="Submit!">
    </div>
</form>
"""


class TestHTTPResponse:
    """Test HTTPSession class"""

    @pytest.fixture(autouse=True)
    def setup(self):
        with requests_mock.Mocker() as mocker:
            mocker.get(WEBSITE)
            response = requests.get(WEBSITE)
            self.httpresponse_ok = HTTPResponse(response)

    def test_getattr(self):
        assert self.httpresponse_ok.status_code == 200

    def test_hooked(self):
        assert self.httpresponse_ok.iter_content()

    def test_repr(self):
        assert repr(self.httpresponse_ok) == f"<[200] {WEBSITE}/>"

    def test_forbid(self, requests_mock):
        path = "/forbidden"
        url = urljoin(WEBSITE, path)
        requests_mock.get(url, status_code=403)
        httpresponse = HTTPResponse(requests.get(url))
        assert httpresponse.isforbid

    def test_exists(self, requests_mock):
        path = "/redirect"
        url = urljoin(WEBSITE, path)
        requests_mock.get(
            url, status_code=301, headers={"Location": f"{path}/"}
        )
        httpresponse = HTTPResponse(requests.get(url, allow_redirects=False))
        assert httpresponse.exists
    
    def test_delay(self, requests_mock):
        requests_mock.get(WEBSITE)
        response = requests.get(WEBSITE)
        httpresponse = HTTPResponse(response)
        assert httpresponse.delay == response.elapsed.total_seconds()

    def test_xml(self, requests_mock):
        requests_mock.get(WEBSITE, text="test")
        assert HTTPResponse(requests.get(WEBSITE))
    
    def test_xpath(self, requests_mock):
        requests_mock.get(WEBSITE, text="<test>")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert httpresponse.xpath("//test")
    
    def test_hrefs(self, requests_mock):
        requests_mock.get(WEBSITE, text="<test href=''>")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert httpresponse.hrefs()
    
    def test_scripts(self, requests_mock):
        requests_mock.get(WEBSITE, text="<script>test<script>")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert httpresponse.scripts()

    def test_srcs(self, requests_mock):
        requests_mock.get(WEBSITE, text="<test src=''>")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert httpresponse.srcs()

    @pytest.mark.parametrize("attr", links_attributes)
    def test_links(self, requests_mock, attr):
        requests_mock.get(WEBSITE, text=f"<test {attr}=''>")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert httpresponse.links()

    @pytest.mark.parametrize(
        "path", [
            urljoin(WEBSITE, "test"), "/test", "./test",
        ]
    )
    def test_paths(self, requests_mock, path):
        requests_mock.get(WEBSITE, text=f"<test src='{path}'>")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        print(urlparse(path))
        assert httpresponse.paths() == [urlparse(path).path]

    def test_form(self, requests_mock):
        requests_mock.get(WEBSITE, text=TESTFORM)
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        action, form_dict = httpresponse.form()
        assert action == "/test_action"
        assert form_dict == {
            "email": "", "name": "Test", "description": "Testing"
        }

    def test_search(self, requests_mock):
        requests_mock.get(WEBSITE, text="TEST123!")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert httpresponse.search(r"\w+\!")

    def test_findall(self, requests_mock):
        requests_mock.get(WEBSITE, text="TEST123! TEST123!")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert httpresponse.findall(r"\w+\!") == ["TEST123!", "TEST123!"]

    def test_tag(self, requests_mock):
        requests_mock.get(WEBSITE, text="<a><b><c><a>")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert httpresponse.tag("a")

    def test_tags(self, requests_mock):
        requests_mock.get(WEBSITE, text="<a><b><c><a>")
        httpresponse = HTTPResponse(requests.get(WEBSITE))
        assert len(httpresponse.tags("a")) == 2