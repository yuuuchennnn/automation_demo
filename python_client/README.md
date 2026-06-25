# Python Client — gRPC & HTTP Automation Testing Framework

A pytest-based API automation testing framework that dynamically invokes server APIs via **gRPC reflection** (no precompiled proto stubs needed) and supports HTTP API testing. Built with a layered architecture, data-driven design, and Allure reporting.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Writing Tests](#writing-tests)
  - [Adding a gRPC Test](#adding-a-grpc-test)
  - [Adding an HTTP Test](#adding-an-http-test)
- [Test Data Management](#test-data-management)
- [Running Tests](#running-tests)
- [Configuration](#configuration)
- [Reports](#reports)
- [Dependencies](#dependencies)

---

## Quick Start

### 1. Start the Dependent Services

Make sure the gRPC and HTTP servers are running (see the top-level [`README.md`](../README.md)):

```bash
# Start the gRPC Server
cd go_services/grpc_demo
make start-server-bg

# Start the HTTP Server
cd go_services/http_demo
make start-server-bg
```

### 2. Install Python Dependencies

```bash
cd python_client
make setup
# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Tests

```bash
cd python_client

# Run all tests
make test

# Run a specific test file
.venv/bin/python -m pytest TestCase/Test_Demo/test_simple_grpc.py

# Specify environment (default: test)
.venv/bin/python -m pytest --env test
```

---

## Project Structure

```text
python_client/
├── conftest.py                # pytest global config & fixtures
├── pytest.ini                 # pytest configuration
├── Makefile                   # Automation commands
├── requirements.txt           # Python dependencies
│
├── configs/
│   └── config.ini             # Environment config (service addresses)
│
├── functions/
│   └── func_hub.py            # Core: FuncHub utility class
│
├── atom/                      # Atomic operation layer
│   ├── grpcAtom/
│   │   ├── base_grpc_atom.py  # gRPC base class (auto resolves service + method)
│   │   └── demo_grpc_atom.py         # DemoService definition
│   └── httpAtom/
│       ├── base_http_atom.py  # HTTP base class
│       └── demo_http_atom.py  # HTTP demo API wrapper
│
├── service/                   # Business logic layer (orchestrates atoms)
│   ├── baseService.py         # Base service class
│   └── demo/
│       └── http_demo_service.py  # HTTP demo business logic
│
├── TestCase/                  # Test cases
│   └── Test_Demo/
│       ├── test_simple_grpc.py
│       └── test_simple_http.py
│
├── TestData/                  # Test data (YAML)
│   └── Demo/
│       ├── simple_grpc.yaml
│       └── simple_http.yaml
│
├── tools/
│   └── data_reader.py         # YAML data reader utility
│
└── allure-results/            # Allure report results (auto-generated)
```

---

## Architecture

The framework uses a **four-layer architecture**, from bottom to top:

```text
┌─────────────────────────────────────────────┐
│              TestCase                        │
│  test_simple_grpc.py / test_simple_http.py   │
├─────────────────────────────────────────────┤
│              Service                         │
│  http_demo_service.py — orchestrates atoms   │
├─────────────────────────────────────────────┤
│      Atom                                   │
│  demo_grpc_atom.py / demo_http_atom.py             │
├─────────────────────────────────────────────┤
│       Functions                             │
│  FuncHub — make_http_call / make_grpc_call  │
└─────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility | Description |
|-------|---------------|-------------|
| **Functions** | gRPC / HTTP invocation engine | `FuncHub` provides `make_http_call()` and `make_grpc_call()`. The gRPC side uses **yagrc reflection** to dynamically resolve services and methods — no proto compilation needed |
| **Atom** | API method-level encapsulation | One Python method maps to one gRPC method or HTTP endpoint. gRPC atom classes use `inspect` to auto-detect the caller's method name and resolve the target service |
| **Service** | Business logic orchestration | Combines multiple atom operations to complete a business scenario — parameter assembly, pre-assertion data preparation |
| **TestCase** | Test cases | Data-driven via pytest, reads YAML test data, invokes through Service or Atom layer, then asserts |

### Key Highlights

#### Dynamic gRPC Reflection

```text
┌──────────┐   1. gRPC Reflection Query   ┌──────────┐
│  Python  │ ──────────────────────────▶  │  Go      │
│  Client  │                              │  Server  │
│          │   2. Dynamically resolve     │          │
│          │      Service / Method        │          │
│          │ ◀──────────────────────────  │          │
│          │   3. Make actual RPC call    │          │
│          │ ──────────────────────────▶  │          │
└──────────┘                              └──────────┘
```

- **No proto-generated Python code needed** — just enable reflection on the server
- Only one reflection query per pytest session; results are cached for subsequent calls

#### Auto Method Name Matching

The Atom layer uses `inspect` to get the call stack and automatically maps the Python method name to the gRPC method name:

# demo_grpc_atom.py

class DemoServiceGrpcAtom(BaseGrpcAtom):
    @classmethod
    def SayHello(cls, toolkits, json_req):
        return cls.grpc(toolkits, json_req)

        # Auto-resolves: service="DemoService", method="SayHello"
```

---

## Writing Tests

### Adding a gRPC Test

Suppose you want to test a gRPC service named `Calculator` with method `Add`.

#### 1. Configure the Service Address

Edit `configs/config.ini`:

```ini
[GRPC]
DemoService = localhost:50051
Calculator = localhost:50052       # Add this line
```

#### 2. Create an Atom Class

`atom/grpcAtom/calculator.py`:

```python
from atom.grpcAtom.base_grpc_atom import BaseGrpcAtom

class CalculatorGrpcAtom(BaseGrpcAtom):

    @classmethod
    def Add(cls, toolkits, json_req):
        return cls.grpc(toolkits, json_req)
```

> **Note**: The class name must match the proto service name (stripped of the `GrpcAtom` suffix). For example, `CalculatorGrpcAtom` → `Calculator`.
>
> If the proto service includes a package prefix like `v1.Calculator`, name your class `V1CalculatorGrpcAtom` or adjust the package path in `base_grpc_atom.py`.

#### 3. Prepare Test Data

`TestData/Demo/calculator.yaml`:

```yaml
- testCase:
    testId: tc-add-1
    testName: calculator_add_normal
  testData:
    request_dict:
      x: 3
      y: 5
    expected: 8
```

#### 4. Write the Test Case

`TestCase/Test_Demo/test_simple_calculator.py`:

```python
import pytest
from atom.grpcAtom.calculator import CalculatorGrpcAtom
from tools.data_reader import yamlDataProvider

class TestCalculator:

    @pytest.mark.parametrize("testdata", yamlDataProvider("TestData/Demo/calculator.yaml"))
    def test_add(self, toolkits, testdata):
        res = CalculatorGrpcAtom.Add(toolkits, testdata["request_dict"])
        assert res.get("result") == testdata["expected"]
```

### Adding an HTTP Test

#### 1. Configure the Service Address

```ini
[HTTP]
http_domain = http://localhost:8080
my_api = https://api.example.com     # Add this line
```

#### 2. Create an Atom Class

`atom/httpAtom/my_api_atom.py`:

```python
class MyApiAtom:

    @staticmethod
    def get_user(toolkits, user_id):
        make_http_call = toolkits['http']
        path = f"/users/{user_id}"
        return make_http_call("my_api", path, method="get")
```

#### 3. Write the Test

```python
def test_get_user(self, toolkits):
    res = MyApiAtom.get_user(toolkits, 123)
    assert res["status_code"] == 200
```

---

## Test Data Management

Test data is stored in the `TestData/` directory in **YAML** format, read by the `yamlDataProvider()` function in `tools/data_reader.py`.

### Data Format

```yaml
- testCase:
    testId: tc-1                    # Test case ID (required; used as parametrize id)
    testName: "my test case name"   # Test case name
    testOwner: owner1               # Owner
    testDescription: "description"  # Description
    isAutomated: Y                  # Automated? Y / N
  testData:
    request_dict:                   # Request parameters (parsed as dict)
      name: "yuchen"
    expected: "Hello, yuchen!"      # Expected result
```

> `yamlDataProvider()` returns a dictionary with all fields under `testData`. In your test, reference them as `testdata["request_dict"]`, `testdata["expected"]`, etc.

---

## Running Tests

```bash
# Run all tests
make test

# Run a specific file
.venv/bin/python -m pytest TestCase/Test_Demo/test_simple_grpc.py

# Run a specific test class
.venv/bin/python -m pytest TestCase/Test_Demo/test_simple_grpc.py::TestSimpleGrpc

# Run a specific test method
.venv/bin/python -m pytest TestCase/Test_Demo/test_simple_grpc.py::TestSimpleGrpc::test_grpc_demo

# Specify environment
.venv/bin/python -m pytest --env stage

# With Allure report
.venv/bin/python -m pytest --alluredir=allure-results

# View Allure report
allure serve allure-results
```

### pytest.ini Default Configuration

```ini
[pytest]
testpaths = TestCase              # Scans TestCase directory by default
pythonpath = .                    # Adds project root to Python path
addopts = -s --alluredir=allure-results   # Allure enabled by default
log_cli = true                    # Real-time console logging
```

---

## Configuration

`configs/config.ini` is the environment configuration file. Use the `--env` flag to select an environment (default: `test`):

```ini
[HTTP]
http_domain = http://localhost:8080

[GRPC]
```

**Multi-environment example** (using different sections in `configs/config.ini`):

```ini
[HTTP]
http_domain = http://localhost:8080

[HTTP-stage]
http_domain = https://stage.api.example.com
[GRPC]
DemoService = localhost:50051
[GRPC-stage]
DemoService = stage-server:50051
```

> `FuncHub.env()` reads sections by name, so multi-environment setups should be organized using section naming conventions.

---

## Reports

### Allure Reports

Tests generate Allure results in the `allure-results/` directory by default.

**View locally**:

```bash
# Install the Allure CLI tool first
brew install allure      # macOS
# or
sudo apt install allure  # Ubuntu

# Serve the report
allure serve allure-results
```

**Generate static HTML**:

```bash
allure generate allure-results -o allure-report
```

---

## Dependencies

| Library | Purpose |
|---------|---------|
| `grpcio` | gRPC core library |
| `grpcio-reflection` | gRPC Server Reflection support |
| `yagrc` | Dynamic proto loading via reflection — no precompilation needed |
| `protobuf` | Protocol Buffers serialization |
| `requests` | HTTP requests |
| `pytest` | Testing framework |
| `pyyaml` | YAML file parsing |
| `loguru` | Logging |
| `allure-pytest` | Allure test report integration |
