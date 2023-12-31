from typing import Optional, List, Tuple
from ..http_json_rpc_connector import HttpJsonRpcConnector
from ..types.block_header import BlockHeader, dict_to_blockheader
from ..types.cid import Cid
from ..types.actor_state import ActorState
from ..types.message import Message
from ..types.tip_set import Tipset
from ..types.actor import Actor
from ..types.state_compute_output import StateComputeOutput
from ..types.invocation_result import InvocationResult


def _make_payload(method: str, params: List, tipset: Optional[Tipset] = None):
    """
    Constructs a JSON-RPC payload for a given method and parameters.

    Args:
        method (str): The name of the JSON-RPC method to call.
        params (List): A list of parameters to pass to the method.
        tipset (Optional[Tipset]): The tipset at which to call the method. If None, the latest tipset is used.

    Returns:
        dict: A dictionary containing the JSON-RPC payload.

    """
    cids = None
    if tipset:
        cids = tipset.dct_cids()

    # if params exists (including if it's an empty list), append the cids
    if params is not None:
        params.append(cids)

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


def _market_balance(connector: HttpJsonRpcConnector, address: str, tipset: Optional[Tipset] = None) -> dict:
    """
    Retrieves the market balance information for a given address in the Filecoin network.

    This method queries the Filecoin node to get the escrow and locked funds associated
    with a specific address in the Filecoin storage market. The escrow balance is the total
    funds deposited in the market actor, while the locked balance is the amount locked for
    active deals.

    Args:
        connector: An instance of HttpJsonRpcConnector, used for communication with the
                   Filecoin node.
        address: A string representing the Filecoin address for which to retrieve
                 market balance information. This should be a valid Filecoin address.
        tipset: An optional Tipset object. If provided, the market balance is queried
                at the state of this tipset. If not provided, the current chain head
                is used.

    Returns:
        dict: A dictionary containing two key-value pairs:
              - 'Escrow': An integer representing the total funds in escrow for the
                          given address in the storage market.
              - 'Locked': An integer representing the total funds locked in active
                          deals for the given address.
    """
    payload = _make_payload("Filecoin.StateMarketBalance", [address], tipset)
    dct_result = connector.execute(payload)
    dct_market_balance = {}
    dct_market_balance['Escrow'] = int(dct_result['result']['Escrow'])
    dct_market_balance['Locked'] = int(dct_result['result']['Locked'])
    return dct_market_balance


def _lookup_id(connector: HttpJsonRpcConnector, address: str, tipset: Optional[Tipset] = None) -> str:
    """
    Retrieves the canonical ID address for a given Filecoin address.

    This function communicates with a Filecoin node through the provided connector
    to resolve the ID address corresponding to a given address. The ID address is
    a compact numerical representation used internally by the Filecoin network.

    Args:
        connector: An instance of HttpJsonRpcConnector. This is used to facilitate
                   communication with the Filecoin node.
        address: A string representing the Filecoin address to be resolved. This
                 can be in any of the standard Filecoin address formats.
        tipset: An optional instance of Tipset. If provided, the state at this tipset
                will be considered for resolving the address. If not provided,
                the current chain head is used.

    Returns:
        str: The canonical ID address as a string. If the address cannot be resolved,
             an empty string is returned.

    Raises:
        ConnectorError: If there is an issue with the RPC call to the Filecoin node.
    """
    payload = _make_payload("Filecoin.StateLookupID", [address], tipset)
    dct_result = connector.execute(payload)
    id = dct_result.get("result", "")

    return id


def _list_miners(connector: HttpJsonRpcConnector, tipset: Optional[Tipset] = None) -> List[str]:
    """
    Retrieves a list of all miner addresses from the Filecoin network at a specified tipset.

    This function sends a JSON-RPC request to the Filecoin node via the provided connector.
    It invokes the `StateListMiners` method to fetch all miner addresses currently active
    in the state tree of the specified tipset. The list of miners can be useful for various
    network analyses and operations, such as inspecting miner activity or selecting miners
    for storage deals.

    Args:
        connector (HttpJsonRpcConnector): An object to interface with the Filecoin node. It
                                          should provide an `execute` method for sending
                                          requests to the node.
        tipset (Optional[Tipset]): The tipset at which to query the state. If not provided
                                   (None), the method queries the state at the current chain head.
                                   This parameter allows querying historical state data.

    Returns:
        List[str]: A list containing the addresses of all miners present in the specified
                   tipset. Each address is a string representing the miner's Filecoin address.
    """
    payload = _make_payload("Filecoin.StateListMiners", [], tipset)
    dct_result = connector.execute(payload)
    lst_miners = dct_result.get("result", [])

    return lst_miners


def _list_messages(connector: HttpJsonRpcConnector, to_addr: str, from_addr: str, epoch: int, tipset: Optional[Tipset] = None) -> List[Cid]:
    """
    Fetches a list of messages sent to or from a specified address up to a given chain epoch.

    Args:
        connector (HttpJsonRpcConnector): Connector object to interact with the Filecoin node.
        to_addr (str): The target address of the messages. Can be empty to ignore this filter.
        from_addr (str): The source address of the messages. Can be empty to ignore this filter.
        epoch (int): The maximum chain epoch for the messages. Messages newer than this will not be included.
        tipset (Optional[Tipset]): The tipset object. If provided, messages will be fetched at this tipset state.

    Returns:
        List[Cid]: A list of CIDs representing the messages that match the given criteria.
    """
    dct_params = {}
    if to_addr:
        dct_params["To"] = to_addr
    if from_addr:
        dct_params["From"] = from_addr
    
    payload = _make_payload("Filecoin.StateListMessages", [dct_params], tipset)
    payload["params"].append(epoch)
    response = connector.execute(payload, debug=True)
    return Cid.dct_cids(response['result'])



