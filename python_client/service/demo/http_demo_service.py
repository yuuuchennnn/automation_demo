from atom.httpAtom.demo_http_atom import DemoHttpAtom
from service.baseService import BaseService
from loguru import logger

class HttoDemoService(BaseService):
    def __init__(self, toolkits, testData: dict):
        super().__init__()
        self.testData = testData
        self.toolkits = toolkits

    def call_demo_http(self):
        response = DemoHttpAtom.demo_http_atom(self.toolkits, headers=self.testData['header'], body=self.testData['body'])
        logger.debug(f" response: {response}")
        return response