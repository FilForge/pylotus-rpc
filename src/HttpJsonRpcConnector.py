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

    def getChainHead(self):
        """
        Gets the chain head from the server.
        :return: The chain head.
        """

        # Lotus JSON-RPC endpoint
        URL = f"http://{self.host}:{self.port}/rpc/v0"

        # Headers
        HEADERS = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}"
        }

        # JSON-RPC payload
        payload = {
            "jsonrpc": "2.0",
            "method": "Filecoin.ChainHead",
            "id": 1
        }

        # Make the request
        response = requests.post(URL, headers=HEADERS, data=json.dumps(payload))

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
