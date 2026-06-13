# Go gRPC Demo

一个尽量简洁的 gRPC demo：

- Go 负责启动 gRPC server
- Python 通过 gRPC reflection 调用 server
- `proto/` 放公共接口定义

## 目录

```text
automation_demo/
  proto/
    helloworld/v1/helloworld.proto

  go_services/
    greeter/
      Makefile
      go.mod
      cmd/server/main.go
      gen/

  python_client/
    Makefile
    client.py
    reflection_client.py
    tests/test_greeter.py
```

## 启动 Go Server

```bash
cd go_services/greeter
make
make start-server
```

后台启动：

```bash
make start-server-bg
tail -f grpc-server.log
```

停止后台服务：

```bash
make stop-server
```

默认监听 `:50051`。换端口：

```bash
make start-server ADDR=:50052
```

## 运行 Python Client

第一次运行先安装 Python 依赖：

```bash
cd python_client
make
```

请求本机服务：

```bash
make run
```

请求 Linux 机器上的服务：

```bash
make run ADDR=192.168.31.46:50051 NAME=Yuchen
```

运行 pytest：

```bash
make test ADDR=192.168.31.46:50051
```

## Reflection

Python 侧没有生成或导入 `helloworld_pb2.py`，而是通过 gRPC reflection 从 Go server 动态读取服务描述，然后调用：

```text
/helloworld.v1.GreeterService/SayHello
```

Go server 中开启 reflection 的位置：

```go
reflection.Register(server)
```

## 修改 Proto

修改：

```text
proto/helloworld/v1/helloworld.proto
```

重新生成 Go 代码：

```bash
cd go_services/greeter
make proto
```

Python 使用 reflection，不需要重新生成 Python 代码。


## cicd