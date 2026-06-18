from atom.httpAtom.base_http_atom import BaseHttpAtom


class DemoHttpAtom(BaseHttpAtom):
    def __init__(self, toolkits, testData: dict):
        super().__init__(toolkits, testData)


    @staticmethod
    def demo_http_atom(toolkits, headers=None, body=None):
        make_http_call = toolkits['http']
        path = "/demo"
        response = make_http_call("http_domain", path, method="post", body=body, headers=headers)
        
        return response

