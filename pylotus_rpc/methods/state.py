from typing import Optional, List, Tuple, Dict
from ..http_json_rpc_connector import HttpJsonRpcConnector
from ..types.block_header import BlockHeader, dict_to_blockheader
from ..types.cid import Cid
from ..types.actor_state import ActorState
from ..types.message import Message
from ..types.tip_set import Tipset
from ..types.actor import Actor
from ..types.deal_proposal import DealProposal
from ..types.deal_state import DealState
from ..types.state_compute_output import StateComputeOutput
from ..types.invocation_result import InvocationResult
from ..types.sector import Sector
from ..types.deadline import Deadline
from ..types.miner_info import MinerInfo
from ..types.sector_pre_commit_info import SectorPreCommitInfo
from ..types.miner_partition import MinerPartition
from ..types.miner_power import MinerPower
from ..types.deadline_info import DeadlineInfo
from ..types.message_lookup import MessageLookup


class SectorPreCommitInfoNotFound(Exception):
    """Exception raised when a sector pre-commit info is not found."""

    def __init__(self, address=None, sector_number=None, message="Sector pre-commit info not found"):
        self.address = address
        self.sector_number = sector_number
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SectorNotFound(Exception):
    """Exception raised when a sector is not found."""

    def __init__(self, address=None, sector_number=None, message="Sector not found"):
        self.address = address
        self.sector_number = sector_number
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class MessageNotFound(Exception):
    """Exception raised when a message is not found."""

    def __init__(self, cid=None, message="Message not found"):
        self.message_id = cid
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


def _make_payload(method: str, params: List, tipset: Optional[Tipset] = None, include_tipset: bool = True) -> dict:
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
        cids = tipset.lst_dct_cids()

    # if params exists (including if it's an empty list), append the cids, unless
    # we are told not too (a few routines don't accept at tipset parameter)
    if params is not None and include_tipset:
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


def _verifier_status(connector: HttpJsonRpcConnector, address: str, tipset: Optional[Tipset] = None) -> int:
    """
    Queries the Filecoin network for the DataCap allocated to a verifier.

    This function sends a request to the Filecoin network to obtain the amount of DataCap 
    allocated to the specified verifier address. The DataCap represents the total volume of data 
    (in bytes) that the verifier can allocate to clients for subsidized storage.

    Args:
        connector (HttpJsonRpcConnector): An object used to connect and send requests to the Filecoin network.
        address (str): The Filecoin address of the verifier whose DataCap status is being queried.
        tipset (Optional[Tipset]): The specific tipset at which to query the verifier's status. 
                                   If None, the latest tipset is used.

    Returns:
        int: The amount of DataCap (in bytes) allocated to the verifier. Returns 0 if the verifier 
             does not have any DataCap or if the address does not correspond to a recognized verifier.

    Raises:
        Exception: If there's an error in the execution of the query, potentially due to connectivity 
                   issues or an invalid address.
    """
    payload = _make_payload("Filecoin.StateVerifierStatus", [address], tipset)
    dct_data = connector.execute(payload)

    # Handle case where the verifier has no allocated DataCap or the address is not a verifier
    if dct_data['result'] is None:
        return 0

    # Convert the DataCap value to an integer and return it
    return int(dct_data['result'])


def _verified_registry_root_key(connector: HttpJsonRpcConnector, tipset: Optional[Tipset] = None) -> str:
    """
    Retrieves the verified registry root key from the Filecoin network.

    This function sends a request to the Filecoin network to obtain the root key of the verified registry.
    The verified registry is a data structure used to store verified client information.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        tipset (Optional[Tipset]): An optional parameter specifying the tipset at which the query should be made.
                                   If None, the query is made against the latest state.

    Returns:
        str: The root key of the verified registry.

    Raises:
        HTTPError: If the request to the Filecoin node fails.
    """
    payload = _make_payload("Filecoin.StateVerifiedRegistryRootKey", [], tipset)
    dct_data = connector.execute(payload)
    return dct_data['result']


