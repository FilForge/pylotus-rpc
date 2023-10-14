
import json
from ..types.BlockHeader import BlockHeader
from ..types.BlockHeader import dict_to_blockheader
from ..types.Cid import Cid
from ..types.TipSet import Tipset  

def _get_chain_head(connector):
    """
    Gets the chain head from the server.
    :return: The chain head.
    """
    # JSON-RPC payload
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.ChainHead",
    }

    response = connector.exec_method(payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # iterate and parse the cids
        lst_cids = []
        for cid in data["result"]["Cids"]:
            lst_cids.append(Cid(cid["/"]))
        # Iterate the block headers and parse them into BlockHeader objects
        lst_block_headers = []
        for dct_block_header in data["result"]["Blocks"]:
            block_header = dict_to_blockheader(dct_block_header)
            lst_block_headers.append(block_header)

        height = data["result"]["Height"]

        print(f"read {len(lst_cids)} cids")
        print(f"read {len(lst_block_headers)} block headers")
        print(f"height: {height}")

        return Tipset(height, lst_cids, lst_block_headers)
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")