def _read_state(connector: HttpJsonRpcConnector, actor_id: str, tipset: Optional[Tipset] = None) -> ActorState:
    """
    Reads the state of an actor at a specified tipset in the Filecoin network.

    This function queries the state of a given actor (identified by `actor_id`) from the Filecoin network
    using the provided HTTP JSON-RPC connector. It can target the state at a specific tipset if provided;
    otherwise, it uses the latest state.

    Args:
        connector (HttpJsonRpcConnector): The connector object used for communicating with the Filecoin node.
                                          It must implement an `execute` method for sending the RPC request.
        actor_id (str): The identifier (address) of the actor whose state is to be read.
        tipset (Optional[Tipset]): The tipset key at which to read the state. If `None`, the latest state is used.

    Returns:
        ActorState: An object representing the state of the actor at the specified tipset. This includes
                    various details like balance, nonce, etc., depending on the actor type.
    """
    payload = _make_payload("Filecoin.StateReadState", [actor_id], tipset)
    response = connector.execute(payload)
    return ActorState.from_dict(response['result'])


def _get_randomness_from_beacon(
        connector: HttpJsonRpcConnector, 
        domain_tag: int, 
        epoch: int, 
        entropy_base64: str, 
        tipset: Optional[Tipset] = None) -> str:
    """
    Retrieves randomness from the Filecoin network's randomness beacon for a specific epoch.

    This function sends a request to the Filecoin network to obtain randomness for a given epoch. 
    The randomness is derived from the network's randomness beacon, which provides unpredictable and unbiased random values.

    Args:
        connector (HttpJsonRpcConnector): An instance of `HttpJsonRpcConnector` used to send the JSON-RPC request.
        domain_tag (int): The domain separation tag (DST) to uniquely identify the use case for the randomness.
        epoch (int): The epoch number for which the randomness is requested.
        entropy_base64 (str): A base64 encoded string of bytes used as additional entropy in the randomness generation process.
        tipset (Optional[Tipset]): The tipset key for specifying a particular chain context. If None, the latest tipset is used.

    Returns:
        str: A base64 encoded string representing the random value obtained from the beacon.
    """
    payload = _make_payload("Filecoin.StateGetRandomnessFromBeacon", [domain_tag, epoch, entropy_base64], tipset)
    response = connector.execute(payload, debug=True)
    return response['result']


def _decode_params(connector: HttpJsonRpcConnector, actor_cid: str, method: int, params: str, tipset: Optional[Tipset] = None) -> dict:
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
    payload= _make_payload("Filecoin.StateDecodeParams", [actor_cid, method, params], tipset)
    response = connector.execute(payload)
    return response.get("result", {})


def _deal_provider_collateral_bounds(
    connector: HttpJsonRpcConnector, 
    padded_piece_size: int, 
    is_verified: bool, 
    tipset: Optional[Tipset]
) -> Tuple[Optional[int], Optional[int]]:
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
    payload = _make_payload("Filecoin.StateDealProviderCollateralBounds", [padded_piece_size, is_verified], tipset)
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

    # Convert the list of Message objects to their JSON representation
    lst_messages = [message.to_json() for message in messages]
    payload = _make_payload("Filecoin.StateCompute", [epoch, lst_messages], tipset)
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
    payload = _make_payload("Filecoin.StateCirculatingSupply", [], tipset)
    data = connector.execute(payload)
    return int(data["result"])


def _changed_actors(connector: HttpJsonRpcConnector, cid1 : str, cid2 : str) -> List[Actor]:
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
    payload = _make_payload("Filecoin.StateChangedActors", Cid.dct_cids([cid1.id, cid2.id], None))
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
    payload = _make_payload("Filecoin.StateCall", [message.to_json()], tipset)
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
    payload = _make_payload("Filecoin.StateAccountKey", [address], tipset)
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
    payload = _make_payload("Filecoin.StateGetActor", [actor_id], tipset)
    dct_result = connector.execute(payload)
    actor_data = dct_result['result']

    # Create Actor object using parsed data
    actor = Actor(
        code=Cid(actor_data['Code']['/']),
        head=Cid(actor_data['Head']['/']),
        nonce=actor_data['Nonce'],
        balance=actor_data['Balance'])

    return actor


def _list_actors(connector, tipset) -> List[str]:
    """
    Retrieves a list of all actors in a specified tipset.

    This function sends a request to the Filecoin node via the provided connector,
    invoking the `StateListActors` method to fetch all actors present in the state
    tree of the specified tipset.

    Args:
        connector: An object to interface with the Filecoin node. It should provide
                   an `execute` method for sending requests to the node.
        tipset: An optional tipset key indicating the state at which to list actors.
                If `None`, the latest state will be used.

    Returns:
        list: A list of actor addresses (as strings) present in the specified tipset.
    """
    payload = _make_payload("Filecoin.StateListActors", [], tipset)
    dct_result = connector.execute(payload)
    lst_actors = dct_result.get("result", [])

    return lst_actors