def _verified_client_status(connector: HttpJsonRpcConnector, address: str, tipset: Optional[Tipset] = None) -> int:
    """
    Retrieves the DataCap allocated to a verified client within the Filecoin network.

    This function sends a request to the Filecoin network to obtain the amount of DataCap
    allocated to a verified client. DataCap is a measure of data storage space that can be
    used in deals with storage miners, and having a verified status may grant the client
    access to larger amounts of storage at better prices.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        address (str): The Filecoin address of the client whose DataCap status is being queried.
        tipset (Optional[Tipset]): An optional parameter specifying the tipset at which the query should be made.
                                   If None, the query is made against the latest state.

    Returns:
        int: The amount of DataCap (in bytes) allocated to the specified client. Returns 0 if the client is not verified or has no allocated DataCap.

    Raises:
        HTTPError: If the request to the Filecoin node fails.
    """
    payload = _make_payload("Filecoin.StateVerifiedClientStatus", [address], tipset)
    dct_data = connector.execute(payload)

    if dct_data['result'] is None:
        return 0

    return int(dct_data['result'])


def _vm_circulating_supply_internal(connector: HttpJsonRpcConnector, tipset: Optional[Tipset] = None) -> Dict[str, int]:
    """
    Retrieves the internal circulating supply metrics from the Filecoin VM.

    This method calls the Filecoin.StateVMCirculatingSupplyInternal JSON-RPC method
    to fetch the latest circulating supply metrics, including details like the total
    FIL burnt, circulating, locked, mined, reserve disbursed, and vested.

    Args:
        connector (HttpJsonRpcConnector): A connector instance to make the JSON-RPC call.
        tipset (Optional[Tipset]): An optional tipset to specify the state at a particular chain height.

    Returns:
        Dict[str, int]: A dictionary mapping each supply metric (e.g., FilBurnt, FilCirculating) to its
        value in integer format.
    """
    payload = _make_payload("Filecoin.StateVMCirculatingSupplyInternal", [], tipset)
    dct_data = connector.execute(payload)['result']
    # Convert the values to integers and return
    return {k: int(v) for k, v in dct_data.items()}


def _sector_pre_commit_info(connector: HttpJsonRpcConnector, miner_address: str, sector_number: int, tipset: Optional[Tipset] = None) -> SectorPreCommitInfo:
    """
    Retrieves pre-commit information for a specified sector from a Filecoin miner.

    This function queries the Filecoin blockchain to obtain details about a sector's pre-commit state,
    including the pre-commit deposit, pre-commit info, and other relevant data. The pre-commit phase
    is the period after a miner has committed to storing a sector but before the storage is verified
    and accepted into the blockchain.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The Filecoin miner address from which to retrieve sector pre-commit information.
        sector_number (int): The unique number of the sector for which to retrieve pre-commit information.
        tipset (Optional[Tipset]): The specific tipset at which to query the data. If None, the most recent
                                   tipset is used. This allows querying historical state at a specific blockchain height.

    Returns:
        SectorPreCommitInfo: An object containing the sector's pre-commit information, such as the seal rand epoch,
                             deal IDs, expiration, and other relevant data.

    Raises:
        SectorPreCommitInfoNotFound: If the sector pre-commit information is not found or the query results in an error.
                                     This exception includes the miner address, sector number, and the error message.    
    """
    payload = _make_payload("Filecoin.StateSectorPreCommitInfo", [miner_address, sector_number], tipset)
    dct_data = connector.execute(payload, debug=True)

    if 'error' in dct_data:
        raise SectorPreCommitInfoNotFound(miner_address, sector_number, dct_data['error']['message'])

    return SectorPreCommitInfo.from_dict(dct_data['result'])


