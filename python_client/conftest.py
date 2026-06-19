import logging

import pytest
from loguru import logger


class PropagateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.remove()
logger.add(PropagateHandler(), format="{message}", level="DEBUG")
logging.getLogger("urllib3").setLevel(logging.WARNING)

from functions.func_hub import FuncHub

def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     dest="environment",
                     default="test",
                     help="environment: test or stage")

'''
    返回加载的config.ini
'''
@pytest.fixture(scope="session")
def env(request):
    rootdir = request.config.rootdir
    environment = request.config.getoption("environment")
    return FuncHub.env(environment,rootdir)

@pytest.fixture(scope="session")
def make_http_call(env):
    http_call = FuncHub.make_http_call(env)
    return http_call

@pytest.fixture(scope='session')
def make_grpc_call(request, env):
    connections = {}
    invoke = FuncHub.make_grpc_call(env, connections)

    def cleanup():
        while connections:
            connections.popitem()[1].close()

    request.addfinalizer(cleanup)
    return invoke

@pytest.fixture(scope='session')
def toolkits(env, make_http_call, make_grpc_call):
    tools = {'env': env,
             'http': make_http_call,
             'grpc': make_grpc_call
             }
    return tools


if __name__ == '__main__':
    pass
