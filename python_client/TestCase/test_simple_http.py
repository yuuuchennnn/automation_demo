import pytest
from tools.data_reader import yamlDataProvider
from service.demo.http_demo_service import HttpDemoService

class TestSimpleHttpAtom:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/simple_http.yaml"))
    def test_http_request(self, toolkits, testdata):
        demo_service = HttpDemoService(toolkits, testdata)
        res = demo_service.call_demo_api_post()
        assert res.get('error_msg',0) == 0