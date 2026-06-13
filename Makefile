.PHONY: go-setup go-build go-start go-start-bg go-stop python-setup python-proto python-test python-client clean

GO_SERVER_DIR := go-server
PYTHON_CLIENT_DIR := python-client
SERVER_ADDR := :50051
PYTHON_ADDR := 127.0.0.1:50051
NAME := Yuchen
PYTHON := python3
VENV_DIR := $(PYTHON_CLIENT_DIR)/.venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip

go-setup:
	$(MAKE) -C $(GO_SERVER_DIR) setup

go-build:
	$(MAKE) -C $(GO_SERVER_DIR) build-server

go-start:
	$(MAKE) -C $(GO_SERVER_DIR) start-server ADDR=$(SERVER_ADDR)

go-start-bg:
	$(MAKE) -C $(GO_SERVER_DIR) start-server-bg ADDR=$(SERVER_ADDR)

go-stop:
	$(MAKE) -C $(GO_SERVER_DIR) stop-server

python-setup:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PIP) install -r $(PYTHON_CLIENT_DIR)/requirements.txt

python-proto:
	$(VENV_PYTHON) -m grpc_tools.protoc \
		-I$(GO_SERVER_DIR) \
		--python_out=$(PYTHON_CLIENT_DIR) \
		--grpc_python_out=$(PYTHON_CLIENT_DIR) \
		$(GO_SERVER_DIR)/proto/helloworld.proto

python-test:
	GRPC_ADDR=$(PYTHON_ADDR) $(VENV_PYTHON) -m pytest $(PYTHON_CLIENT_DIR)

python-client:
	$(VENV_PYTHON) $(PYTHON_CLIENT_DIR)/client.py --addr $(PYTHON_ADDR) --name $(NAME)

clean:
	$(MAKE) -C $(GO_SERVER_DIR) clean
	rm -rf $(VENV_DIR)
