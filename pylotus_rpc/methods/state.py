
import json
from pylotus_rpc.types.BlockHeader import BlockHeader
from pylotus_rpc.types.BlockHeader import dict_to_blockheader


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
        # Iterate the block headers and parse them into BlockHeader objects
        lst_block_headers = []
        for dct_block_header in data["result"]["Blocks"]:
            block_header = dict_to_blockheader(dct_block_header)
            lst_block_headers.append(block_header)

        print(f"read {len(lst_block_headers)} block headers")
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")