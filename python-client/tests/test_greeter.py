import os

from greeter_client import say_hello


def test_say_hello_returns_name() -> None:
    addr = os.getenv("GRPC_ADDR", "127.0.0.1:50051")

    assert say_hello(addr, "Pytest") == "Hello, Pytest!"
