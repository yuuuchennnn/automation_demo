# Automation Demo

A full-stack API automation testing project built with **Go + Python**.


- **Go** — Provides a gRPC server (DemoService) and an HTTP demo server
- **Python** — A pytest-based testing framework that uses **gRPC reflection** to dynamically invoke server APIs without precompiling proto files
- **proto/** — Shared protobuf interface definitions
- **GitHub Actions** — CI pipeline that builds services, runs tests, and generates Allure reports

---

## Directory Structure

```text
automation_demo/
├── proto/                          # Proto interface definitions
│   └── helloworld/v1/helloworld.proto
│
├── go_services/                    # Go servers

│   ├── grpc_demo/                  #   gRPC Server (DemoService)
│   │   ├── cmd/server/main.go
│   │   ├── gen/                    #   Generated Go proto code
│   │   ├── Makefile
│   │   └── go.mod
│   └── http_demo/                  #   HTTP Demo Server
│       ├── cmd/server/main.go
│       ├── Makefile
│       └── go.mod
│
├── python_client/                  # Python automation test framework
│   ├── conftest.py                 # pytest global config & fixtures
│   ├── pytest.ini
│   ├── Makefile
│   ├── requirements.txt
│   ├── configs/config.ini          # Environment config (service addresses)
│   ├── functions/func_hub.py       # Core engine (HTTP/gRPC invocation)
│   ├── atom/                       # Atomic operation layer
│   ├── service/                    # Business logic layer
│   ├── TestCase/                   # Test cases
│   ├── TestData/                   # Test data (YAML)
│   └── tools/                      # Utility classes
│
├── .github/workflows/demo-ci.yml   # CI configuration
└── README.md
```

---

## Proto Interface

```protobuf
// proto/helloworld/v1/helloworld.proto
service DemoService {
  rpc SayHello(SayHelloRequest) returns (SayHelloResponse);
}
```
```

---

## Starting Go Services

### gRPC Server

```bash
cd go_services/grpc_demo

# Build & start (foreground)
make
make start-server

# Start in background
make start-server-bg
tail -f grpc-server.log

# Stop
make stop-server

# Custom port
make start-server ADDR=:50052
```

### HTTP Demo Server

```bash
cd go_services/http_demo

make
make start-server

# Start in background
make start-server-bg
tail -f http-demo-server.log

# Stop
make stop-server
```

Default port: `:8080`.

Example request:

```bash
curl -X POST http://localhost:8080/demo \
  -H 'Content-Type: application/json' \
  -d '{"startTime":"1","endTime":"2"}'
```

Health check:

```bash
curl http://localhost:8080/healthz
```

---

## Python Automation Testing

Detailed documentation for the testing framework is available in [`python_client/README.md`](python_client/README.md).

### Quick Start

```bash
cd python_client

# Install dependencies
make setup

# Run all tests
make test

# Run a single test file
.venv/bin/python -m pytest TestCase/Test_Demo/test_simple_grpc.py -v
```

### Architecture Overview

```
TestCase          ─  Test cases (pytest + YAML data driven)
    ↓
Service           ─  Business logic layer (orchestrates atom operations)
    ↓
Atom              ─  Atomic operation layer (wraps individual APIs)
    ↓
FuncHub           ─  Core engine (gRPC reflection / HTTP calls)
```

**Key Features**:

| Feature | Description |
|---------|-------------|
| **gRPC Reflection** | No `protoc` needed on the Python side — service definitions are dynamically resolved via reflection |
| **Data-Driven** | Test data managed in YAML, completely separated from code |
| **Auto Method Mapping** | The Atom layer uses `inspect` to automatically resolve the caller's method name and map it to the gRPC method |
| **Session-Level Cache** | The reflector and service name resolution results are reused across the entire pytest session |
| **Allure Reports** | Built-in Allure integration with CI report generation and archiving |

### Reflection Flow

```text
┌──────────┐   1. ServerReflectionInfo     ┌──────────┐
│  Python  │ ───────────────────────────▶  │  Go      │
│  Client  │   2. Dynamically fetch proto  │  Server  │
│  (yagrc) │ ◀───────────────────────────  │          │
│          │   3. Make actual RPC call     │          │
│          │ ───────────────────────────▶  │          │
└──────────┘                               └──────────┘
```

Enable reflection on the Go server:

```go
import "google.golang.org/grpc/reflection"

reflection.Register(server)
```

---

## Modifying Proto

```bash
# 1. Edit the proto file
vim proto/helloworld/v1/helloworld.proto

# 2. Regenerate Go code
cd go_services/grpc_demo
make proto

# 3. No regeneration needed for Python (uses reflection)
```

---

## CI (GitHub Actions)

Configuration file: `.github/workflows/demo-ci.yml`

CI pipeline:

1. **Checkout** code
2. **Build Go services** (gRPC + HTTP)
3. **Install Python dependencies**
4. **Start Go services** → **Run pytest**
5. Print server logs on failure
6. **Generate Allure report** → Upload as Artifact (retained for 14 days)

> Allure reports can be downloaded from the Actions page's Artifacts, or deployed to GitHub Pages.