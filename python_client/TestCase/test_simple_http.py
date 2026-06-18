import pytest
from tools.data_reader import yamlDataProvider
from service.demo.http_demo_service import HttoDemoService

class TestSimpleHttpAtom:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/simple_http.yaml"))
    def test_http_request(self, toolkits, testdata):
        demo_service = HttoDemoService(toolkits, testdata)
        demo_service.call_demo_http()