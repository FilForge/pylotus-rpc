from ..HttpJsonRpcConnector import HttpJsonRpcConnector
from ..types.Cid import Cid
from ..types.BlockHeader import BlockHeader, dict_to_blockheader
import os

def _get_block(connector: HttpJsonRpcConnector, cid: str) -> BlockHeader:
    """
    Retrieves a block from the Filecoin blockchain using its CID.

    This function sends a JSON-RPC request to the Filecoin network to retrieve a specific
    block's information. The block information is then converted into a `BlockHeader` object.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to
                                          send the JSON-RPC request.
        cid (str): The CID (Content Identifier) of the block to be retrieved.

    Returns:
        BlockHeader: An instance of `BlockHeader` representing the retrieved block.

    Example:
        >>> connector = HttpJsonRpcConnector('localhost', 1234, 'my_api_token')
        >>> block_cid = "bafy2bzaced..."
        >>> block_header = _get_block(connector, block_cid)
        >>> print(block_header)

    Note:
        The `debug` parameter is set to `True`, which will print the JSON-RPC request and
        response payload to stdout. Set this to `False` in production environments to avoid
        leaking sensitive information.
    """
    
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.ChainGetBlock",
        "params": Cid.dct_cids([cid])
    }

    result = connector.execute(connector, payload, debug=False)["result"]
    return dict_to_blockheader(result)
