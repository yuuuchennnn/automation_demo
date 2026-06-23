import pytest

from atom.grpcAtom.greeter import GreeterServiceGrpcAtom
from tools.data_reader import yamlDataProvider


class TestSimpleGrpc:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Demo/simple_grpc.yaml"))
    def test_grpc_greeter(self, toolkits, testdata):

        res = GreeterServiceGrpcAtom.SayHello(toolkits, testdata["input_data"])
        
        assert res.get("message") == testdata["expected"]