def _sector_partition(connector: HttpJsonRpcConnector, miner_address: str, sector_number: int, tipset: Optional[Tipset] = None) -> Dict[str, int]:
    """
    Retrieves the partition information for a specific sector identified by its sector number
    for a given miner.

    This method queries the Filecoin network to determine the partition in which a sector is
    located. It returns a dictionary containing the index of the deadline and partition in which
    the sector is located.

    Args:
        connector (HttpJsonRpcConnector): The connector object used for sending requests to the
                                           Filecoin network via its JSON-RPC interface.
        miner_address (str): The address of the miner to which the sector belongs.
        sector_number (int): The number identifying the specific sector within the miner's sector set.
        tipset (Optional[Tipset]): An optional parameter that specifies the blockchain tipset
                                   from which to base the query. If None, the query is based on the
                                   current chain head.

    Returns:
        Dict[str, int]: A dictionary containing the 'Deadline' and 'Partition' indices for the sector.
                        'Deadline' is the index of the deadline in which the sector is located, and
                        'Partition' is the index of the partition within the deadline.

    Raises:
        SectorNotFound: If the specified sector cannot be found for the given miner address,
                        an exception is raised indicating the sector was not found.
    """
    payload = _make_payload("Filecoin.StateSectorPartition", [miner_address, sector_number], tipset)
    dct_data = connector.execute(payload)

    # Handling potential errors in response
    if 'error' in dct_data:
        raise SectorNotFound(miner_address, sector_number, dct_data['error']['message'])

    # Assuming the response is successful, return the partition details
    return dct_data['result']

def _sector_get_info(connector: HttpJsonRpcConnector, miner_address: str, sector_number: int, tipset: Optional[Tipset] = None) -> Sector:
    """
    Retrieves detailed information about a specific sector identified by its sector number for a given miner address.

    This function sends a JSON-RPC request to a Filecoin node through the specified connector, using the
    'Filecoin.StateSectorGetInfo' method. It queries information about a sector belonging to a miner, optionally
    at a specific blockchain state identified by a tipset.

    Args:
        connector (HttpJsonRpcConnector): An object responsible for managing HTTP JSON-RPC requests to a Filecoin node.
        miner_address (str): The address of the miner whose sector information is being queried.
        sector_number (int): The number of the sector for which information is being requested.
        tipset (Optional[Tipset]): An optional tipset to specify the state at which to query the sector information.
                                  If None, the latest state is used.

    Returns:
        Sector: An object containing detailed information about the sector, including its state, deals,
                expiration, and more, depending on the Filecoin API's response structure.

    Raises:
        An exception if the request fails or if the response from the Filecoin node does not contain the
        expected information. The exact exception will depend on the implementation of the `HttpJsonRpcConnector`
        and the response from the Filecoin node.
    """
    payload = _make_payload("Filecoin.StateSectorGetInfo", [miner_address, sector_number], tipset)
    dct_data = connector.execute(payload)
    if 'result' not in dct_data:
        raise ValueError("Failed to fetch sector information or sector does not exist.")
    return Sector.from_dict(dct_data['result'])


def _sector_expiration(connector: HttpJsonRpcConnector, miner_address: str, sector_number: int, tipset: Optional[Tipset] = None) -> Dict[str, int]:
    """
    Retrieves expiration information for a specific sector identified by its sector number
    for a given miner.

    This method queries the Filecoin network to determine the scheduled expiration epoch
    for a sector. It provides both the on-time expiration epoch, indicating when the sector
    is scheduled to expire under normal circumstances, and an early expiration value which
    is typically zero unless the sector is set to expire ahead of its on-time expiration due
    to certain conditions like penalties or manual termination.

    Args:
        connector (HttpJsonRpcConnector): The connector object used for sending requests to the
                                           Filecoin network via its JSON-RPC interface.
        miner_address (str): The address of the miner to which the sector belongs.
        sector_number (int): The number identifying the specific sector within the miner's sector set.
        tipset (Optional[Tipset]): An optional parameter that specifies the blockchain tipset
                                   from which to base the query. If None, the query is based on the
                                   current chain head.

    Returns:
        Dict[str, int]: A dictionary containing the 'OnTime' and 'Early' expiration epochs for the sector.
                        'OnTime' is the epoch at which the sector is scheduled to expire, and 'Early' is
                        the epoch if the sector is set to expire earlier than its scheduled on-time expiration,
                        which is usually zero under normal circumstances.

    Raises:
        SectorNotFound: If the specified sector cannot be found for the given miner address,
                        an exception is raised indicating the sector was not found.
    """
    payload = _make_payload("Filecoin.StateSectorExpiration", [miner_address, sector_number], tipset)
    dct_data = connector.execute(payload)

    # Handling potential errors in response
    if 'error' in dct_data:
        raise SectorNotFound(miner_address, sector_number, dct_data['error']['message'])

    # Assuming the response is successful, return the expiration details
    return dct_data['result']


