from atom.httpAtom.base_http_atom import BaseHttpAtom


class HttpDemoAtom(BaseHttpAtom):

    # for http_demo api
    @staticmethod
    def http_post_demo_atom(toolkits, headers=None, body=None):
        make_http_call = toolkits['http']
        path = "/demo"
        response = make_http_call("http_domain", path, method="post", body=body, headers=headers)
        
        return response

    @staticmethod
    def http_get_demo_atom(toolkits, headers=None, body=None):
        make_http_call = toolkits['http']
        path = "/demo"
        response = make_http_call("http_domain", path, method="get", headers=headers)
        
        return response
