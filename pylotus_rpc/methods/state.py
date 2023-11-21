from typing import Optional, List
from ..HttpJsonRpcConnector import HttpJsonRpcConnector
from ..types.BlockHeader import BlockHeader, dict_to_blockheader
from ..types.Cid import Cid
from ..types.Message import Message
from ..types.TipSet import Tipset
from ..types.Actor import Actor
from ..types.StateComputeOutput import StateComputeOutput
from ..types.InvocationResult import InvocationResult
import json


def _decode_params(connector: HttpJsonRpcConnector, actor_cid: str, method: int, params: str, tipset: Optional[Tipset] = None):
    """
    Decodes the parameters of a message for a given actor and method into a human-readable format.

    This function is useful for understanding the data passed in transactions, especially those interacting with smart contracts.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to send the JSON-RPC request.
        actor_cid (str): The CID (Content Identifier) of the actor (smart contract) for which the message was intended.
        method (int): The method number on the actor the message is calling.
        params (str): The encoded parameters to be decoded. This is usually a base64 encoded string.
        tipset (Optional[Tipset]): The tipset at which to perform the decoding. If None, the latest tipset is used.

    Returns:
        A dictionary representing the decoded parameters in a human-readable format. If the decoding fails, an empty dictionary is returned.

    """

    cids = tipset.dct_cids() if tipset else None

    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateDecodeParams",
        "params": [actor_cid, method, params, cids]
    }

    response = connector.execute(payload)
    return response.get("result", {})


def _deal_provider_collateral_bounds(connector: HttpJsonRpcConnector, padded_piece_size : int, is_verified : bool, tipset: Optional[Tipset]):
    """
    Retrieves the minimum and maximum collateral bounds for a storage provider based on the given piece size and verification status.

    This function queries the Filecoin network using the StateDealProviderCollateralBounds method to determine the range of collateral a storage provider is expected to lock for a given deal size.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        padded_piece_size (int): The size of the piece in bytes, after padding. This is the size of data that will be stored in a deal.
        is_verified (bool): A boolean indicating if the deal is verified. Verified deals typically require less collateral.
        tipset (Optional[Tipset]): The tipset at which to check the collateral bounds. If None, the latest tipset is used.

    Returns:
        tuple: A tuple containing two integers (min_value, max_value). 
               'min_value' is the minimum collateral amount required, 
               and 'max_value' is the maximum collateral amount that could be required.
               Returns (None, None) if either 'Min' or 'Max' values are not found in the response.
    """
    cids = None
    if tipset:
        cids = tipset.dct_cids()

    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateDealProviderCollateralBounds",
        "params": [
            padded_piece_size,
            is_verified,
            cids
        ]
    }

    dct_data = connector.execute(payload)
    result = dct_data.get("result", {})
    min_value = result.get("Min")
    max_value = result.get("Max")

    # Converting to integers and returning them as a tuple
    return (int(min_value), int(max_value)) if min_value and max_value else (None, None)

    

def _state_compute(connector: HttpJsonRpcConnector, epoch: int, messages: List[Message], tipset: Optional[Tipset] = None) -> StateComputeOutput:
    """
    Calls the Filecoin StateCompute API to apply a set of messages on a specific tipset at a given epoch.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making the API call.
        epoch (int): The epoch number at which to compute the state. Represents the blockchain height.
        messages (List[Message]): A list of messages to be applied to the state.
        tipset (Optional[Tipset]): The tipset on which the state will be computed. Default is None.

    Returns:
        StateComputeOutput: An object representing the output of the state computation.

    This function constructs a request payload with the specified epoch, messages, and optional tipset.
    It then sends this request to the Filecoin node via the provided HttpJsonRpcConnector instance.
    The response is parsed into a StateComputeOutput object which contains details of the computation result.
    """

    # Extract CIDs from the tipset if provided
    cids = None
    if tipset:
        cids = tipset.dct_cids()

    # Convert the list of Message objects to their JSON representation
    lst_messages = [message.to_json() for message in messages]

    # Construct the request payload
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateCompute",
        "params": [
            epoch,
            lst_messages,
            cids  # Tipset CIDs, if provided
        ] 
    }

    # Execute the API call and parse the result
    dct_data = connector.execute(payload)
    state_compute_output = StateComputeOutput.from_dict(dct_data['result'])
    return state_compute_output


def _circulating_supply(connector: HttpJsonRpcConnector, tipset: Optional[Tipset]) -> int:
    """
    Retrieves the circulating supply of Filecoin at a given tipset.

    This function makes a JSON-RPC call to the Filecoin network to obtain the 
    circulating supply of Filecoin tokens. The circulating supply is the number 
    of tokens that are actively circulating in the market and in the general 
    public's hands. It excludes tokens that are locked, reserved, or not yet 
    released into circulation.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector 
                                          used for making the JSON-RPC call.
        tipset (Optional[Tipset]): The tipset at which the circulating supply 
                                   is to be checked. If None, the latest 
                                   circulating supply is fetched.

    Returns:
        int: The circulating supply of Filecoin at the specified tipset, 
             represented in attoFIL (1 FIL = 10^18 attoFIL).

    Example:
        >>> connector = HttpJsonRpcConnector('http://localhost:1234', 'my_api_token')
        >>> tipset = Tipset(...)
        >>> circulating_supply = _circulating_supply(connector, tipset)
        >>> print(circulating_supply)

    Note:
        Ensure to handle any potential exceptions that may occur due to network 
        issues or unexpected responses from the Filecoin node.
    """
    cids = None
    if tipset:
        cids = tipset.dct_cids()

    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateCirculatingSupply",
        "params": [cids]
    }

    data = connector.execute(payload)
    return int(data["result"])