def _search_message_limited(connector: HttpJsonRpcConnector, cid: str, limit: int) -> MessageLookup:
    """
    Searches the blockchain up to a specified number of epochs in the past for a message by its CID and returns its
    execution details if found.

    This function sends a request to the Filecoin node to search for a message identified by its CID, looking back up
    to `limit` epochs from the current head of the blockchain. If the message is found within this range, it returns
    an instance of `MessageLookup` containing the message details, its receipt, and the tipset in which the message
    was executed.

    Args:
        connector (HttpJsonRpcConnector): The connector used for making API requests to a Filecoin node.
        cid (str): The Content Identifier (CID) of the message to search for.
        limit (int): The maximum number of epochs to look back in the chain from the current head.

    Returns:
        MessageLookup: An object encapsulating the details of the message's execution, including its receipt and the
                       tipset where it was executed, provided the message is found within the specified epoch limit.

    Raises:
        MessageNotFound: If the message cannot be found within the specified number of epochs or if an error occurs
                         during the search.
    """
    payload = _make_payload("Filecoin.StateSearchMsgLimited", [Cid(cid).to_dict(), limit], include_tipset=False)
    dct_data = connector.execute(payload)

    # If an error is identified in the response, raise an exception to indicate the message couldn't be located.
    if 'error' in dct_data:
        raise MessageNotFound(cid, dct_data['error']['message'])

    return MessageLookup.from_dict(dct_data['result'])


def _search_message(connector: HttpJsonRpcConnector, cid: str) -> MessageLookup:
    """
    Searches for a message in the Filecoin blockchain by its CID and returns its execution details.

    This function sends a request to a Filecoin node to search for a message by its CID.
    If found, it returns an instance of MessageLookup containing the details of the message
    execution, including its receipt and the tipset in which it was included.

    Args:
        connector (HttpJsonRpcConnector): An interface for making requests to a Filecoin node.
        cid (str): The Content Identifier (CID) of the message to search for.

    Returns:
        MessageLookup: An object containing the details of the message execution, if found.

    Raises:
        MessageNotFound: If the message with the given CID cannot be found or if there's an error
                         in retrieving the message from the Filecoin network.
    """
    payload = _make_payload("Filecoin.StateSearchMsg", Cid.format_cids_for_json([cid]), include_tipset=False)
    dct_data = connector.execute(payload)

    # raise an exception if the message can't be found / loaded
    if 'error' in dct_data:
        raise MessageNotFound(cid, dct_data['error']['message'])

    return MessageLookup.from_dict(dct_data['result'])


def _replay(connector: HttpJsonRpcConnector, cid: str, tipset: Optional[Tipset] = None) -> InvocationResult:
    """
    Replays a message, returning the result of the message execution.

    This function sends a request to the Filecoin network to replay a message, returning the result of the message execution.
    The message is identified by its CID (Content Identifier), and the tipset parameter specifies the state at which to replay the message.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        cid (str): The CID of the message to replay.
        tipset (Optional[Tipset]): The tipset at which to replay the message. If None, the latest tipset is used.

    Returns:
        InvocationResult: An instance of InvocationResult containing the result of the message execution.
    """
    tipset_key = []
    if tipset:
        tipset_key = tipset.lst_dct_cids()

    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateReplay",
        "params": [tipset_key, {"/": cid}]
    }
    dct_data = connector.execute(payload, debug=True)

    # raise an exception if the message can't be found / loaded
    if 'error' in dct_data:
        raise MessageNotFound(cid, dct_data['error']['message'])

    return InvocationResult.from_dict(dct_data['result'])


