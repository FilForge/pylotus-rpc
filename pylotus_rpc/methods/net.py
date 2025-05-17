from ..http_json_rpc_connector import HttpJsonRpcConnector
from typing import List, Dict, Tuple
from ..types.address_info import AddressInfo
from ..types.nat_info import NatInfo

ApiCallError = HttpJsonRpcConnector.ApiCallError


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


def _stat(connector: HttpJsonRpcConnector, scope: str) -> Dict:
    """
    Retrieves network statistics for a specific scope from the Lotus node.
    
    This method provides detailed network statistics including bandwidth usage, connection counts,
    and other network-related metrics for the specified scope.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        scope (str): The scope for which to retrieve network statistics.

    Returns:
        Dict: A dictionary containing statistics for the specified scope

    Raises:
        ApiCallError: If the RPC call fails or returns an error.
    """
    payload = _make_payload("Filecoin.NetStat", [scope])
    dct_response = connector.execute(payload)

    if 'error' in dct_response:
        raise ApiCallError("Filecoin.NetStat", dct_response['error']['code'], dct_response['error']['message'])
    else:
        return dct_response['result']


def _set_limit(
    connector: HttpJsonRpcConnector,
    service: str,
    limits: Dict[str, int]
) -> Tuple[bool, str]:
    """
    Sets network resource limits for a specified service on a Filecoin node.
    
    This method configures limits on resources such as memory, streams, connections, and file descriptors
    to optimize node performance and prevent resource exhaustion. It is crucial for maintaining stability
    in the Filecoin network, especially for storage providers and critical nodes.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        service (str): The service or component to which the limits apply.
        limits (Dict[str, int]): Dictionary of resource limits to set. Valid keys are:
            - "Memory": Maximum memory allocation for network operations (in bytes)
            - "Streams": Total number of active streams (connections)
            - "StreamsInbound": Maximum number of incoming streams
            - "StreamsOutbound": Maximum number of outgoing streams
            - "Conns": Total number of connections
            - "ConnsInbound": Maximum number of incoming connections
            - "ConnsOutbound": Maximum number of outgoing connections
            - "FD": Maximum number of file descriptors

    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if the operation was successful, False otherwise.
            - str: Success message or error message if the operation failed.

    Example:
        >>> # Set only memory and streams limits
        >>> limits = {
        ...     "Memory": 1024 * 1024 * 1024,  # 1GB
        ...     "Streams": 100
        ... }
        >>> _set_limit(connector, "service1", limits)
        
        >>> # Set all possible limits
        >>> limits = {
        ...     "Memory": 2048 * 1024 * 1024,  # 2GB
        ...     "Streams": 200,
        ...     "StreamsInbound": 100,
        ...     "StreamsOutbound": 100,
        ...     "Conns": 500,
        ...     "ConnsInbound": 250,
        ...     "ConnsOutbound": 250,
        ...     "FD": 1000
        ... }
        >>> _set_limit(connector, "service2", limits)
    """
    if not limits:
        return False, "No limits specified"

    payload = _make_payload("Filecoin.NetSetLimit", [service, limits])
    dct_response = connector.execute(payload)
    if 'error' in dct_response:
        return False, dct_response['error']['message']
    else:
        return True, "Success"



# NetPubsubScores
def _pubsub_scores(connector: HttpJsonRpcConnector) -> Dict:
    """
    Retrieves the pubsub scores of the Lotus node.
    
    Returns:
        Dict: A dictionary containing pubsub scores for each peer. Each peer entry contains:
            - ID (str): The peer ID
            - Score (Dict): A dictionary containing score metrics:
                - AppSpecificScore (float): Application-specific score
                - BehaviourPenalty (float): Penalty for misbehavior
                - IPColocationFactor (float): Factor for IP colocation
                - Score (float): Overall score
                - Topics (Dict): Optional dictionary of topic-specific metrics for each topic:
                    - FirstMessageDeliveries (float): Score for first message deliveries
                    - InvalidMessageDeliveries (float): Penalty for invalid message deliveries
                    - MeshMessageDeliveries (float): Score for mesh message deliveries
                    - TimeInMesh (float): Score for time spent in mesh
    """
    payload = _make_payload("Filecoin.NetPubsubScores", [])
    dct_response = connector.execute(payload)
    return dct_response['result']


def _protect_list(connector: HttpJsonRpcConnector) -> List[str]:
    """
    Retrieves the list of protected peers from the Lotus node.

    This method queries the Lotus node to get a list of peer IDs that are currently
    protected from being disconnected. Protected peers are typically those that are
    critical for the node's operation, such as storage providers or other essential
    network participants.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.

    Returns:
        List[str]: A list of peer IDs that are currently protected from disconnection.
    """
    payload = _make_payload("Filecoin.NetProtectList", [])
    dct_response = connector.execute(payload)
    return dct_response['result']

