import requests
import time
import json

class HttpJsonRpcConnector:
    """
    Connector class for HTTP-based JSON RPC communication.

    Attributes:
    - host: Host address of the RPC server.
    - port: Port on which the RPC server is listening.
    - api_token: Token for authenticating with the RPC server.
    """

    def __init__(self, host='localhost', port=1234, api_token=None):
        """
        Initializes an instance of the HttpJsonRpcConnector class.

        :param host: The server's hostname or IP address (default is 'localhost').
        :param port: The server's port (default is 1234).
        :param api_token: The API token for authentication (default is None).
        """
        self.host = host
        self.port = port
        self.api_token = api_token

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
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

    def get_rpc_endpoint(self) -> str:
        """
        Constructs the RPC endpoint URL.

        :return: The full RPC endpoint URL.
        """
        return f"http://{self.host}:{self.port}/rpc/v0"

    def exec_method(self, payload: dict) -> requests.Response:
        """
        Sends a JSON RPC request to the server with the provided payload.

        :param payload: Dictionary containing the RPC request details.
        :return: The server's response as a `requests.Response` object.
        """
        payload["id"] = self._generate_RPC_id()
        response = requests.post(
            self.get_rpc_endpoint(), 
            data=json.dumps(payload), 
            headers=self.get_request_headers()
        )
        return response

    def _generate_RPC_id(self) -> str:
        """
        Generates a unique RPC ID based on the current timestamp.

        :return: A string representation of the current timestamp.
        """
        return int(time.time() * 1000)
    
    @staticmethod
    def execute(connector: 'HttpJsonRpcConnector', payload: dict, debug=False) -> dict:
        """
        Execute a JSON RPC call using the given connector.

        This static method takes a connector instance, a payload for the RPC call, and an optional
        debug flag to output the request and response information. It sends the request and returns
        the parsed JSON response.

        Args:
            connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector, which holds
                                            the connection settings and methods to interact with
                                            the JSON RPC server.
            payload (dict): A dictionary representing the JSON RPC request payload.
            debug (bool, optional): If set to True, the method will print the payload and the response
                                    for debugging purposes. Defaults to False.

        Returns:
            dict: A dictionary parsed from the JSON response.

        Raises:
            ApiCallError: If there is any exception during the API call or if the response status
                        code is not 200.

        Example:
            >>> connector = HttpJsonRpcConnector('localhost', 1234, 'api_token_here')
            >>> payload = {"jsonrpc": "2.0", "method": "Filecoin.ChainHead", "params": []}
            >>> response = HttpJsonRpcConnector.execute(connector, payload)
            >>> print(response)

        Note:
            This method should be used with caution in production environments, especially when
            the debug flag is set to True, as it may expose sensitive information in the logs.
        """
        if debug:
            print(json.dumps(payload, indent=4))

        try:
            response = connector.exec_method(payload)
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
