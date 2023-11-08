import pytest
import os
from pylotus_rpc.methods.state import _get_chain_head, _get_actor, _account_key, _state_call
from pylotus_rpc.types.InvocationResult import InvocationResult
from pylotus_rpc.types.Cid import Cid
from pylotus_rpc.types.Message import Message
from pylotus_rpc.HttpJsonRpcConnector import HttpJsonRpcConnector
from tests.test_common import parse_fullnode_api_info


good_msg = Message(
    Version=0,  # Always 0 for now, as per Filecoin protocol
    To="f086971",  # Destination address
    From="f01986715",  # Source address
    Nonce=5,  # Assume this sender has sent 4 messages previously, so this is the 5th message.
    Value=10**19,  # Transfer 10 FIL (as attoFIL)
    GasLimit=1000000,  # A generous gas limit; in practice, one should estimate this
    GasFeeCap=1,  # Maximum price per gas unit this sender is willing to pay
    GasPremium=5,  # Willing to pay half of GasFeeCap as a premium for faster inclusion
    Method=0,  # Method 0 is a simple fund transfer in Filecoin
    Params=""  # No params needed for simple transfers
)    

@pytest.fixture
def setup_connector():
    dct_node_info = parse_fullnode_api_info()
    host = dct_node_info["host"]
    port = dct_node_info["port"]
    api_token = dct_node_info["jwt_token"]
    return HttpJsonRpcConnector(host, port, api_token)

def test_state_call_returned_values(setup_connector):
    tipset = _get_chain_head(setup_connector)
    invocation_result = _state_call(setup_connector, good_msg, tipset=tipset)

    assert isinstance(invocation_result, InvocationResult)
    assert invocation_result.MsgRct.ExitCode == 0  # No error in execution
    assert invocation_result.Duration > 0  # Duration should be greater than zero for any call

def test_state_call_execution_error(setup_connector):
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')

    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _state_call(faulty_connector, good_msg, tipset=None)


def test_state_call_message_error(setup_connector):
    # Create a message that you expect will fail when executed
    bad_msg = Message(
        Version=28,
        To="f01234",  # Destination address
        From="f01234",  # Source address
        Nonce=5,  # Assume this sender has sent 4 messages previously, so this is the 5th message.
        Value=10**19,  # Transfer 10 FIL (as attoFIL)
        GasLimit=1000000,  # A generous gas limit; in practice, one should estimate this
        GasFeeCap=1,  # Maximum price per gas unit this sender is willing to pay
        GasPremium=5,  # Willing to pay half of GasFeeCap as a premium for faster inclusion
        Method=0,  # Method 0 is a simple fund transfer in Filecoin
        Params=""  # No params needed for simple transfers
    )

    invoc_result = _state_call(setup_connector, bad_msg, tipset=None)
    assert invoc_result.MsgRct.ExitCode == 6  #detect error in execution
    
# Test Check Gas Charges
def test_state_call_gas_charges(setup_connector):
    tipset = _get_chain_head(setup_connector)
    invocation_result = _state_call(setup_connector, good_msg, tipset=tipset)
    assert invocation_result.ExecutionTrace.GasCharges  # Ensure gas charges are returned
    for gas_charge in invocation_result.ExecutionTrace.GasCharges:
        assert gas_charge.TotalGas >= 0
        assert gas_charge.ComputeGas >= 0
        assert gas_charge.StorageGas >= 0

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
    
    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _account_key(faulty_connector, "f047684")

def test_get_actor_success(setup_connector):
    actor = _get_actor(setup_connector, "f05")
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(actor.Code, Cid)
    assert isinstance(actor.Head, Cid)
    assert isinstance(actor.Nonce, int)
    assert isinstance(actor.Balance, str)

def test_get_actor_failure():
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
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
    
    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _get_chain_head(faulty_connector)


