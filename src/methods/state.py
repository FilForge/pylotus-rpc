
import json
import requests

def get_chain_head(self, connector):
    """
    Gets the chain head from the server.
    :return: The chain head.
    """
    # JSON-RPC payload
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.ChainHead",
        "id": 1
    }

    response = connector.exec_method(payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
