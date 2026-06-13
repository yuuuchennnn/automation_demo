# Go gRPC Services + Python Pytest Client

这个 demo 按“公共 proto + 多服务目录 + 独立 Python 测试客户端”的方式组织，后续可以继续扩展多个 Go gRPC 服务。

## 目录结构

```text
automation_demo/
  proto/
    helloworld/v1/helloworld.proto

  services/
    greeter/
      Makefile
      go.mod
      cmd/
        server/main.go
        client/main.go
      gen/

  python-client/
    Makefile
    client.py
    reflection_client.py
    tests/test_greeter.py
```

- `proto/`：公共接口契约，多个服务和多语言客户端都可以复用
- `services/greeter/`：Greeter Go gRPC 服务，独立构建、启动、部署
- `python-client/`：Python reflection client 和 pytest 测试

## 启动 Go 服务

```bash
cd services/greeter
make
make start-server
```

后台启动：

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

后台日志：

```bash
tail -f grpc-server.log
```

## Python pytest 请求 Go gRPC

Python 侧通过 gRPC Server Reflection 动态获取服务描述，不需要生成 Python proto 文件，也不需要导入 `helloworld_pb2`。

准备 Python 环境：

```bash
cd python-client
make
```

请求本机 Go 服务：

```bash
make test
```

从 macOS 请求 Linux 上的 Go 服务：

```bash
make test ADDR=<linux-server-ip>:50051
```

直接运行 Python client：

```bash
make run ADDR=<linux-server-ip>:50051 NAME=Yuchen
```

预期输出：

```text
Hello, Yuchen!
```

## gRPC Reflection

Go server 启动时注册 reflection：

```go
reflection.Register(server)
```

Python client 会先请求 reflection 服务，拿到 `GreeterService`、`SayHello`、`SayHelloRequest`、`SayHelloResponse` 的 descriptor，然后动态创建 protobuf message，并调用：

```text
/helloworld.v1.GreeterService/SayHello
```

## 修改 proto 后重新生成 Go 代码

修改公共 proto：

```text
proto/helloworld/v1/helloworld.proto
```

重新生成 Greeter 服务的 Go 代码：

```bash
cd services/greeter
make proto
```

Python 侧使用 reflection，会从正在运行的 Go server 动态读取服务描述。

## 继续添加 Go 服务

后续新增服务时，建议继续放到 `services/` 下：

```text
services/
  greeter/
  user/
  order/
```

每个服务维护自己的：

```text
Makefile
go.mod
cmd/server
internal/
gen/
```

公共 proto 继续放在根目录 `proto/`：

```text
proto/
  helloworld/v1/helloworld.proto
  user/v1/user.proto
  order/v1/order.proto
```
