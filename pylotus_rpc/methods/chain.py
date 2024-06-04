from typing import List
from ..http_json_rpc_connector import HttpJsonRpcConnector
from ..types.cid import Cid
from ..types.tip_set import Tipset
from ..types.block_header import BlockHeader
from ..types.block_messages import BlockMessages

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


def _get_genesis(connector: HttpJsonRpcConnector) -> Tipset:
    """
    Retrieves the genesis block of the Filecoin blockchain.

    This function sends a JSON-RPC request to the Filecoin network to retrieve the genesis block.
    The genesis block is the first block in the blockchain and serves as the starting point for the chain.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to
                                          send the JSON-RPC request.

    Returns:
        Tipset: An instance of `Tipset` representing the genesis block of the blockchain.
    """
    payload = _make_payload("Filecoin.ChainGetGenesis", None)
    data = connector.execute(payload, debug=True)
    genesis_tipset = Tipset.from_dict(data['result'])
    return genesis_tipset


def _delete_obj(connector: HttpJsonRpcConnector, cid: str) -> bool:
    """
    Attempts to remove the local copy of an object associated with a given CID from the Filecoin node. 
    Note that this operates on local node data and does not affect the data on the blockchain itself, which is immutable.

    This function sends a request to the dedicated Filecoin node to attempt the removal of the object's local copy using its CID (Content Identifier).    
    It is commonly used for managing node storage by clearing unneeded local data copies.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` that facilitates communication with the Filecoin node via JSON-RPC.  
        cid (str): The CID (Content Identifier) of the object whose local copy is to be removed. CIDs serve as unique identifiers for data in the Filecoin network.

    Returns:
        bool: True if the operation to delete the local copy was reported as successful by the node, otherwise False.

    """
    payload = _make_payload("Filecoin.ChainDeleteObj", Cid.format_cids_for_json([cid]))
    dct_result = connector.execute(payload, debug=True)

    if 'error' in dct_result:
        return False

    return True


def _export(connector: HttpJsonRpcConnector, chain_epoch: int, old_msg_skip: bool, tipset_key: str):
    """
    WARNING: this method exists as a stub, lotus currently does not support this via RPC (AFAIK)

    Export chain data from a given epoch to a given tipset key.  

    This function sends a JSON-RPC request to the Filecoin network to export chain data from a given epoch to a given tipset key.

    Args:
        chain_epoch (int): The epoch from which to start exporting chain data.
        old_msg_skip (bool): A boolean flag that indicates whether to skip old messages.
        tipset_key (str): The tipset key to which to export chain data.

    Returns:
        dict: A dictionary containing the exported chain data.
    """
    raise NotImplementedError("Currently, you cannot call this API directly. It requires a buffered output channel to dump the output.")


def _get_block_messages(connector: HttpJsonRpcConnector, block_cid: str) -> BlockMessages:
    """  
    Retrieves the messages in a block from the Filecoin blockchain using its CID.

    This function sends a JSON-RPC request to the Filecoin network to retrieve the messages
    in a specific block. It then converts the response into a `BlockMessages` object.

    Args:  
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to  
                                          send the JSON-RPC request.  
        block_cid (str): The CID (Content Identifier) of the block to be retrieved.

    Returns:
        BlockMessages: An instance of the `BlockMessages` class representing the messages in the block.

    Raises:
        Exception: If the JSON-RPC request fails or the response is invalid.
    """  
    payload = _make_payload("Filecoin.ChainGetBlockMessages", Cid.format_cids_for_json([block_cid]))  
    response = connector.execute(payload)  

    if 'result' not in response:
        raise Exception(f"Invalid response from JSON-RPC request: {response}")

    block_messages = BlockMessages.from_dict(response['result'])  
    return block_messages


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
    return Tipset.from_dict(result['result'])


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
    return Tipset.from_dict(dct_result["result"])


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
    return BlockHeader.from_dict(result)