def _protect_remove(connector: HttpJsonRpcConnector, peer_ids: List[str]) -> Tuple[bool, str]:
    """
    Removes specified peers from a protected set within the Filecoin network, allowing them to be disconnected.
    
    This method is useful for managing the protected peers list, allowing for dynamic updates to the set of protected nodes.    

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peer_ids (List[str]): List of peer IDs to remove from the protected set.

    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if the operation was successful, False otherwise
            - str: Success message or error message if the operation failed
    """
    payload = _make_payload("Filecoin.NetProtectRemove", [peer_ids])
    dct_response = connector.execute(payload)
    if 'error' in dct_response:
        return False, dct_response['error']['message']
    else:
        return True, "Success"


def _protect_add(connector: HttpJsonRpcConnector, peer_ids: List[str]) -> Tuple[bool, str]:
    """
    Adds specified peers to a protected set within the Filecoin network, preventing them from being disconnected.
    
    This method is crucial for maintaining stable and reliable connections, especially for storage providers
    and other critical nodes. By protecting these peers, it ensures that essential network interactions,
    such as data storage and retrieval operations, are not interrupted.
    
    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peer_ids (List[str]): List of peer IDs to add to the protected set.
        
    Returns:
        Tuple[bool, str]: A tuple containing:
            - bool: True if the operation was successful, False otherwise
            - str: Success message or error message if the operation failed
    """
    payload = _make_payload("Filecoin.NetProtectAdd", [peer_ids])
    dct_response = connector.execute(payload)
    if 'error' in dct_response:
        return False, dct_response['error']['message']
    else:
        return True, "Success"


def _ping(connector: HttpJsonRpcConnector, peer_id: str) -> int:
    """
    Pings a specific peer and returns the latency in nanoseconds.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peer_id (str): The ID of the peer to ping.
    """
    payload = _make_payload("Filecoin.NetPing", [peer_id])
    dct_response = connector.execute(payload)
    return int(dct_response['result'])


def _peer_info(connector: HttpJsonRpcConnector, peer_id: str) -> Dict:
    """
    Retrieves detailed information about a specific peer.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peer_id (str): The ID of the peer to retrieve information for.

    Returns:
        Dict: A dictionary containing detailed information about the peer.
    """
    payload = _make_payload("Filecoin.NetPeerInfo", [peer_id])
    dct_response = connector.execute(payload)
    return dct_response['result']


def _limit(connector: HttpJsonRpcConnector, limit: int) -> Dict:
    """
    Get or set resource limits for a scope.
    
    This function allows setting or retrieving resource limits for different scopes in the Lotus node.
    The scope can be one of the following:
    - system        -- reports the system aggregate resource usage
    - transient     -- reports the transient resource usage
    - svc:<service> -- reports the resource usage of a specific service
    - proto:<proto> -- reports the resource usage of a specific protocol
    - peer:<peer>   -- reports the resource usage of a specific peer
    
    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        limit (int): The resource limit to set for the specified scope.
        
    Returns:
        Dict: A dictionary containing the result of the operation, typically the current limits.
    """
    payload = _make_payload("Filecoin.NetLimit", [limit])
    dct_response = connector.execute(payload)
    return dct_response.get('result')


def _find_peer(connector: HttpJsonRpcConnector, peer_id: str) -> Dict:
    """
    Finds a peer in the network.
    """
    payload = _make_payload("Filecoin.NetFindPeer", [peer_id])
    dct_response = connector.execute(payload)
    return dct_response.get('result', False)


def _disconnect(connector: HttpJsonRpcConnector, peer_id: str) -> bool:
    """
    Disconnects from a specified peer.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peer_id (str): The ID of the peer to disconnect from.

    Returns:
        bool: True if the disconnection was successful, False otherwise.
    """
    payload = _make_payload("Filecoin.NetDisconnect", [peer_id])
    dct_response = connector.execute(payload)
    return dct_response.get('result', False)


def _connectedness(connector: HttpJsonRpcConnector, peer_id: str) -> Dict:
    """
    Retrieves the connectedness status of a specific peer.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peer_id (str): The ID of the peer to check connectedness for.

    Returns:
        Dict: A dictionary containing the connectedness status of the peer.
    """
    payload = _make_payload("Filecoin.NetConnectedness", [peer_id])
    dct_response = connector.execute(payload)
    return dct_response['result'] == 1


