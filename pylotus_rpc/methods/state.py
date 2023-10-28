from typing import Optional
from ..HttpJsonRpcConnector import HttpJsonRpcConnector
from ..types.BlockHeader import BlockHeader, dict_to_blockheader
from ..types.Cid import Cid
from ..types.Message import Message
from ..types.TipSet import Tipset
from ..types.Actor import Actor
from ..types.InvocationResult import InvocationResult
import json

class ApiCallError(Exception):
    """
    Exception raised when there's an error during an API call.
    """
    def __init__(self, method_name: str, status_code: int, message: str):
        super().__init__(f"Failed API call '{method_name}'. Status code: {status_code}. Message: {message}")
        self.method_name = method_name
        self.status_code = status_code
        self.message = message


def _state_call(connector: HttpJsonRpcConnector, 
                message: Message, 
                tipset: Optional[Tipset] = None) -> InvocationResult:  

    # JSON-RPC payload for requesting the account key
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateCall",
        "params": [
            message.to_json(),
            tipset.dct_cids() if tipset else None,
        ]
    }

    pretty_json = json.dumps(payload, indent=4, sort_keys=True)
    print(pretty_json)
    
    try:
        response = connector.exec_method(payload)
    except Exception as e:
        raise ApiCallError("Filecoin.StateCall", 0, str(e))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        invocation_result = InvocationResult.from_json(response.json())
        return invocation_result
    else:
        raise ApiCallError("Filecoin.StateAccountKey", response.status_code, response.text)


     
def _account_key(connector, address, tipset=None):
    """
    Retrieves the account key for the given address.

    :param connector: The HTTP JSON-RPC connector object to communicate with the server.
    :param address: The address to retrieve the account key for.
    :param tipset: The tipset to retrieve the account key at. If None, the chain head is used.
    :return: The account key for the given address.
    :raises ApiCallError: If there's an error during the API call.
    """
    # JSON-RPC payload for requesting the account key
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateAccountKey",
        "params": [
            address,
            tipset.dct_cids() if tipset else None,
        ]
    }

    try:
        response = connector.exec_method(payload)
    except Exception as e:
        raise ApiCallError("Filecoin.StateAccountKey", 0, str(e))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Parse the account key
        address = Cid(data["result"])

        return address
    else:
        raise ApiCallError("Filecoin.StateAccountKey", response.status_code, response.text)
    

def _get_actor(connector, actor_id, tipset=None):

    cids = None
    if tipset:
        cids = tipset.dct_cids()

    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateGetActor",
        "params": [
            actor_id,
            cids,
        ],
    }

    try:
        response = connector.exec_method(payload)
    except Exception as e:
        raise ApiCallError("Filecoin.StateGetActor", 0, str(e))

    if response.status_code == 200:
        # Parse the response into a Python dictionary
        data = response.json()

        # Extract the result section which contains the Actor details
        actor_data = data['result']

        # Create Actor object using parsed data
        actor = Actor(
            Code=Cid(actor_data['Code']['/']),
            Head=Cid(actor_data['Head']['/']),
            Nonce=actor_data['Nonce'],
            Balance=actor_data['Balance'])

        return actor
    else:
        raise ApiCallError("Filecoin.StateGetActor", response.status_code, response.text)



# WARNING: This method takes an exceptionally long time to complete.
def _list_state_actors(connector, tipset):
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateListActors",
        "params": [
            tipset.dct_cids(),
        ]
    }

    try:
        response = connector.exec_method(payload)
    except Exception as e:
        raise ApiCallError("Filecoin.StateListActors", 0, str(e))

    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        raise ApiCallError("Filecoin.StateListActors", response.status_code, response.text)


def _get_chain_head(connector):
    """
    Retrieves the chain head from the server.

    :param connector: The HTTP JSON-RPC connector object to communicate with the server.
    :return: A Tipset object representing the chain head.
    :raises ChainHeadRetrievalError: If there's an error retrieving the chain head.
    """
    # JSON-RPC payload for requesting the chain head
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.ChainHead",
    }

    try:
        response = connector.exec_method(payload)
    except Exception as e:
        raise ApiCallError("Filecoin.ChainHead", 0, str(e))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Parse the CIDs
        lst_cids = [Cid(cid["/"]) for cid in data["result"]["Cids"]]

        # Parse block headers into BlockHeader objects
        lst_block_headers = [dict_to_blockheader(dct) for dct in data["result"]["Blocks"]]

        height = data["result"]["Height"]
        
        return Tipset(height, lst_cids, lst_block_headers)
    else:
        raise ApiCallError("Filecoin.ChainHead", response.status_code, response.text)

