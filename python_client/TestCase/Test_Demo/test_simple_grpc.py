import pytest

from atom.grpcAtom.demo_grpc_atom import DemoServiceGrpcAtom
from tools.data_reader import yamlDataProvider


class TestSimpleGrpc:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Demo/simple_grpc.yaml"))
    def test_grpc_demo(self, toolkits, testdata):
        res = DemoServiceGrpcAtom.SayHello(toolkits, testdata["request_dict"])
        
        assert res.get("message") == testdata["expected"]
