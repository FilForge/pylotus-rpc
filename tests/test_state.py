import pytest
import os
from pylotus_rpc.methods.state import _get_chain_head, _get_actor, ApiCallError, _account_key
from pylotus_rpc.types.Cid import Cid
from pylotus_rpc.HttpJsonRpcConnector import HttpJsonRpcConnector

@pytest.fixture
def setup_connector():
    dct_node_info = parse_fullnode_api_info()
    host = dct_node_info["host"]
    port = dct_node_info["port"]
    api_token = dct_node_info["jwt_token"]
    return HttpJsonRpcConnector(host, port, api_token)

def test_get_account_key_success_with_tipset(setup_connector):
    tipset = _get_chain_head(setup_connector)
    address = _account_key(setup_connector, "f047684", tipset=tipset)
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(address, Cid)
    assert len(address.id) > 0

def test_get_account_key_success(setup_connector):
    tipset = _get_chain_head(setup_connector)
    address = _account_key(setup_connector, "f047684", tipset=None)
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(address, Cid)
    assert len(address.id) > 0

def test_get_account_key_failure():
# Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(ApiCallError):
        _account_key(faulty_connector, "f047684")

def test_get_actor_success(setup_connector):
    actor = _get_actor(setup_connector, "f05")
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(actor.Code, Cid)
    assert isinstance(actor.Head, Cid)
    assert isinstance(actor.Nonce, int)
    assert isinstance(actor.Balance, int)

def test_get_actor_failure():
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(ApiCallError):
        _get_actor(faulty_connector, "f05")

def test_get_chain_head_success(setup_connector):
    tipset = _get_chain_head(setup_connector)
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(tipset.height, int)
    assert len(tipset.cids) > 0
    assert len(tipset.blocks) > 0

def test_get_chain_head_failure():
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(ApiCallError):
        _get_chain_head(faulty_connector)

def parse_fullnode_api_info():
    # Try to fetch the environment variable
    fullnode_api_info = os.environ.get("FULLNODE_API_INFO")
    
    # If it's not found, raise an error
    if not fullnode_api_info:
        raise EnvironmentError("FULLNODE_API_INFO environment variable is not set.")
    
    # Split the info at the ':' to separate JWT token and address
    jwt_token, address = fullnode_api_info.split(":", 1)

    # Extract the host by splitting the address string and taking the appropriate section
    parts = address.split("/")
    port = parts[4]
    host = parts[2]
    
    return {
        "jwt_token": jwt_token,
        "host": host,
        "port": port
    }
