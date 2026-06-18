import configparser

from loguru import logger
import requests
import os
import grpc
from google.protobuf import json_format

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
            logger.info("\n")
            logger.info(f"HTTP {method} request {url} starts...")
            logger.info(f"body headers -->\n{str(headers)}")
            logger.info(f"body request -->\n{str(body)}")
            try:
                response = requests.request(method=method, url=url, json=body, headers=headers, params=params)
                logger.info(f"HTTP response -->\n{str(response)}")
                logger.info(f"HTTP response.json -->\n{str(response.json())}")

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
            except requests.exceptions.Timeout:
                logger.error("Timeout requesting")
                return {"error_msg": "request timeout"}
            except requests.exceptions.ConnectionError:
                logger.error("Connection Error")
                return {"error_msg": "connection error"}
            except requests.exceptions.RequestException as err:
                return {"error_msg": err.__str__()}

        return make

    @staticmethod
    def make_grpc_call(env, connections):
        def invoke_grpc(grpcInfo, methodName: str, grpcRequest, responseType, metadata, needSign=False):

            app_url = grpcInfo.value[0]
            stub_name = grpcInfo.value[1]
            connection_info = env['GRPC'][app_url]

            if not (conn := connections.get(connection_info, None)):
                conn = grpc.insecure_channel(connection_info)
                connections[connection_info] = conn

            stub = stub_name(channel=conn)
            func = getattr(stub, methodName)
            logger.info(f"GRPC call {methodName} starts...")
            logger.info(f"grpc request -->\n{str(grpcRequest)}")
            if needSign:
                metadata = FuncHub.make_sign(metadata)

            try:
                response = func(grpcRequest, metadata=metadata)
                logger.info(f"grpc response -->\n{str(response)}")
                return json_format.MessageToDict(response, responseType,preserving_proto_field_name=True)

            except grpc.RpcError as rpc_error:
                if rpc_error.code() in [grpc.StatusCode.CANCELLED, grpc.StatusCode.UNAVAILABLE]:
                    logger.info(grpc.RpcError)
                    raise grpc.RpcError
                else:
                    error_info = {'code': rpc_error.code(), 'msg': rpc_error.details()}
                    logger.info(error_info)
                    return error_info  # '{"status":400,"ret_code":400001,"grpc_code":3,"ret_msg":"invalid spot airdrop value","details":null}'

        return invoke_grpc