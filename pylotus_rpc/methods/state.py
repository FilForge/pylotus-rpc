from ..types.BlockHeader import BlockHeader, dict_to_blockheader
from ..types.Cid import Cid
from ..types.TipSet import Tipset

class ChainHeadRetrievalError(Exception):
    """
    Exception raised when there's an error retrieving the chain head.
    """
    def __init__(self, status_code, message):
        super().__init__(f"Failed to retrieve chain head. Status code: {status_code}. Message: {message}")
        self.status_code = status_code
        self.message = message

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

    response = connector.exec_method(payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Parse the CIDs
        lst_cids = [Cid(cid["/"]) for cid in data["result"]["Cids"]]

        # Parse block headers into BlockHeader objects
        lst_block_headers = [dict_to_blockheader(dct) for dct in data["result"]["Blocks"]]

        height = data["result"]["Height"]

        print(f"read {len(lst_cids)} cids")
        print(f"read {len(lst_block_headers)} block headers")
        print(f"height: {height}")

        return Tipset(height, lst_cids, lst_block_headers)
    else:
        raise ChainHeadRetrievalError(response.status_code, response.text)
