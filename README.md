# Go gRPC Server + Python Pytest Client

这个 demo 把 Go gRPC 服务端和 Python gRPC 测试客户端分开管理：

- `go-server/`：Go gRPC server、Go client、proto、生成的 Go 代码
- `python-client/`：Python reflection client、pytest 测试

Go 和 Python 各自维护自己的 `Makefile`，互不耦合。

## Go Server

Linux 或 macOS 上准备 Go 服务端：

```bash
cd go-server
make
```

`make` 等价于 `make setup`，会执行依赖整理和 Go 服务端/客户端编译。

前台启动服务：

```bash
make start-server
```

后台启动服务：

```bash
make start-server-bg
```

停止后台服务：

```bash
make stop-server
```

默认监听 `:50051`。如果要换端口：

```bash
make start-server ADDR=:50052
make start-server-bg ADDR=:50052
```

## Python Client

macOS 上准备 Python 客户端：

```bash
cd python-client
make
```

这个命令会：

- 创建 `python-client/.venv`
- 安装 `grpcio`、`grpcio-reflection`、`pytest`

Python 侧通过 gRPC Server Reflection 动态获取服务描述，不需要手动导入 `helloworld_pb2` 或生成 Python proto 代码。

## 用 pytest 请求 Go gRPC

如果 Go server 在同一台机器：

```bash
make test
```

如果 Go server 在 Linux 服务器上，从 macOS 请求：

```bash
make test ADDR=<linux-server-ip>:50051
```

也可以直接运行 Python client：

```bash
make run ADDR=<linux-server-ip>:50051 NAME=Yuchen
```

预期输出：

```text
Hello, Yuchen!
```

pytest 测试会通过 reflection 调用：

```text
/helloworld.v1.GreeterService/SayHello
```

并断言返回：

```text
Hello, Pytest!
```

## gRPC Reflection 原理

Go server 启动时注册 reflection：

```go
reflection.Register(server)
```

Python client 会先请求 reflection 服务，拿到 `GreeterService`、`SayHello`、`SayHelloRequest`、`SayHelloResponse` 的 descriptor，然后用 descriptor 动态创建 protobuf message，再通过原始 gRPC method path 发起调用：

```text
/helloworld.v1.GreeterService/SayHello
```

所以 Python 端不需要写：

```python
import helloworld_pb2
import helloworld_pb2_grpc
```

## Linux 部署提示

在 Linux 上 clone 后：

```bash
git clone <your-repo-url>
cd automation_demo
cd go-server
make
make start-server-bg
```

如果 macOS 要访问 Linux 上的服务，需要确认 Linux 防火墙或云安全组开放 TCP `50051`。

## 修改 proto 后重新生成

修改 `go-server/proto/helloworld.proto` 后，Go 侧需要重新生成：

```bash
cd go-server
make proto
```

Python 侧使用 reflection，请求时会从正在运行的 Go server 动态读取服务描述。
