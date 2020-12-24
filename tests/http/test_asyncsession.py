import sys
import os
import pytest

h4cktools = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
sys.path.append(h4cktools)

from h4cktools.http.asyncsession import AsyncSession

WEBSITE = "http://test.com"

class TestAsyncSession:

    @pytest.mark.asyncio
    async def test_request(self, requests_mock):
        requests_mock.get(WEBSITE)
        response = await AsyncSession().request("GET", WEBSITE)
        assert response.status_code == 200
    

    def test_run(self, requests_mock):
        session = AsyncSession()

        requests_mock.get(WEBSITE)
        responses = session.run(
            session.get(WEBSITE), session.get(WEBSITE)
        )
        assert [r.status_code for r in responses] == [200, 200]