def _network_version(connector: HttpJsonRpcConnector, tipset: Optional[Tipset] = None) -> int:
    """
    Retrieves the version of the Filecoin network protocol as of a specific tipset.

    This function queries the Filecoin node to get the network's protocol version at the specified tipset.
    If no tipset is provided, the current network version is returned.

    Args:
        connector (HttpJsonRpcConnector): The connector used to communicate with the Filecoin node.
        tipset (Optional[Tipset]): The tipset at which to get the network version. If None, the latest network version is retrieved.

    Returns:
        int: The protocol version of the Filecoin network at the given tipset.

    Raises:
        HTTPError: If the request to the Filecoin node fails.
    """
    payload = _make_payload("Filecoin.StateNetworkVersion", [], tipset)
    dct_data = connector.execute(payload)
    return int(dct_data['result'])


def _network_name(connector: HttpJsonRpcConnector) -> str:
    """
    Retrieves the name of the Filecoin network.

    This function sends a request to the Filecoin network to obtain the name of the network.
    The network name is a human-readable identifier for the network, such as "mainnet" or "testnet".

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.

    Returns:
        str: The name of the Filecoin network.

    Raises:
        HTTPError: If the request to the Filecoin node fails.
    """
    payload = {
            "jsonrpc": "2.0",
            "method": "Filecoin.StateNetworkName"
    }
    dct_data = connector.execute(payload)
    return dct_data['result']


def _miner_sectors(connector: HttpJsonRpcConnector, miner_address: str, sector_list: List[int] = [], tipset: Optional[Tipset] = None) -> List[Sector]:
    """
    Retrieves detailed information about a list of sectors for a given miner address.

    This function queries the Filecoin network to obtain detailed information about a list of sectors for a given miner address.
    It returns a list of Sector objects, each representing a sector associated with the miner.
    The Sector object includes sector details such as sector number, seal proof, sealed CID, and more.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve sector details.
        sector_list (List[int]): A list of sector numbers for which to retrieve detailed information. If empty, all sectors are retrieved.
        tipset (Optional[Tipset]): The tipset at which to query the sector details. If None, the latest tipset is used.

    Returns:
        List[Sector]: A list of Sector objects, each containing detailed information about a sector.
    """
    payload = _make_payload("Filecoin.StateMinerSectors", [miner_address, sector_list], tipset)
    list_of_dicts = connector.execute(payload)['result']
    list_of_active_sectors = [Sector.from_dict(dct) for dct in list_of_dicts]

    return list_of_active_sectors


