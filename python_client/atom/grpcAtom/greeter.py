from atom.grpcAtom.base_grpc_atom import BaseGrpcAtom


class GreeterServiceGrpcAtom(BaseGrpcAtom):

    @classmethod
    def SayHello(cls, toolkits, json_req):
        return cls.grpc(toolkits, json_req)
