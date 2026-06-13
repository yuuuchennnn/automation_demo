import grpc

from proto import helloworld_pb2, helloworld_pb2_grpc


def say_hello(addr: str, name: str, timeout: float = 3.0) -> str:
    with grpc.insecure_channel(addr) as channel:
        stub = helloworld_pb2_grpc.GreeterServiceStub(channel)
        response = stub.SayHello(helloworld_pb2.SayHelloRequest(name=name), timeout=timeout)

    return response.message