def _block_remove(connector: HttpJsonRpcConnector, peers: List[str] = None, ip_addrs: List[str] = None, ip_subnets: List[str] = None) -> bool:
    """
    Removes entries from the blocklist, allowing communication with previously blocked peers, IP addresses, or IP subnets.

    Note: This method requires admin privileges on the Lotus server.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peers (List[str], optional): List of peer IDs to remove from the block list.
        ip_addrs (List[str], optional): List of IP addresses to remove from the block list.
        ip_subnets (List[str], optional): List of IP subnets to remove from the block list.
        
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    block_params = {
        "Peers": peers or [],
        "IPAddrs": ip_addrs or [],
        "IPSubnets": ip_subnets or []
    }

    payload = _make_payload("Filecoin.NetBlockRemove", [block_params])
    dct_response = connector.execute(payload)
    return dct_response.get('result', False)


def _block_list(connector: HttpJsonRpcConnector) -> Dict:
    """
    Retrieves the list of blocked peers, IP addresses, and IP subnets from the Lotus node.

    This function queries the Lotus node for all entities that have been blocked from
    communicating with the node. The blocks may have been added using the _block_add method.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.

    Returns:
        Dict: A dictionary containing lists of blocked entities with the following structure:
            {
                "Peers": [str],       # List of blocked peer IDs
                "IPAddrs": [str],     # List of blocked IP addresses
                "IPSubnets": [str]    # List of blocked IP subnets
            }
    """
    payload = _make_payload("Filecoin.NetBlockList", [])
    dct_response = connector.execute(payload)
    return dct_response['result']


# Implement Filecoin.NetBlockAdd
def _block_add(connector: HttpJsonRpcConnector, peers: List[str] = None, ip_addrs: List[str] = None, ip_subnets: List[str] = None) -> bool:
    """
    Blocks communication with specific peers, IP addresses, or IP subnets.
    
    Note: This method requires admin privileges on the Lotus server.
    
    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peers (List[str], optional): List of peer IDs to block.
        ip_addrs (List[str], optional): List of IP addresses to block.
        ip_subnets (List[str], optional): List of IP subnets to block.
        
    Returns:
        bool: True if the operation was successful, False otherwise.
    """
    block_params = {
        "Peers": peers or [],
        "IPAddrs": ip_addrs or [],
        "IPSubnets": ip_subnets or []
    }

    payload = _make_payload("Filecoin.NetBlockAdd", [block_params])
    dct_response = connector.execute(payload)
    return dct_response.get('result', False)


def _bandwidth_stats_by_protocol(connector: HttpJsonRpcConnector) -> Dict:
    """
    Retrieves the bandwidth statistics of the Lotus node by protocol.
    """
    payload = _make_payload("Filecoin.NetBandwidthStatsByProtocol", [])
    dct_response = connector.execute(payload)
    return dct_response['result']


def _bandwidth_stats_by_peer(connector: HttpJsonRpcConnector) -> Dict:
    """
    Retrieves the bandwidth statistics of the Lotus node by peer.

    Returns:
        Dict: A dictionary containing the bandwidth statistics by peer.
    """
    payload = _make_payload("Filecoin.NetBandwidthStatsByPeer", [])
    dct_response = connector.execute(payload)
    return dct_response['result']


def _bandwidth_stats(connector: HttpJsonRpcConnector) -> Dict:
    """
    Retrieves the bandwidth statistics of the Lotus node.

    Returns:
        Dict: A dictionary containing the bandwidth statistics.
    """
    payload = _make_payload("Filecoin.NetBandwidthStats", [])
    dct_response = connector.execute(payload)
    return dct_response['result']


def _auto_nat_status(connector: HttpJsonRpcConnector) -> NatInfo:
    """
    Retrieves the auto NAT status of the Lotus node.

    Returns:
        NatInfo: An object containing the NAT status information including
                reachability status and public addresses.
    """
    payload = _make_payload("Filecoin.NetAutoNatStatus", [])
    dct_response = connector.execute(payload)
    return NatInfo.from_dict(dct_response['result'])


def _peers(connector: HttpJsonRpcConnector) -> List[AddressInfo]:
    """
    Retrieves the list of peers connected to the Lotus node.
    """
    payload = _make_payload("Filecoin.NetPeers", [])
    dct_response = connector.execute(payload)
    return [AddressInfo.from_dict(peer) for peer in dct_response['result']]


def _agent_version(connector: HttpJsonRpcConnector, peer_id: str) -> str:
    """
    Retrieves the version of the Lotus agent.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peer_id (str): The identifier of the peer whose agent version is being requested.

    Returns:
        str: The version string of the Lotus agent.

    """
    payload = _make_payload("Filecoin.NetAgentVersion", [peer_id])
    dct_response = connector.execute(payload)
    return dct_response['result']


def _addrs_listen(connector: HttpJsonRpcConnector) -> AddressInfo:
    """
    Retrieves the listening addresses of the Lotus node.

    Returns:
        AddressInfo: An object containing the listening addresses and peer ID.
    """
    payload = _make_payload("Filecoin.NetAddrsListen", [])
    dct_response = connector.execute(payload)
    address_info = AddressInfo.from_dict(dct_response['result'])
    return address_info


def _connect(connector: HttpJsonRpcConnector, peer_id: str, addrs: List[str]) -> bool:
    """
    Establishes a connection to a specified peer.

    This method attempts to connect the Lotus node to a peer using their ID and multiaddresses.
    If successful, the peer will be added to the node's peer list and communication
    can be established.

    Args:
        connector (HttpJsonRpcConnector): The JSON-RPC connector to communicate with the Lotus node.
        peer_id (str): The ID of the peer to connect to.
        addrs (List[str]): A list of multiaddresses associated with the peer.

    Returns:
        bool: True if the connection was successful, False otherwise.
    """
    peer_info = {
        "ID": peer_id,
        "Addrs": addrs
    }

    payload = _make_payload("Filecoin.NetConnect", [peer_info])
    dct_response = connector.execute(payload)

    return "error" not in dct_response
    