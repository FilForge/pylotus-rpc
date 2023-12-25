import requests
import time
import json
from typing import List, Optional
from .types.tip_set import Tipset
from urllib.parse import urlparse


class HttpJsonRpcConnector:
    def __init__(self, host='http://localhost/rpc/v0', port=None, api_token=None):
        """
        Initializes an instance of the HttpJsonRpcConnector class.

        :param host: The server's hostname or IP address (default is 'localhost').
        :param port: The server's port (default is None).
        :param api_token: The API token for authentication (default is None).
        """
        # Parse the host to get the scheme and path
        parsed_url = urlparse(host)
        
        self.scheme = parsed_url.scheme
        self.path = parsed_url.path

        # If the port is not specified, we will try to use the one from the parsed URL.
        # If the parsed URL doesn't have one either, we will default to None.
        self.port = port if port is not None else parsed_url.port

        # If the host includes a netloc (network location part), use it.
        # Otherwise, fall back to the host parameter.
        self.host = parsed_url.netloc.split(':')[0] if parsed_url.netloc else host

        self.api_token = api_token

        # Ensure that the path starts with '/' if it's not empty.
        if self.path and not self.path.startswith('/'):
            self.path = '/' + self.path


    class ApiCallError(Exception):
        """
        Exception raised when there's an error during an API call.
        """
        def __init__(self, method_name: str, status_code: int, message: str):
            super().__init__(f"Failed API call '{method_name}'. Status code: {status_code}. Message: {message}")
            self.method_name = method_name
            self.status_code = status_code
            self.message = message

    
    def get_request_headers(self) -> dict:
        """
        Constructs the headers required for the JSON RPC request.

        :return: Dictionary containing the request headers.
        """
        headers = {"Content-Type": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers


    def get_rpc_endpoint(self) -> str:
        """
        Constructs the RPC endpoint URL.

        If a port is defined, it includes the port number in the endpoint URL,
        otherwise, it only uses the host for the URL.

        :return: The full RPC endpoint URL.
        """
        endpoint = f"{self.scheme}://{self.host}"
        if self.port:
            endpoint += f":{self.port}"
        endpoint += self.path

        return endpoint


    def exec_method(self, payload: dict, debug=False) -> requests.Response:
        """
        Sends a JSON RPC request to the server with the provided payload.

        :param payload: Dictionary containing the RPC request details.
        :return: The server's response as a `requests.Response` object.
        """
        payload["id"] = self._generate_RPC_id()

        if debug:
            print(f"using endpoint {self.get_rpc_endpoint()}")

        response = requests.post(
            self.get_rpc_endpoint(), 
            data=json.dumps(payload), 
            headers=self.get_request_headers(),
            timeout=300
        )
        return response

    def _generate_RPC_id(self) -> str:
        """
        Generates a unique RPC ID based on the current timestamp.

        :return: A string representation of the current timestamp.
        """
        return int(time.time() * 1000)
    
    def execute(self, payload: dict, debug=False) -> dict:
        """
        Executes a JSON RPC request using the specified payload and returns the response.

        This method serves as a high-level interface to `exec_method`, handling exceptions,
        debugging output, and response validation. It raises an ApiCallError if the request
        fails or if the server returns a non-200 status code.

        :param payload: A dictionary containing the JSON RPC request payload. The payload
                        should include at least the 'method' name and the 'params' for the request.
        :param debug: A boolean flag that, when set to True, enables the printing of debug
                      information like the request payload and response.
        :return: A dictionary containing the parsed JSON response from the server.
        :raises: ApiCallError if there's an error in making the API call or if the response
                 status code is not 200.
        """
        if debug:
            print(json.dumps(payload, indent=4))

        try:
            response = self.exec_method(payload, debug=debug)
        except Exception as e:
            raise HttpJsonRpcConnector.ApiCallError(payload["method"], 0, str(e))

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            if debug:
                print(json.dumps(response.json(), indent=4))

            return response.json()
        else:
            raise HttpJsonRpcConnector.ApiCallError(payload['method'], response.status_code, response.text)