def _changed_actors(connector: HttpJsonRpcConnector, cid1 : str, cid2 : str):
    """
    Retrieve a list of actors that have changed between two specified CIDs.

    This function sends a JSON RPC request to the Filecoin/Lotus node to fetch a list
    of actors that have changed between the two specified CIDs. The actors are represented
    as a list of `Actor` objects containing information such as their code CID, head CID,
    nonce, and balance.

    Args:
        connector (HttpJsonRpcConnector): An instance of the HTTP-based JSON RPC connector.
        cid1 (str): The first CID to compare.
        cid2 (str): The second CID to compare.

    Returns:
        List[Actor]: A list of `Actor` objects representing actors that have changed.

    Example:
        actors = _changed_actors(connector_instance, "cid1_value", "cid2_value")
    
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateChangedActors",
        "params": Cid.dct_cids([cid1.id, cid2.id])
    }
    
    # execute the method, capture the result
    data = connector.execute(payload)

    actors = []
    results = data.get("result", {})

    for actor_id, actor_data in results.items():
        code_cid = Cid(actor_data["Code"]["/"])
        head_cid = Cid(actor_data["Head"]["/"])
        nonce = actor_data["Nonce"]
        balance = int(actor_data["Balance"])
        actor = Actor(Code=code_cid, Head=head_cid, Nonce=nonce, Balance=balance)
        actors.append(actor)

    return actors
    
def _state_call(connector: HttpJsonRpcConnector, 
                message: Message, 
                tipset: Optional[Tipset] = None) -> InvocationResult:
    """
    Performs a state call to a Filecoin Lotus node via JSON RPC. This method simulates sending a message
    without actually sending it or causing any state change. It's useful for debugging and for calling smart contracts.

    Parameters:
        connector (HttpJsonRpcConnector): The connector instance to interface with the JSON RPC API.
        message (Message): The message to simulate. This contains the information necessary to call a method on a smart contract.
        tipset (Optional[Tipset], optional): The tipset to use for the call context. If not provided, the latest tipset will be used.

    Returns:
        InvocationResult: An object representing the result of the call. This includes the return value and any error if occurred.

    Raises:
        ApiCallError: If there is an issue with the RPC call, an ApiCallError will be raised with the details.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateCall",
        "params": [
            message.to_json(),
            tipset.dct_cids() if tipset else None,
        ]
    }
    
    dct_result = connector.execute(payload, debug=True)
    invocation_result = InvocationResult.from_dict(dct_result)
    return invocation_result

def _account_key(connector: HttpJsonRpcConnector, address: str, tipset: Optional[Tipset] = None) -> Cid:
    """
    Queries a Filecoin Lotus node for the key address associated with a given actor address.

    Parameters:
        connector (HttpJsonRpcConnector): The connector instance to interface with the JSON RPC API.
        address (str): The actor address to query for the corresponding key address.
        tipset (Optional[Tipset], optional): The specific tipset state to look up the actor key address.
            If not provided, the latest state is used.

    Returns:
        Cid: A Cid object representing the key address associated with the given actor address.

    Raises:
        ApiCallError: If there is an issue with the RPC call, an ApiCallError will be raised with the details.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateAccountKey",
        "params": [
            address,
            tipset.dct_cids() if tipset else None,
        ]
    }

    dct_result = connector.execute(payload)
    # Parse the account key
    address = Cid(dct_result["result"])
    return address
    
def _get_actor(connector: HttpJsonRpcConnector, actor_id: str, tipset: Optional[Tipset] = None) -> Actor:
    """
    Fetches an actor's details from a Filecoin Lotus node using its actor ID.

    Parameters:
        connector (HttpJsonRpcConnector): The connector instance to interface with the JSON RPC API.
        actor_id (str): The unique identifier of the actor whose details are being requested.
        tipset (Optional[Tipset], optional): The specific tipset to query against.
            If None, the latest state is used.

    Returns:
        Actor: An Actor object populated with the details of the requested actor, such as the actor's code,
               head, nonce, and balance.

    Raises:
        ApiCallError: If the RPC call encounters an issue, an ApiCallError is raised with detailed information.

    Examples:
        >>> actor_details = _get_actor(connector, 't01234')
        >>> print(actor_details.Code)
        >>> print(actor_details.Balance)
    """
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

    dct_result = connector.execute(payload)
    actor_data = dct_result['result']

    # Create Actor object using parsed data
    actor = Actor(
        Code=Cid(actor_data['Code']['/']),
        Head=Cid(actor_data['Head']['/']),
        Nonce=actor_data['Nonce'],
        Balance=actor_data['Balance'])

    return actor


# WARNING: This method takes an exceptionally long time to complete.
def _list_state_actors(connector, tipset):
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateListActors",
        "params": [
            tipset.dct_cids(),
        ]
    }

    # TODO - unfinished
    dct_result = connector.execute(payload)

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
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.ChainHead",
    }

    dct_result = connector.execute(payload)

    # Parse the CIDs
    lst_cids = [Cid(cid["/"]) for cid in dct_result["result"]["Cids"]]

    # Parse block headers into BlockHeader objects
    lst_block_headers = [dict_to_blockheader(dct) for dct in dct_result["result"]["Blocks"]]
    height = dct_result["result"]["Height"]

    # construct and return a Tipset        
    return Tipset(height, lst_cids, lst_block_headers)

