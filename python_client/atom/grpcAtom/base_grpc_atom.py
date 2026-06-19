import inspect

class BaseGrpcAtom:

    @classmethod
    def grpc(cls, toolkits, json_req):
        grpccall = toolkits['grpc']
        module_suffix = cls.__module__.split('atom.grpcAtom.', 1)[-1]
        module_parts = module_suffix.split('.')
        packageName = '.'.join(module_parts[:-1])
        serviceName = cls.__name__.split('GrpcAtom')[0]
        if packageName:
            serviceName = f"{packageName}.{serviceName}"
        methodName = inspect.currentframe().f_back.f_code.co_name
        url_key = serviceName.split('.')[-1]
        print(url_key, serviceName, methodName, json_req)
        response = grpccall(url_key, serviceName, methodName, json_req)
        return response