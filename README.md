# Go gRPC Demo

一个最小但完整的 Go gRPC 示例，包含：

- `proto/helloworld.proto`：gRPC 服务定义
- `cmd/server`：服务端
- `cmd/client`：客户端
- `gen/helloworld/v1`：由 `protoc` 生成的 Go 代码

## 本地运行

安装依赖：

```bash
go mod tidy
```

启动服务端：

```bash
go run ./cmd/server -addr :50051
```

另开一个终端调用客户端：

```bash
go run ./cmd/client -addr 127.0.0.1:50051 -name Yuchen
```

预期输出类似：

```text
response: Hello, Yuchen!
```

## 生成 proto 代码

如果修改了 `proto/helloworld.proto`，先安装生成插件：

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

然后重新生成：

```bash
make proto
```

## Linux 构建和部署

可以直接 clone 到 Linux 后编译。Linux 机器需要提前安装：

- Go 1.22 或更新版本
- make
- git

生成后的 gRPC 代码已经在 `gen/` 目录里，所以只要不修改 `proto/helloworld.proto`，Linux 上不需要安装 `protoc`。

在 Linux 机器上：

```bash
git clone <your-repo-url>
cd automation_demo
go mod tidy
make build
```

如果只想编译服务端：

```bash
make build-server
```

启动服务端：

```bash
./bin/grpc-server -addr :50051
```

服务启动后会监听 TCP `50051` 端口。另开一个终端测试：

```bash
./bin/grpc-client -addr 127.0.0.1:50051 -name Yuchen
```

预期输出类似：

```text
response: Hello, Yuchen!
```

后台启动可以用：

```bash
nohup ./bin/grpc-server -addr :50051 > grpc-server.log 2>&1 &
```

查看进程：

```bash
ps aux | grep grpc-server
```

查看日志：

```bash
tail -f grpc-server.log
```

如果服务器有防火墙或云安全组，需要开放 TCP `50051` 端口。

## 交叉编译 Linux 二进制

如果想在 macOS 上提前编译 Linux amd64 二进制：

```bash
make build-linux
```

只编译 Linux 服务端：

```bash
make build-linux-server
```

上传 `grpc-server-linux-amd64` 到 Linux 后运行：

```bash
chmod +x grpc-server-linux-amd64
./grpc-server-linux-amd64 -addr :50051
```
