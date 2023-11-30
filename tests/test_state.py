import pytest
import os

from pylotus_rpc.methods.state import (
    _state_compute,
    _get_actor,
    _account_key,
    _state_call,
    _circulating_supply,
    _deal_provider_collateral_bounds,
    _decode_params,
    _get_randomness_from_beacon
)

from pylotus_rpc.methods.chain import (
    _get_chain_head
)

from pylotus_rpc.types.invocation_result import InvocationResult
from pylotus_rpc.types.cid import Cid
from pylotus_rpc.types.StateComputeOutput import StateComputeOutput
from pylotus_rpc.types.message import Message
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

good_msg2 = Message(
    Version=0,  # Always 0 for now, as per Filecoin protocol
    To="f086971",  # Destination address
    From="f01986715",  # Source address
    Nonce=7,  # Assume this sender has sent 4 messages previously, so this is the 5th message.
    Value=10**19,  # Transfer 10 FIL (as attoFIL)
    GasLimit=1000000,  # A generous gas limit; in practice, one should estimate this
    GasFeeCap=1,  # Maximum price per gas unit this sender is willing to pay
    GasPremium=5,  # Willing to pay half of GasFeeCap as a premium for faster inclusion
    Method=0,  # Method 0 is a simple fund transfer in Filecoin
    Params=""  # No params needed for simple transfers
)    


@pytest.fixture
def setup_connector():
    # TODO - use environment variable for host
    host = "http://lotus.filforge.io:1234/rpc/v0"
    # host = "https://filfox.info/rpc/v1"
    return HttpJsonRpcConnector(host=host)

def test_get_randomness_from_beacon(setup_connector):
    result = _get_randomness_from_beacon(setup_connector, 2, 10101, "Ynl0ZSBhcnJheQ==", tipset=None)
    assert result is not None
    assert len(result) > 0
    assert result == "Qg+/Ia8AQK+6Wf6rdET3tO3DYjZdDxMYAND/Mazu6Pc="

@pytest.mark.integration
def test_deal_provider_collateral_bounds(setup_connector):
    [min, max] = _deal_provider_collateral_bounds(setup_connector, 34359738368, False, tipset=None)
    assert min > 0
    assert max > 0


@pytest.mark.integration
def test_decode_params(setup_connector):
    data = _decode_params(setup_connector, "f05", 6, "goEaA5wJ/BoASmsX", tipset=None)
    assert data is not None
    assert len(data) > 0


@pytest.mark.integration
def test_state_compute(setup_connector):
    # Prepare test data
    tipset = _get_chain_head(setup_connector)
    lst_messages  = [good_msg, good_msg2]

    # Call the function under test
    result = _state_compute(setup_connector, tipset.height, lst_messages, tipset=tipset)

    # Assertions to validate the function's behavior
    assert result is not None
    assert isinstance(result, StateComputeOutput)
    assert result.root is not None
    assert len(result.trace) > 1

# TODO - this one times out, find out why
#@pytest.mark.integration
#def test_state_circulating_supply(setup_connector):
#    tipset = _get_chain_head(setup_connector)
#    circulating_supply = _circulating_supply(setup_connector, tipset=tipset)
#    assert circulating_supply > 0

@pytest.mark.integration
def test_state_call_returned_values(setup_connector):
    tipset = _get_chain_head(setup_connector)
    invocation_result = _state_call(setup_connector, good_msg, tipset=tipset)

    assert isinstance(invocation_result, InvocationResult)
    assert invocation_result.MsgRct.ExitCode == 0  # No error in execution
    assert invocation_result.Duration > 0  # Duration should be greater than zero for any call

@pytest.mark.integration
def test_state_call_execution_error(setup_connector):
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')

    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _state_call(faulty_connector, good_msg, tipset=None)

@pytest.mark.integration
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
    assert invoc_result.Error  # Ensure error is returned

@pytest.mark.integration
def test_state_call_gas_charges(setup_connector):
    tipset = _get_chain_head(setup_connector)
    invocation_result = _state_call(setup_connector, good_msg, tipset=tipset)
    assert invocation_result.ExecutionTrace.GasCharges  # Ensure gas charges are returned
    for gas_charge in invocation_result.ExecutionTrace.GasCharges:
        assert gas_charge.TotalGas >= 0
        assert gas_charge.ComputeGas >= 0
        assert gas_charge.StorageGas >= 0

@pytest.mark.integration
def test_get_account_key_success_with_tipset(setup_connector):
    tipset = _get_chain_head(setup_connector)
    address = _account_key(setup_connector, "f047684", tipset=tipset)
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(address, Cid)
    assert len(address.id) > 0

@pytest.mark.integration
def test_get_account_key_success(setup_connector):
    tipset = _get_chain_head(setup_connector)
    address = _account_key(setup_connector, "f047684", tipset=None)
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(address, Cid)
    assert len(address.id) > 0

@pytest.mark.integration
def test_get_account_key_failure():
# Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _account_key(faulty_connector, "f047684")

@pytest.mark.integration
def test_get_actor_success(setup_connector):
    actor = _get_actor(setup_connector, "f05")
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(actor.Code, Cid)
    assert isinstance(actor.Head, Cid)
    assert isinstance(actor.Nonce, int)
    assert isinstance(actor.Balance, str)

@pytest.mark.integration
def test_get_actor_failure():
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _get_actor(faulty_connector, "f05")

