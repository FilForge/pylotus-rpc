from typing import List, Dict, Optional
from ..http_json_rpc_connector import HttpJsonRpcConnector
from ..types.cid import Cid
from ..types.tip_set import Tipset
from ..types.block_header import BlockHeader
from ..types.block_messages import BlockMessages
from ..types.message import Message
from ..types.wrapped_message import WrappedMessage
from ..types.message_receipt import MessageReceipt
from ..types.head_change import HeadChange

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


def _chain_notify(connector: HttpJsonRpcConnector) -> Dict:
    """
    This function is intended to notify about changes in the blockchain. However, it is not
    currently implemented because it requires a buffered output channel to dump the output.  Calling this
    method on a lotus RPC node will return a 500 error.

    Args:
        connector (HttpJsonRpcConnector): The connector used to communicate with the Filecoin node via JSON-RPC.

    Returns:
        Dict: A dictionary representing the notification about changes in the blockchain.

    Raises:
        NotImplementedError: Always raised because this function is not implemented.
    """
    raise NotImplementedError("Currently, you cannot call this API directly. It requires a buffered output channel to dump the output.")


def _has_obj(connector: HttpJsonRpcConnector, cid: str) -> bool:
    """
    Determines whether a specific object exists in the Filecoin node's local storage.

    This method sends a JSON-RPC request to the Filecoin node to check if the object
    identified by the given CID (Content Identifier) is present in the node's local storage.

    Args:
        connector (HttpJsonRpcConnector): The connector used to communicate with the Filecoin node via JSON-RPC.
        cid (str): The Content Identifier (CID) of the object to verify.

    Returns:
        bool: 
            - `True` if the object exists in the local storage.
            - `False` if the object does not exist.

    Raises:
        ApiCallError: If the JSON-RPC request fails due to network issues or invalid responses.
    """
    payload = _make_payload("Filecoin.ChainHasObj", Cid.format_cids_for_json([cid]))
    response = connector.execute(payload)
    return response['result']


def _get_randomness_from_tickets(
        connector: HttpJsonRpcConnector, 
        domain_tag: int, 
        epoch: int, 
        entropy_base64: str, 
        tipset: Tipset) -> str:
    """
    Retrieves randomness from the Filecoin tickets for a specific epoch.

    This function sends a request to the Filecoin network to get randomness from the tickets
    for a given epoch, domain tag, and entropy. It's used in various parts of the Filecoin
    protocol that require verifiable randomness.

    Args:
        connector (HttpJsonRpcConnector): The connector to send the JSON-RPC request.
        domain_tag (int): An integer representing the domain separation tag.
        epoch (int): The epoch for which to retrieve the randomness.
        entropy_base64 (str): Additional entropy as a base64-encoded string.
        tipset (Tipset): The tipset to use as a reference.

    Returns:
        str: A string representing the retrieved randomness.
    """
    tipset_key = tipset.get_tip_set_key() if tipset else None
    payload = _make_payload("Filecoin.ChainGetRandomnessFromTickets", [tipset_key, domain_tag, epoch, entropy_base64])
    response = connector.execute(payload)
    return response['result']


def _get_randomness_from_beacon(
        connector: HttpJsonRpcConnector, 
        domain_tag: int, 
        epoch: int, 
        entropy_base64: str, 
        tipset: Optional[Tipset] = None) -> str:
    """
    Retrieves randomness from the Filecoin beacon for a specific epoch.

    This function sends a request to the Filecoin network to get randomness from the beacon
    for a given epoch, domain tag, and entropy. It's used in various parts of the Filecoin
    protocol that require verifiable randomness.

    Args:
        connector (HttpJsonRpcConnector): The connector to send the JSON-RPC request.
        domain_tag (int): An integer representing the domain separation tag.
        epoch (int): The epoch for which to retrieve the randomness.
        entropy_base64 (str): Additional entropy as a base64-encoded string.
        tipset (Optional[Tipset]): The tipset to use as a reference. If None, the current
                                   chain head will be used.

    Returns:
        str: A string representing the retrieved randomness.
    """
    tipset_key = tipset.get_tip_set_key() if tipset else []
    payload = _make_payload("Filecoin.ChainGetRandomnessFromBeacon", [ tipset_key, domain_tag, epoch, entropy_base64])
    response = connector.execute(payload)
    return response['result']


def _get_tipset_by_height(connector: HttpJsonRpcConnector, height: int, tipset_key: List[dict] = None) -> List[HeadChange]:
    """
    Retrieve the TipSet at a specific height from the Filecoin blockchain.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to use for the API call.
        height (int): The specific height for which to retrieve the TipSet.
        tipset_key (List[dict], optional): The key of the TipSet to consider if you want the TipSet at the height
                                           X considering the state from this TipSet. Defaults to None.

    Returns:
        Tipset: The TipSet object at the specified height.
    """
    payload = _make_payload("Filecoin.ChainGetTipSetByHeight", [height, tipset_key])
    result = connector.execute(payload)
    return Tipset.from_dict(result['result'])


