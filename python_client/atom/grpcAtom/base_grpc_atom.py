import inspect

class BaseGrpcAtom:

    @classmethod
    def grpc(cls, toolkits, json_req):
        grpccall = toolkits['grpc']
        packageName = '.'.join(cls.__module__.split('atom.grpcAtom.')[1].split('.')[:-1])
        serviceName = cls.__name__.split('GrpcAtom')[0]
        serviceName = packageName + '.' + serviceName
        methodName = inspect.currentframe().f_back.f_code.co_name
        url_key = '.'.join(cls.__module__.split('.')[2:])
        print(url_key, serviceName, methodName,json_req)
        response = grpccall(url_key, serviceName, methodName, json_req)
        return response