def _miner_sector_count(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> Dict:
    """
    Retrieves the sector count for a given miner address.

    This function queries the Filecoin network to obtain the sector count for a specified miner address.
    It returns a dictionary containing the number of active and faulty sectors for the miner.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve the sector count.
        tipset (Optional[Tipset]): The tipset at which to query the sector count. If None, the latest tipset is used.

    Returns:
        Dict: A dictionary containing the number of active and faulty sectors for the miner.
    """
    payload = _make_payload("Filecoin.StateMinerSectorCount", [miner_address], tipset)
    dct_data = connector.execute(payload)
    return dct_data['result']


def _miner_sector_allocated(connector: HttpJsonRpcConnector, miner_address: str, sector_number: int, tipset: Optional[Tipset] = None) -> bool:
    """
    Checks if a sector has been allocated for sealing by a given miner.

    This function queries the Filecoin network to determine if a given sector number has been allocated for sealing by a specified miner.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to check the sector allocation.
        sector_number (int): The sector number to check.
        tipset (Optional[Tipset]): The tipset at which to check the sector allocation. If None, the latest tipset is used.

    Returns:
        bool: A boolean indicating if the sector has been allocated for sealing by the miner.
    """
    payload = _make_payload("Filecoin.StateMinerSectorAllocated", [miner_address, sector_number], tipset)
    dct_data = connector.execute(payload)
    return dct_data['result']


def _miner_recoveries(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> List[int]:
    """
    Retrieves a list of recovered sectors for a given miner address.

    This function queries the Filecoin network to obtain a list of recovered sectors for a given miner address.
    It returns a list of integers, each representing a sector number that has been recovered.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve recovered sectors.
        tipset (Optional[Tipset]): The tipset at which to query the recovered sectors. If None, the latest tipset is used.

    Returns:
        List[int]: A list of integers, each representing a sector number that has been recovered.
    """
    payload = _make_payload("Filecoin.StateMinerRecoveries", [miner_address], tipset)
    lst_of_recoveries = connector.execute(payload)['result']
    return lst_of_recoveries


def _miner_proving_deadline(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> DeadlineInfo:
    """
    Retrieves the proving deadline information for a given miner.

    This function queries the Filecoin network to obtain detailed information about the current
    proving deadline for a specified miner. This includes information such as the current epoch,
    deadline index, open and close epochs for the deadline, and more.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve proving deadline information.
        tipset (Optional[Tipset]): The tipset at which to query the proving deadline. If None, the latest tipset is used.

    Returns:
        DeadlineInfo: An instance of DeadlineInfo containing detailed information about the miner's current proving deadline.
    """
    payload = _make_payload("Filecoin.StateMinerProvingDeadline", [miner_address], tipset)
    dct_data = connector.execute(payload)
    return DeadlineInfo.from_dict(dct_data['result'])



def _miner_pre_commit_deposit_for_power(connector: HttpJsonRpcConnector, miner_address: str, sector_pre_commit_info: SectorPreCommitInfo, tipset: Optional[Tipset] = None) -> int:
    """
    Calculates the PreCommit Deposit required for a given sector pre-commitment by a miner.

    This function queries the Filecoin network to determine the amount of collateral a miner must
    deposit when pre-committing a new sector. The PreCommit Deposit is a form of collateral that 
    ensures miners follow through with their commitment.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner.
        sector_pre_commit_info (SectorPreCommitInfo): Information about the sector being pre-committed.
        tipset (Optional[Tipset]): The tipset at which to query. If None, the latest tipset is used.

    Returns:
        int: The amount of PreCommit Deposit required in attoFIL (1 FIL = 10^18 attoFIL).

    Raises:
        HTTPError: If the request to the Filecoin node fails.
    """
    payload = _make_payload("Filecoin.StateMinerPreCommitDepositForPower", [miner_address, sector_pre_commit_info.to_dict()], tipset)
    dct_data = connector.execute(payload)
    return int(dct_data['result'])



def _miner_power(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> MinerPower:
    """
    Retrieves the mining power of a given miner at a specified tipset.

    This function queries the Filecoin network to obtain the miner's power, including raw byte power and adjusted quality power. It also indicates if the miner has the minimum power required in the network.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve power information.
        tipset (Optional[Tipset]): The tipset at which to query the miner's power. If None, the latest tipset is used.

    Returns:
        MinerPower: An instance of MinerPower dataclass, containing the miner's power details and whether they have the minimum required power.
    """
    payload = _make_payload("Filecoin.StateMinerPower", [miner_address], tipset)
    dct_data = connector.execute(payload)
    miner_power = MinerPower.from_dict(dct_data['result'])
    return miner_power


def _miner_partitions(connector: HttpJsonRpcConnector, miner_address: str, deadline_index: int, tipset: Optional[Tipset] = None) -> List[MinerPartition]:
    """
    Retrieves the partition details for a specific miner and deadline index.

    This function communicates with a Filecoin node via the provided connector to fetch 
    partition details for a miner at a given deadline index. It returns a list of 
    MinerPartition objects, each representing a partition.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector to facilitate
                                          communication with the Filecoin node.
        miner_address (str): The address of the miner for which partition details are sought.
        deadline_index (int): The index of the deadline for which partition details are sought.
        tipset (Optional[Tipset]): The tipset at which to query the miner partitions. If None, 
                                  the latest tipset is used.

    Returns:
        List[MinerPartition]: A list of MinerPartition objects, each representing a partition
                              within the specified miner's deadline.
    """
    payload = _make_payload("Filecoin.StateMinerPartitions", [miner_address, deadline_index], tipset)
    dct_data = connector.execute(payload)
    miner_partitions = []
    for dct_partition in dct_data['result']:
        miner_partitions.append(MinerPartition.from_dict(dct_partition))

    return miner_partitions


def _miner_initial_pledge_collateral(connector: HttpJsonRpcConnector, miner_address: str, sector_pre_commit_info: SectorPreCommitInfo, tipset: Optional[Tipset] = None) -> int:
    """
    Calculates the initial pledge collateral for a given miner and sector pre-commit info.

    This function sends a request to the Filecoin network to calculate the initial pledge
    collateral required for a sector based on its pre-commit information.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner.
        sector_pre_commit_info (SectorPreCommitInfo): Information about the sector during its pre-commit phase.
        tipset (Optional[Tipset]): The tipset at which to perform this query. If None, the latest tipset is used.

    Returns:
        int: The amount of initial pledge collateral required, in attoFIL.
    """
    payload = _make_payload("Filecoin.StateMinerInitialPledgeCollateral", [miner_address, sector_pre_commit_info.to_dict()], tipset)
    dct_data = connector.execute(payload)
    return int(dct_data['result'])


def _miner_info(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> MinerInfo:
    """
    Retrieves detailed information about a specific miner from the Filecoin network.

    This function sends a request to the Filecoin node via the provided connector,
    invoking the `StateMinerInfo` method. It fetches detailed information about the
    specified miner, including owner, worker addresses, peer ID, sector size, and more.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve information.
        tipset (Optional[Tipset]): The tipset at which to query the miner information. If None,
                                  the latest tipset is used.

    Returns:
        MinerInfo: An instance of MinerInfo containing various details about the specified miner.
                   This includes the miner's owner, worker addresses, peer ID, sector size, and other
                   relevant information.
    """
    payload = _make_payload("Filecoin.StateMinerInfo", [miner_address], tipset)
    dct_data = connector.execute(payload)
    miner_info = MinerInfo.from_dict(dct_data['result'])
    return miner_info


def _miner_faults(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> List[int]:
    """
    Retrieves a list of faulted sectors for a given miner address.

    This function queries the Filecoin network to obtain a list of faulted sectors for a given miner address.
    It returns a list of integers, each representing a sector number that has been faulted.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve faulted sectors.
        tipset (Optional[Tipset]): The tipset at which to query the faulted sectors. If None, the latest tipset is used.

    Returns:
        List[int]: A list of integers, each representing a sector number that has been faulted.
    """
    payload = _make_payload("Filecoin.StateMinerFaults", [miner_address], tipset)
    lst_of_faults = connector.execute(payload)['result']
    return lst_of_faults


def _miner_deadlines(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> List[Deadline]:
    """
    Retrieves the deadlines for a given miner address.

    This function queries the Filecoin network to obtain the deadlines for a specified miner address.
    It returns a list of Deadline objects, each representing a miner's deadline, with information such as 
    post submissions and disputable proof count.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve deadlines.
        tipset (Optional[Tipset]): The tipset at which to query the deadlines. If None, the latest tipset is used.

    Returns:
        List[Deadline]: A list of Deadline objects, each representing a deadline with information like post submissions and disputable proof count.
    """
    payload = _make_payload("Filecoin.StateMinerDeadlines", [miner_address], tipset)
    deadlines_data = connector.execute(payload)['result']
    lst_of_deadlines = [Deadline.from_dict(deadline_dict) for deadline_dict in deadlines_data]
    return lst_of_deadlines


def _miner_available_balance(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> int:
    """
    Retrieves the available balance of a given miner address.

    This function queries the Filecoin network to obtain the available balance of a given miner address.
    The available balance is the amount of FIL that can be withdrawn by the miner.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve the available balance.
        tipset (Optional[Tipset]): The tipset at which to query the available balance. If None, the latest tipset is used.

    Returns:
        int: The available balance of the miner, represented in attoFIL (1 FIL = 10^18 attoFIL).
    """
    payload = _make_payload("Filecoin.StateMinerAvailableBalance", [miner_address], tipset)
    dct_data = connector.execute(payload)
    available_balance = int(dct_data['result'])
    return available_balance


def _miner_active_sectors(connector: HttpJsonRpcConnector, miner_address: str, tipset: Optional[Tipset] = None) -> List[Sector]:
    """
    Retrieves a list of active sectors for a given miner address.

    This function queries the Filecoin network to obtain a list of active sectors for a given miner address.
    It returns a list of Sector objects, each representing a sector associated with the miner.
    The Sector object includes sector details such as sector number, seal proof, sealed CID, and more.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        miner_address (str): The address of the miner for which to retrieve active sectors.
        tipset (Optional[Tipset]): The tipset at which to query the active sectors. If None, the latest tipset is used.

    Returns:
        List[Sector]: A list of Sector objects, each containing detailed information about an active sector.
    """
    payload = _make_payload("Filecoin.StateMinerActiveSectors", [miner_address], tipset)
    list_of_dicts = connector.execute(payload)['result']
    list_of_active_sectors = [Sector.from_dict(dct) for dct in list_of_dicts]

    return list_of_active_sectors


def _storage_market_deal(connector: HttpJsonRpcConnector, deal_id: int, tipset: Optional[Tipset] = None) -> dict:
    """
    Retrieves details of a storage market deal by its deal ID.

    This function queries the Filecoin node for information about a specific storage market deal,
    identified by its deal ID. It returns both the deal's proposal and its state.

    Args:
        connector (HttpJsonRpcConnector): The connector used to interact with the Filecoin node.
        deal_id (int): The unique identifier of the storage market deal.
        tipset (Optional[Tipset]): The tipset at which to query the deal's state. 
                                   If None, the latest state is used.

    Returns:
        dict: A dictionary containing two keys, 'Proposal' and 'State'. 
              'Proposal' maps to an instance of DealProposal containing the details of the deal's proposal.
              'State' maps to an instance of DealState containing the current state of the deal.

    """
    payload = _make_payload("Filecoin.StateMarketStorageDeal", [deal_id], tipset)
    result = connector.execute(payload)
    deal_proposal = DealProposal.from_dict(result['result']['Proposal'])
    deal_state = DealState.from_dict(result['result']['State'])
    return {"Proposal": deal_proposal, "State": deal_state}


def _market_participants(connector: HttpJsonRpcConnector, tipset: Optional[Tipset] = None) -> List[Dict]:
    """
    Retrieves a list of market participants (dealers and clients) from the Filecoin network.

    This method calls the `StateMarketParticipants` Lotus RPC API to obtain information about
    all market participants (dealers and clients) in the specified tipset. If no tipset is provided,
    it retrieves information from the latest state.

    Args:
        connector (HttpJsonRpcConnector): An instance of HttpJsonRpcConnector for making API requests.
        tipset (Optional[Tipset]): An optional Tipset object representing the state at which to query. 
                                   If None, the latest state will be queried.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains details about a market participant.
                    The details include the participant's ID and other relevant information.
    """
    payload = _make_payload("Filecoin.StateMarketParticipants", [], tipset)
    data = connector.execute(payload)['result']
    list_of_dicts = [{"id": key, "Escrow": int(value['Escrow']), "Locked": int(value['Locked'])} for key, value in data.items()]
    return list_of_dicts

    
def _market_deals(connector: HttpJsonRpcConnector, tipset: Optional[Tipset] = None) -> dict:
    """
    Retrieves all active deals in the Filecoin storage market.

    We tried to implement this method but it spikes the memory usage of our lotus node so much that it could be used to perform a DoS attack.
    Currently, we haven't found a single node that supports this call so it's useless to implement it.
    """
    raise NotImplementedError("StateMarketDeals is not implemented yet")


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
    return Cid.format_cids_for_json(response['result'])



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
    payload = _make_payload("Filecoin.StateChangedActors", Cid.format_cids_for_json([cid1.id, cid2.id]))
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
