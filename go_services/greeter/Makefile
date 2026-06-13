.PHONY: all check-go proto tidy setup build build-server build-client build-linux build-linux-server build-linux-client run-server run-client start-server start-server-bg stop-server clean

BIN_DIR := bin
SERVER_BIN := grpc-server
CLIENT_BIN := grpc-client
LINUX_GOOS := linux
LINUX_GOARCH := amd64
ADDR := :50051
SERVER_LOG := grpc-server.log
SERVER_PID := grpc-server.pid
PROTO_ROOT := ../../proto
PROTO_FILE := helloworld/v1/helloworld.proto

all: setup

check-go:
	@command -v go >/dev/null 2>&1 || { \
		echo "go is not installed or not in PATH"; \
		echo "install Go 1.22+ first, then run: make setup"; \
		exit 1; \
	}

proto: check-go
	protoc -I$(PROTO_ROOT) \
		--go_out=. --go_opt=paths=source_relative \
		--go-grpc_out=. --go-grpc_opt=paths=source_relative \
		$(PROTO_FILE)
	mkdir -p gen/helloworld/v1
	mv helloworld/v1/helloworld.pb.go helloworld/v1/helloworld_grpc.pb.go gen/helloworld/v1/
	rm -rf helloworld

setup: check-go tidy build

build: build-server build-client

build-server: check-go
	mkdir -p $(BIN_DIR)
	go build -o $(BIN_DIR)/$(SERVER_BIN) ./cmd/server

build-client: check-go
	mkdir -p $(BIN_DIR)
	go build -o $(BIN_DIR)/$(CLIENT_BIN) ./cmd/client

build-linux: build-linux-server build-linux-client

build-linux-server: check-go
	mkdir -p $(BIN_DIR)
	GOOS=$(LINUX_GOOS) GOARCH=$(LINUX_GOARCH) go build -o $(BIN_DIR)/$(SERVER_BIN)-$(LINUX_GOOS)-$(LINUX_GOARCH) ./cmd/server

build-linux-client: check-go
	mkdir -p $(BIN_DIR)
	GOOS=$(LINUX_GOOS) GOARCH=$(LINUX_GOARCH) go build -o $(BIN_DIR)/$(CLIENT_BIN)-$(LINUX_GOOS)-$(LINUX_GOARCH) ./cmd/client

run-server: check-go
	go run ./cmd/server

run-client: check-go
	go run ./cmd/client

start-server: build-server
	./$(BIN_DIR)/$(SERVER_BIN) -addr $(ADDR)

start-server-bg: build-server
	nohup ./$(BIN_DIR)/$(SERVER_BIN) -addr $(ADDR) > $(SERVER_LOG) 2>&1 & echo $$! > $(SERVER_PID)
	@echo "server started, pid=$$(cat $(SERVER_PID)), log=$(SERVER_LOG), addr=$(ADDR)"

stop-server:
	@if [ -f $(SERVER_PID) ]; then \
		kill $$(cat $(SERVER_PID)); \
		rm -f $(SERVER_PID); \
		echo "server stopped"; \
	else \
		echo "$(SERVER_PID) not found"; \
	fi

tidy: check-go
	go mod tidy

clean:
	rm -rf $(BIN_DIR) $(SERVER_PID) $(SERVER_LOG)
