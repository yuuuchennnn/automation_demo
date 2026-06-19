import pytest

from atom.grpcAtom.demo_grpc_atom import DemoGrpcAtom
from tools.data_reader import yamlDataProvider


class TestSimpleGrpc:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/simple_grpc.yaml"))
    def test_grpc_greeter(self, toolkits, testdata):

        DemoGrpcAtom().grpc_demo(toolkits, testdata)


