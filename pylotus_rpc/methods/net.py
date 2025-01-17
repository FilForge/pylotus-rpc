from ..http_json_rpc_connector import HttpJsonRpcConnector
from typing import List
from ..types.address_info import AddressInfo

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


def _peers(connector: HttpJsonRpcConnector) -> List[AddressInfo]:
    """
    Retrieves the list of peers connected to the Lotus node.
    """
    payload = _make_payload("Filecoin.NetPeers", [])
    dct_response = connector.execute(payload)
    return [AddressInfo.from_dict(peer) for peer in dct_response['result']]


def _agent_version(connector: HttpJsonRpcConnector) -> str:
    """
    Retrieves the version of the Lotus agent.
    """
    payload = _make_payload("Filecoin.NetAgentVersion", [])
    dct_response = connector.execute(payload, debug=True)
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
    