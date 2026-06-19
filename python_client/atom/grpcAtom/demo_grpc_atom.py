from atom.grpcAtom.base_grpc_atom import BaseGrpcAtom


class DemoGrpcAtom(BaseGrpcAtom):

    @classmethod
    def grpc_demo(cls, toolkits, json_req):
        return cls.grpc(toolkits, json_req)