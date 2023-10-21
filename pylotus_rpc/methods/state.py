from ..types.BlockHeader import BlockHeader, dict_to_blockheader
from ..types.Cid import Cid
from ..types.TipSet import Tipset
from ..types.Actor import Actor
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

