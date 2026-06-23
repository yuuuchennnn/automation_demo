import configparser
import json

from loguru import logger
import requests
import os
import grpc
from google.protobuf import json_format
from grpc_reflection.v1alpha import reflection_pb2, reflection_pb2_grpc
from yagrc import reflector as yagrc_reflector


class FuncHub:
    """
        返回加载出的对应config.ini
    """
    @staticmethod
    def env(environment, rootdir=None):
        project_name = 'python_client'
        project_path = os.path.join(os.path.abspath(os.curdir).split(project_name)[0],
                                    project_name)

        path = project_path
        if rootdir:
            path = rootdir
        config_file = os.path.join(path,
                                   "configs",
                                   "config.ini")
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    @staticmethod
    def make_http_call(env):
        def make(app_url: str, api_path: str, method="post", body=None, headers=None, params=None) -> dict:
            base_url = env["HTTP"][app_url]
            url = base_url + api_path

            logger.info(f"HTTP {method} request {url} starts...")
            logger.info(f"body headers --> {str(headers)}")
            logger.info(f"body request --> {str(body)}")
            try:
                response = requests.request(method=method, url=url, json=body, headers=headers, params=params)
                logger.info(f"HTTP response --> {str(response)}")
                logger.info(f"HTTP response.json --> {str(response.json())}")

                res = {"status_code": response.status_code,
                       "json_resp": {}}
                if response.ok:
                    res["json_resp"] = response.json()
                    return res
                else:
                    return {"error_msg": f"HTTP request failed with status code {response.status_code}"}
            except requests.exceptions.HTTPError as err:
                logger.error(err.__str__())
                return {"error_msg": err.__str__()}
            except requests.exceptions.Timeout as err:
                logger.error(err.__str__())
                return {"error_msg": err.__str__()}
            except requests.exceptions.ConnectionError as err:
                logger.error(err.__str__())
                return {"error_msg": err.__str__()}
            except requests.exceptions.RequestException as err:
                return {"error_msg": err.__str__()}

        return make

    @staticmethod
    def _normalize_name(name):
        return ''.join(ch for ch in name.lower() if ch.isalnum())

    @staticmethod
    def _list_reflection_services(conn):
        stub = reflection_pb2_grpc.ServerReflectionStub(conn)
        request = reflection_pb2.ServerReflectionRequest(list_services="")
        response_stream = stub.ServerReflectionInfo(iter([request])) # type: ignore[attr-defined]
        for response in response_stream:
            return [service.name for service in response.list_services_response.service]
        return []

    @staticmethod
    def _service_matches(reflected_service_name, service_name):
        reflected_short_name = reflected_service_name.split('.')[-1]
        expected = FuncHub._normalize_name(service_name.split('.')[-1])
        actual = FuncHub._normalize_name(reflected_short_name)
        return (
            reflected_service_name == service_name
            or reflected_service_name.endswith(f".{service_name}")
            or actual == expected
            or actual == f"{expected}service"
        )

    @staticmethod
    def _load_service(conn, reflector, service_name):
        load_error = None
        service_name_candidates = ['.'.join(service_name.split('.')[index:])
                                   for index in range(len(service_name.split('.')))]
        for service_name_candidate in service_name_candidates:
            try:
                reflector.load_protocols(conn, symbols=[service_name_candidate])
                return service_name_candidate
            except Exception as err:
                load_error = err

        reflected_services = FuncHub._list_reflection_services(conn)
        service_matches_names = [name for name in reflected_services if FuncHub._service_matches(name, service_name)]
        if len(service_matches_names) == 1:
            reflector.load_protocols(conn, symbols=[service_matches_names[0]])
            return service_matches_names[0]
        if len(service_matches_names) > 1:
            raise ValueError(f"Multiple gRPC services match {service_name}: {service_matches_names}")

        raise load_error or ValueError(f"gRPC service not found: {service_name}")

    @staticmethod
    def _rpc_error_details(rpc_error):
        details = rpc_error.details()
        if not details:
            return ''
        try:
            return json.loads(details)
        except json.JSONDecodeError:
            return details

    @staticmethod
    def make_grpc_call(env, connections):
        def invoke(app_url: str, service_name: str, methodName: str, jsonReq):
            connection_info = env['GRPC'][app_url]
            reflector = yagrc_reflector.GrpcReflectionClient()

            if not (conn := connections.get(connection_info, None)):
                conn = grpc.insecure_channel(connection_info)
                connections[connection_info] = conn
            try:
                service_name = FuncHub._load_service(conn, reflector, service_name)
                # 获取客户端发送的数据
                stub_class = reflector.service_stub_class(service_name)
                method = reflector._engine.pool.FindMethodByName(service_name + '.' + methodName)
                request_name = method.input_type.full_name
                response_name = method.output_type.full_name
                request_class = reflector.message_class(request_name)
                reflector.message_class(response_name)
                # 生成 客户端通过客户端对象
                stub = stub_class(conn)
                # 通过客户端找出对应的方法
                method = getattr(stub, methodName)

                logger.info(f"GRPC call {methodName} starts...")
                logger.info(f"GRPC request -->\n{json.dumps(jsonReq, indent=4, sort_keys=True)}")

                # 执行方法
                response = method(request=json_format.ParseDict(jsonReq, request_class(), ignore_unknown_fields=True),
                                  timeout=3)
                res = json_format.MessageToDict(response, preserving_proto_field_name=True)
                logger.info(f"GRPC response -->\n{json.dumps(res, indent=4, sort_keys=True)}")
                return res
            except grpc.RpcError as rpc_error:
                if rpc_error.code() in [grpc.StatusCode.CANCELLED, grpc.StatusCode.UNAVAILABLE]:
                    logger.info(grpc.RpcError)
                    raise
                else:
                    error_info = {'code': rpc_error.code(),
                                  'msg': FuncHub._rpc_error_details(rpc_error)}
                    logger.info(error_info)
                    return error_info

        return invoke
