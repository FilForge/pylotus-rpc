import requests
import json

class HttpJsonRpcConnector:
    """
    This class is responsible for the connection to the server via HTTP.
    """

    def __init__(self, host='localhost', port=1234, api_token=None):
        """
        Constructor of the class.
        :param host: The host of the server (default: 'localhost').
        :param port: The port of the server (default: 1234).
        :param api_token: The api token of the server (default: None).
        """
        self.host = host
        self.port = port
        self.api_token = api_token


    def get_request_headers(self):
        """
        Gets the request headers.
        :return: The request headers.
        """
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }
    
    def get_rpc_endpoint(self):
        """
        Gets the RPC endpoint.
        :return: The RPC endpoint.
        """
        return f"http://{self.host}:{self.port}/rpc/v0"
    
    def exec_method(self, payload):
        """
        Executes the method.
        :param payload: The payload.
        :return: The response.
        """
        response = requests.post(self.get_rpc_endpoint(), data=json.dumps(payload), headers=self.get_request_headers())
        return response

