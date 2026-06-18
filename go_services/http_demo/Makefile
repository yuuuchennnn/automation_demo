.PHONY: all check-go tidy build build-linux start-server start-server-bg stop-server clean

BIN_DIR := bin
SERVER_BIN := http-demo-server
LINUX_GOOS := linux
LINUX_GOARCH := amd64
ADDR := :8080
SERVER_LOG := http-demo-server.log
SERVER_PID := http-demo-server.pid

all: setup

check-go:
	@command -v go >/dev/null 2>&1 || { \
		echo "go is not installed or not in PATH"; \
		echo "install Go 1.22+ first, then run: make setup"; \
		exit 1; \
	}

setup: check-go tidy build

build: check-go
	mkdir -p $(BIN_DIR)
	go build -o $(BIN_DIR)/$(SERVER_BIN) ./cmd/server

build-linux: check-go
	mkdir -p $(BIN_DIR)
	GOOS=$(LINUX_GOOS) GOARCH=$(LINUX_GOARCH) go build -o $(BIN_DIR)/$(SERVER_BIN)-$(LINUX_GOOS)-$(LINUX_GOARCH) ./cmd/server

start-server: build
	./$(BIN_DIR)/$(SERVER_BIN) -addr $(ADDR)

start-server-bg: build
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
