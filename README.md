# Go Service Demo

一个尽量简洁的 Go 服务 demo：

- Go 负责启动 gRPC server
- Go 负责启动 HTTP demo server
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
    http_demo/
      Makefile
      go.mod
      cmd/server/main.go

  python_client/
    Makefile
    client.py
    reflection_client.py
    tests/test_greeter.py
```

## 启动 Go gRPC Server

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

## 启动 Go HTTP Demo Server

```bash
cd go_services/http_demo
make
make start-server
```

后台启动：

```bash
make start-server-bg
tail -f http-demo-server.log
```

停止后台服务：

```bash
make stop-server
```

默认监听 `:8080`。换端口：

```bash
make start-server ADDR=:8081
```

接口示例：

```bash
curl -X POST http://localhost:8080/demo \
  -H 'Content-Type: application/json' \
  -d '{"startTime":"1","endTime":"2"}'
```

探活：

```bash
curl http://localhost:8080/healthz
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
