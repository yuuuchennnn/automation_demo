import argparse
import sys

import grpc

from reflection_client import say_hello_with_reflection


def main() -> None:
    parser = argparse.ArgumentParser(description="Call the Go gRPC GreeterService.")
    parser.add_argument("--addr", default="192.168.31.46:50051", help="gRPC server address")
    parser.add_argument("--name", default="Yuchen", help="name to greet")
    parser.add_argument("--timeout", type=float, default=3.0, help="request timeout in seconds")
    args = parser.parse_args()

    try:
        print(say_hello_with_reflection(args.addr, args.name, timeout=args.timeout))
    except grpc.FutureTimeoutError:
        print(f"Failed to connect to {args.addr} within {args.timeout} seconds.", file=sys.stderr)
        print("Check that the gRPC server is running, reachable, and listening on this address.", file=sys.stderr)
        sys.exit(1)
    except grpc.RpcError as exc:
        print(f"gRPC call failed: {exc.code().name}: {exc.details()}", file=sys.stderr)
        print("If connection succeeds but reflection fails, make sure server reflection is enabled.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
