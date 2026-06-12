.PHONY: proto build build-server build-client build-linux build-linux-server build-linux-client run-server run-client tidy clean

BIN_DIR := bin
SERVER_BIN := grpc-server
CLIENT_BIN := grpc-client
LINUX_GOOS := linux
LINUX_GOARCH := amd64

proto:
	protoc --go_out=. --go_opt=paths=source_relative \
		--go-grpc_out=. --go-grpc_opt=paths=source_relative \
		proto/helloworld.proto
	mkdir -p gen/helloworld/v1
	mv proto/helloworld.pb.go proto/helloworld_grpc.pb.go gen/helloworld/v1/

build: build-server build-client

build-server:
	mkdir -p $(BIN_DIR)
	go build -o $(BIN_DIR)/$(SERVER_BIN) ./cmd/server

build-client:
	mkdir -p $(BIN_DIR)
	go build -o $(BIN_DIR)/$(CLIENT_BIN) ./cmd/client

build-linux: build-linux-server build-linux-client

build-linux-server:
	mkdir -p $(BIN_DIR)
	GOOS=$(LINUX_GOOS) GOARCH=$(LINUX_GOARCH) go build -o $(BIN_DIR)/$(SERVER_BIN)-$(LINUX_GOOS)-$(LINUX_GOARCH) ./cmd/server

build-linux-client:
	mkdir -p $(BIN_DIR)
	GOOS=$(LINUX_GOOS) GOARCH=$(LINUX_GOARCH) go build -o $(BIN_DIR)/$(CLIENT_BIN)-$(LINUX_GOOS)-$(LINUX_GOARCH) ./cmd/client

run-server:
	go run ./cmd/server

run-client:
	go run ./cmd/client

tidy:
	go mod tidy

clean:
	rm -rf $(BIN_DIR)
