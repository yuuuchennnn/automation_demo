.PHONY: all setup reinstall test test-api test-selenium run clean

PYTHON := python3
VENV_DIR := .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
ADDR := 127.0.0.1:50051
NAME := Yuchen

all: setup

setup:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PYTHON) -m ensurepip --upgrade
	$(VENV_PYTHON) -m pip install -r requirements.txt

reinstall: clean setup

test:
	GRPC_ADDR=$(ADDR) $(VENV_PYTHON) -m pytest .

test-api:
	GRPC_ADDR=$(ADDR) $(VENV_PYTHON) -m pytest TestCase/Test_Demo -v

test-selenium:
	$(VENV_PYTHON) -m pytest TestCase/TC_Selenium -m ui_selenium -v

run:
	$(VENV_PYTHON) client.py --addr $(ADDR) --name $(NAME)

clean:
	rm -rf $(VENV_DIR)
