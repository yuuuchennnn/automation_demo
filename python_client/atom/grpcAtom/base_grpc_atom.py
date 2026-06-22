import inspect

class BaseGrpcAtom:

    @classmethod
    def grpc(cls, toolkits, json_req):
        
        grpccall = toolkits['grpc']
        module_suffix = cls.__module__.split('atom.grpcAtom.', 1)[-1]
        module_parts = module_suffix.split('.')
        serviceName = cls.__name__.split('GrpcAtom')[0]
        # 兼容grpcAtom下的子包，拼接serviceName
        packageName = '.'.join(module_parts[:-1])
        if packageName:
            serviceName = f"{packageName}.{serviceName}"
            
        frame = inspect.currentframe()
        caller = frame.f_back if frame is not None else None
        methodName = caller.f_code.co_name if caller is not None else ''
        
        url_key = serviceName.split('.')[-1]
        
        response = grpccall(url_key, serviceName, methodName, json_req)
        return response