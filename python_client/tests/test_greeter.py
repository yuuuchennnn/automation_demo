import os

from reflection_client import say_hello_with_reflection


def test_say_hello_returns_name_through_reflection() -> None:
    addr = os.getenv("GRPC_ADDR", "127.0.0.1:50051")

    assert say_hello_with_reflection(addr, "Pytest") == "Hello, Pytest!"
