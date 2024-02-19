from typing import List
from ..http_json_rpc_connector import HttpJsonRpcConnector
from ..types.cid import Cid
from ..types.tip_set import Tipset
from ..types.block_header import BlockHeader, dict_to_blockheader

def _make_payload(method: str, params: List):
    """
    Internal utility method to generate a JSON-RPC payload for a given method and parameters.
    """
    if params: 
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
    else:
        payload = {
            "jsonrpc": "2.0",
            "method": method
        }

    return payload

# TODO - we don't have this tested and working yet and there isn't a clear reason why it's
# failing.  We will come back and revisit this later.
def _get_block_messages(connector: HttpJsonRpcConnector, block_cid: str) -> List[Cid]:
    """
    Retrieves the messages in a block from the Filecoin blockchain using its CID.

    This function sends a JSON-RPC request to the Filecoin network to retrieve the messages
    in a specific block. The messages are then converted into a list of `Cid` objects.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to
                                          send the JSON-RPC request.
        block_cid (str): The CID (Content Identifier) of the block to be retrieved.

    Returns:
        List[Cid]: A list of `Cid` objects representing the messages in the block.

    Example:
        >>> connector = HttpJsonRpcConnector('localhost', 1234, 'my_api_token')
        >>> block_cid = "bafy2bzaced..."
        >>> block_messages = _get_block_messages(connector, block_cid)
        >>> print(block_messages)
    """
    payload = _make_payload("Filecoin.ChainGetBlockMessages", Cid.format_cids_for_json([block_cid]))
    result = connector.execute(payload, debug=True)
    exit(0)
    return [Cid(cid["/"]) for cid in result['result']['Cids']]

def _get_tip_set(connector: HttpJsonRpcConnector, tipset_key: List[dict]) -> Tipset:
    """
    Retrieves a Tipset from the Filecoin blockchain using its key.

    This function sends a JSON-RPC request to the Filecoin network to retrieve a specific
    Tipset's information. The Tipset information is then converted into a `Tipset` object.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to
                                          send the JSON-RPC request.
        tipset_key (List[dict]): A list of dictionaries containing the CIDs of the blocks
                                 in the Tipset.

    Returns:
        Tipset: An instance of `Tipset` representing the retrieved Tipset.
    """
    payload = _make_payload("Filecoin.ChainGetTipSet", [tipset_key])
    result = connector.execute(payload)
    return Tipset(result['result']['Height'], [Cid(cid["/"]) for cid in result['result']['Cids']], [dict_to_blockheader(dct) for dct in result['result']['Blocks']])


def _read_obj(connector: HttpJsonRpcConnector, cid: str) -> str:
    """
    Retrieves the raw data associated with a given CID from the Filecoin blockchain.

    This function sends a request to the Filecoin network to fetch the raw data (in CBOR format) 
    represented by a specific CID (Content Identifier). The function is useful for accessing 
    various data structures on the Filecoin blockchain, such as actor states, messages, 
    block headers, etc.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` which handles 
                                          the communication with the Filecoin node via JSON-RPC.
        cid (str): The CID (Content Identifier) of the object to be retrieved. CIDs are unique 
                   identifiers for data in the Filecoin network.

    Returns:
        A string containing the raw data associated with the given CID. The data is 
        typically in CBOR (Concise Binary Object Representation) format and may require 
        further decoding and interpretation depending on its structure and context.
    """
    payload = _make_payload("Filecoin.ChainReadObj", Cid.format_cids_for_json([cid]))
    result = connector.execute(payload)
    return result['result']


def _get_chain_head(connector: HttpJsonRpcConnector) -> Tipset:
    """
    Retrieves the latest chain head from a Filecoin Lotus node.

    This method queries the Filecoin node for the latest head of the blockchain, which is a Tipset object that 
    contains the CIDs of the block headers at the current chain height.

    Parameters:
        connector (HttpJsonRpcConnector): The connector instance used to interface with the JSON RPC API of the Filecoin Lotus node.

    Returns:
        Tipset: An object representing the latest Tipset on the chain, which includes its height and the block headers.

    Raises:
        ApiCallError: If the RPC call fails, an ApiCallError is raised containing the error details.

    Examples:
        >>> current_chain_head = _get_chain_head(connector)
        >>> print(current_chain_head.height)
        >>> for header in current_chain_head.block_headers:
        ...     print(header.miner)
    """
    # JSON-RPC payload for requesting the chain head
    payload = _make_payload("Filecoin.ChainHead", None)
    dct_result = connector.execute(payload)

    # Parse the CIDs
    lst_cids = [Cid(cid["/"]) for cid in dct_result["result"]["Cids"]]

    # Parse block headers into BlockHeader objects
    lst_block_headers = [dict_to_blockheader(dct) for dct in dct_result["result"]["Blocks"]]
    height = dct_result["result"]["Height"]

    # construct and return a Tipset        
    return Tipset(height, lst_cids, lst_block_headers)


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
        "params": Cid.format_cids_for_json([cid])
    }

    result = connector.execute(payload, debug=False)["result"]
    return dict_to_blockheader(result)
