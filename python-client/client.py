import argparse

from greeter_client import say_hello


def main() -> None:
    parser = argparse.ArgumentParser(description="Call the Go gRPC GreeterService.")
    parser.add_argument("--addr", default="127.0.0.1:50051", help="gRPC server address")
    parser.add_argument("--name", default="Yuchen", help="name to greet")
    args = parser.parse_args()

    print(say_hello(args.addr, args.name))


if __name__ == "__main__":
    main()
