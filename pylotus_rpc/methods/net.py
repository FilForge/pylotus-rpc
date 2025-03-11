from ..http_json_rpc_connector import HttpJsonRpcConnector
from typing import List, Dict
from ..types.address_info import AddressInfo
from ..types.nat_info import NatInfo

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
    