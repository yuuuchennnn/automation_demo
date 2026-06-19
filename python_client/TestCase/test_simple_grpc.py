import pytest

from atom.grpcAtom.greeter import GreeterServiceGrpcAtom
from tools.data_reader import yamlDataProvider


class TestSimpleGrpc:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/simple_grpc.yaml"))
    def test_grpc_greeter(self, toolkits, testdata):

        GreeterServiceGrpcAtom.SayHello(toolkits, testdata)
