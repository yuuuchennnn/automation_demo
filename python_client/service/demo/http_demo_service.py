from atom.httpAtom.demo_http_atom import HttpDemoAtom
from service.baseService import BaseService
from loguru import logger

class HttpDemoService(BaseService):
    def __init__(self, toolkits, testdata: dict):
        super().__init__()
        self.testdata = testdata
        self.toolkits = toolkits

    def call_demo_api(self):
        response = HttpDemoAtom.http_post_demo_atom(self.toolkits, headers=self.testdata['header'], body=self.testdata['body'])
        logger.debug(f" response: {response}")
        return response