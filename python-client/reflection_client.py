import grpc
from google.protobuf import descriptor_pool, message_factory
from grpc_reflection.v1alpha import proto_reflection_descriptor_database


SERVICE_NAME = "helloworld.v1.GreeterService"
METHOD_NAME = "SayHello"


def say_hello_with_reflection(addr: str, name: str, timeout: float = 3.0) -> str:
    with grpc.insecure_channel(addr) as channel:
        grpc.channel_ready_future(channel).result(timeout=timeout)

        reflection_db = proto_reflection_descriptor_database.ProtoReflectionDescriptorDatabase(channel)
        pool = descriptor_pool.DescriptorPool(reflection_db)

        service = pool.FindServiceByName(SERVICE_NAME)
        method = service.FindMethodByName(METHOD_NAME)

        request_cls = message_factory.GetMessageClass(method.input_type)
        response_cls = message_factory.GetMessageClass(method.output_type)

        request = request_cls(name=name)
        call = channel.unary_unary(
            f"/{service.full_name}/{method.name}",
            request_serializer=lambda msg: msg.SerializeToString(),
            response_deserializer=response_cls.FromString,
        )
        response = call(request, timeout=timeout)

    return response.message