def _get_path(connector: HttpJsonRpcConnector, start_tipset_key: List[dict], end_tipset_key: List[dict]) -> Dict:
    """
    Retrieves the path between two tipsets in the Filecoin blockchain.

    This function sends a JSON-RPC request to the Filecoin network to retrieve the path between two tipsets.
    The path is represented as a list of tipsets and messages.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to
                                          send the JSON-RPC request.
        start_tipset_key (List[dict]): A list of dictionaries containing the CIDs of the blocks
                                       in the starting tipset.
        end_tipset_key (List[dict]): A list of dictionaries containing the CIDs of the blocks
                                     in the ending tipset.

    Returns:
        Dict: A dictionary containing the path between the two tipsets.

    Raises:
        Exception: If the JSON-RPC request fails or the response is invalid.
    """
    payload = _make_payload("Filecoin.ChainGetPath", [start_tipset_key, end_tipset_key])
    response = connector.execute(payload)

    if 'result' not in response:
        raise Exception(f"Invalid response from JSON-RPC request: {response}")

    head_changes = []
    for dct_headchange in response['result']:
        head_change = HeadChange.from_dict(dct_headchange)
        head_changes.append(head_change)

    return head_changes


def _get_parent_receipts(connector: HttpJsonRpcConnector, block_cid: str) -> List[MessageReceipt]:
    """
    Retrieves the parent receipts of a Filecoin block using the given CID.

    This function leverages the Filecoin JSON-RPC API to fetch the parent 
    receipts associated with a specified block CID. 

    Parameters:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` to 
            communicate with the Filecoin node.
        block_cid (str): The CID of the block whose parent receipts are to be fetched.

    Returns:
        List[MessageReceipt]: A list of `MessageReceipt` instances
    """
    payload = _make_payload("Filecoin.ChainGetParentReceipts", Cid.format_cids_for_json([block_cid]))
    response = connector.execute(payload)
    receipts = []

    for dct_message_receipt in response['result']:
        receipt = MessageReceipt.from_dict(dct_message_receipt)
        receipts.append(receipt)

    return receipts

def _get_parent_messages(connector: HttpJsonRpcConnector, block_cid: str) -> List[WrappedMessage]:
    """
    Retrieves the parent messages of a Filecoin block using the given CID.

    This function leverages the Filecoin JSON-RPC API to fetch the parent 
    messages associated with a specified block CID. Each parent message is 
    wrapped with its corresponding CID.

    Parameters:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` to 
            communicate with the Filecoin node.
        block_cid (str): The CID of the block whose parent messages are to be fetched.

    Returns:
        List[WrappedMessage]: A list of `WrappedMessage` instances, each containing a parent 
        message and its corresponding CID.
    """
    payload = _make_payload("Filecoin.ChainGetParentMessages", Cid.format_cids_for_json([block_cid]))
    response = connector.execute(payload)
    wrapped_messages = []

    for dct in response['result']:
        message = Message.from_dict(dct['Message'])
        cid = Cid.from_dict(dct['Cid'])
        wrapped_messages.append(WrappedMessage(message, cid))

    return wrapped_messages


def _get_node(connector: HttpJsonRpcConnector, node_path_selector: str) -> dict:
    """
    Fetches specific node data from the Filecoin blockchain using the ChainGetNode RPC method.

    This function sends a request to the Filecoin blockchain node to retrieve data at a specified path.
    The path is defined by the `node_path_selector` parameter. It utilizes the `HttpJsonRpcConnector` 
    to execute the RPC call.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector to communicate with the Filecoin node.
        node_path_selector (str): The path selector string specifying the node's data to be retrieved.

    Returns:
        dict: The data retrieved from the specified node, as a dictionary.

    Raises:
        KeyError: If the 'result' key is not found in the response.
        ConnectionError: If there is a problem with the RPC connection.
    """
    payload = _make_payload("Filecoin.ChainGetNode", [node_path_selector])
    response = connector.execute(payload)
    node_data = response['result']
    return node_data


def _get_messages_in_tipset(connector: HttpJsonRpcConnector, tipset_key: List[dict]) -> List[Message]:
    """
    Retrieves messages in a Tipset from the Filecoin blockchain using its key.

    This function sends a JSON-RPC request to the Filecoin network to retrieve the messages
    in a specific Tipset. The messages are then converted into a list of `Message` objects.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to
                                          send the JSON-RPC request.
        tipset_key (List[dict]): A list of dictionaries containing the CIDs of the blocks
                                 in the Tipset.

    Returns:
        List[Message]: A list of `Message` objects representing the messages in the Tipset.
    """
    payload = _make_payload("Filecoin.ChainGetMessagesInTipset", [tipset_key])
    result = connector.execute(payload)
    messages = []
    for dct in result['result']:
        messages.append(Message.from_dict(dct['Message']))

    return messages


def _get_message(connector: HttpJsonRpcConnector, cid: str) -> Message:
    """
    Retrieves a message from the Filecoin blockchain using its CID.

    This function sends a JSON-RPC request to the Filecoin network to retrieve a specific
    message. The message information is then converted into a `Message` object.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to
                                          send the JSON-RPC request.
        cid (str): The CID (Content Identifier) of the message to be retrieved.

    Returns:
        Message: An instance of `Message` representing the retrieved message.
    """
    payload = _make_payload("Filecoin.ChainGetMessage", Cid.format_cids_for_json([cid]))
    result = connector.execute(payload)
    return Message.from_dict(result['result'])


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
