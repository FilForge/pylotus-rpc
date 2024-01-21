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
    _get_randomness_from_beacon,
    _list_actors,
    _read_state,
    _list_messages,
    _list_miners,
    _lookup_id,
    _market_balance,
    _market_participants,
    _storage_market_deal,
    _miner_active_sectors,
    _miner_available_balance,
    _miner_deadlines,
    _miner_faults,
    _miner_info,
    _miner_initial_pledge_collateral,
    _miner_partitions,
    _miner_power
)

from pylotus_rpc.methods.chain import (
    _get_chain_head
)

from pylotus_rpc.types.invocation_result import InvocationResult
from pylotus_rpc.types.cid import Cid
from pylotus_rpc.types.miner_power import MinerPower
from pylotus_rpc.types.actor_state import ActorState
from pylotus_rpc.types.state_compute_output import StateComputeOutput
from pylotus_rpc.types.message import Message
from pylotus_rpc.http_json_rpc_connector import HttpJsonRpcConnector
from pylotus_rpc.types.sector_pre_commit_info import SectorPreCommitInfo
from tests.test_common import parse_fullnode_api_info


good_msg = Message(
    version=0,  # Always 0 for now, as per Filecoin protocol
    to_addr="f086971",  # Destination address
    from_addr="f01986715",  # Source address
    nonce=5,  # Assume this sender has sent 4 messages previously, so this is the 5th message.
    value=10**19,  # Transfer 10 FIL (as attoFIL)
    gas_limit=1000000,  # A generous gas limit; in practice, one should estimate this
    gas_fee_cap=1,  # Maximum price per gas unit this sender is willing to pay
    gas_premium=5,  # Willing to pay half of GasFeeCap as a premium for faster inclusion
    method=0,  # Method 0 is a simple fund transfer in Filecoin
    params=""  # No params needed for simple transfers
)    

good_msg2 = Message(
    version=0,  # Always 0 for now, as per Filecoin protocol
    to_addr="f086971",  # Destination address
    from_addr="f01986715",  # Source address
    nonce=7,  # Assume this sender has sent 4 messages previously, so this is the 5th message.
    value=10**19,  # Transfer 10 FIL (as attoFIL)
    gas_limit=1000000,  # A generous gas limit; in practice, one should estimate this
    gas_fee_cap=1,  # Maximum price per gas unit this sender is willing to pay
    gas_premium=5,  # Willing to pay half of GasFeeCap as a premium for faster inclusion
    method=0,  # Method 0 is a simple fund transfer in Filecoin
    params=""  # No params needed for simple transfers
)    

# JSON string
spci_json_str = '''
{
    "SealProof": 8,
    "SectorNumber": 9,
    "SealedCID": {
      "/": "bafy2bzacea3wsdh6y3a36tb3skempjoxqpuyompjbmfeyf34fi3uy6uue42v4"
    },
    "SealRandEpoch": 10101,
    "DealIDs": [
      5432
    ],
    "Expiration": 10101,
    "ReplaceCapacity": true,
    "ReplaceSectorDeadline": 42,
    "ReplaceSectorPartition": 42,
    "ReplaceSectorNumber": 9
}
'''


@pytest.fixture
def setup_filfox_connector():
    host = "https://filfox.info/rpc/v1"
    return HttpJsonRpcConnector(host=host)

@pytest.fixture
def setup_connector():
    host = os.environ.get('LOTUS_GATEWAY', 'https://filfox.info/rpc/v1')
    return HttpJsonRpcConnector(host=host)

@pytest.mark.integration
def test_miner_power(setup_connector):
    # you can get a miner address to test with from https://filfox.info/en/ranks/power
    result = _miner_power(setup_connector, "f02244985", tipset=None)
    assert result is not None
    assert isinstance(result, MinerPower)
    assert result.miner_power is not None
    assert result.total_power is not None
    assert result.has_min_power is not None

@pytest.mark.integration
def test_miner_partitions(setup_connector):
    # you can get a miner address to test with from https://filfox.info/en/ranks/power
    list_result = _miner_partitions(setup_connector, "f02244985", 0, tipset=None)
    assert list_result is not None
    assert len(list_result) > 0
    assert list_result[0].all_sectors is not None
    assert list_result[0].faulty_sectors is not None
    assert list_result[0].recovering_sectors is not None
    assert list_result[0].live_sectors is not None
    assert list_result[0].active_sectors is not None

@pytest.mark.integration
def test_miner_initial_pledge_collateral(setup_connector):
    # you can get a miner address to test with from https://filfox.info/en/ranks/power
    sector_pre_commit_info = SectorPreCommitInfo.from_json(spci_json_str)
    result = _miner_initial_pledge_collateral(setup_connector, "f02244985", sector_pre_commit_info, tipset=None)
    assert result is not None
    assert isinstance(result, int)

@pytest.mark.integration
def test_miner_info(setup_connector):
    # you can get a miner address to test with from https://filfox.info/en/ranks/power
    result = _miner_info(setup_connector, "f02244985", tipset=None)
    assert result is not None
    assert result.owner is not None
    assert result.worker is not None
    assert result.peer_id is not None
    assert result.multiaddrs is not None
    assert result.sector_size > 0
    assert result.window_post_partition_sectors > 0
    assert result.beneficiary is not None
    assert result.beneficiary_term is not None
    assert result.beneficiary_term.quota is not None
    assert result.beneficiary_term.used_quota is not None

@pytest.mark.integration
def test_miner_faults(setup_connector):
    # you can get a miner address to test with from https://filfox.info/en/ranks/power
    list_result = _miner_faults(setup_connector, "f02244985", tipset=None)
    assert list_result is not None
    assert len(list_result) > 0

@pytest.mark.integration
def test_miner_deadlines(setup_connector):
    # you can get a miner address to test with from https://filfox.info/en/ranks/power
    result = _miner_deadlines(setup_connector, "f02244985", tipset=None)
    assert result is not None
    assert len(result) > 0

@pytest.mark.integration
def test_miner_available_balance(setup_connector):
    # you can get a miner address to test with from https://filfox.info/en/ranks/power
    result = _miner_available_balance(setup_connector, "f02244985", tipset=None)
    assert result is not None
    assert isinstance(result, int)

@pytest.mark.integration
def test_miner_active_sectors(setup_connector):
    # you can get a miner address to test with from https://filfox.info/en/ranks/power
    result = _miner_active_sectors(setup_connector, "f02244985", tipset=None)
    assert result is not None
    assert len(result) > 0

@pytest.mark.integration
def test_storage_market_deal(setup_connector):
    # You can get a deal id to test with from https://filfox.info/en/deal
    result = _storage_market_deal(setup_connector, 68901592, tipset=None)
    assert result is not None
    assert result['State'] is not None
    assert result['Proposal'] is not None
    assert result['Proposal'].piece_size > 0


@pytest.mark.integration
def test_market_participants(setup_connector):
    result = _market_participants(setup_connector, tipset=None)
    assert result is not None
    assert len(result) > 0


@pytest.mark.integration
def test_market_balance(setup_connector):
    result = _market_balance(setup_connector, "f02620", tipset=None)
    assert result is not None
    assert result['Escrow'] > 0
    assert result['Locked'] > 0

@pytest.mark.integration
def test_lookup_id(setup_connector):
    result = _lookup_id(setup_connector, "f1gdqsyh2twcmimfujjkgajqccx6v4bbywy33xpuq", tipset=None)
    assert result is not None
    assert result == "f02914334"

@pytest.mark.integration
def test_list_miners(setup_connector):
    result = _list_miners(setup_connector, tipset=None)
    assert result is not None
    assert len(result) > 0


@pytest.mark.integration
def test_list_messages(setup_connector):
    tipset = _get_chain_head(setup_connector)
    # test by getting all messages sent to the storage market actor
    result = _list_messages(setup_connector, "f05", None, tipset.height, tipset=tipset)
    assert result is not None
    assert len(result) > 0


@pytest.mark.integration
def test_read_state(setup_connector):
    result = _read_state(setup_connector, "f05")
    assert result is not None
    assert isinstance(result, ActorState)
    assert result.balance > 0
    assert result.code is not None
    assert result.state is not None


@pytest.mark.integration
def test_state_list_actors(setup_filfox_connector):
    result = _list_actors(setup_filfox_connector, tipset=None)
    assert result is not None
    assert len(result) > 0

@pytest.mark.integration
def test_get_randomness_from_beacon(setup_filfox_connector):
    result = _get_randomness_from_beacon(setup_filfox_connector, 2, 10101, "Ynl0ZSBhcnJheQ==", tipset=None)
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


@pytest.mark.integration
def test_state_circulating_supply(setup_connector):
    tipset = _get_chain_head(setup_connector)
    circulating_supply = _circulating_supply(setup_connector, tipset=tipset)
    assert circulating_supply > 0


@pytest.mark.integration
def test_state_call_returned_values(setup_connector):
    tipset = _get_chain_head(setup_connector)
    invocation_result = _state_call(setup_connector, good_msg, tipset=tipset)

    assert isinstance(invocation_result, InvocationResult)
    assert invocation_result.msg_receipt.exit_code == 0  # No error in execution
    assert invocation_result.duration > 0  # Duration should be greater than zero for any call

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
        version=28,
        to_addr="f01234",  # Destination address
        from_addr="f01234",  # Source address
        nonce=5,  # Assume this sender has sent 4 messages previously, so this is the 5th message.
        value=10**19,  # Transfer 10 FIL (as attoFIL)
        gas_limit=1000000,  # A generous gas limit; in practice, one should estimate this
        gas_fee_cap=1,  # Maximum price per gas unit this sender is willing to pay
        gas_premium=5,  # Willing to pay half of GasFeeCap as a premium for faster inclusion
        method=0,  # Method 0 is a simple fund transfer in Filecoin
        params=""  # No params needed for simple transfers
    )

    invoc_result = _state_call(setup_connector, bad_msg, tipset=None)
    assert invoc_result.error  # Ensure error is returned

@pytest.mark.integration
def test_state_call_gas_charges(setup_connector):
    tipset = _get_chain_head(setup_connector)
    invocation_result = _state_call(setup_connector, good_msg, tipset=tipset)
    assert invocation_result.execution_trace.gas_charges  # Ensure gas charges are returned
    for gas_charge in invocation_result.execution_trace.gas_charges:
        assert gas_charge.total_gas >= 0
        assert gas_charge.compute_gas >= 0
        assert gas_charge.storage_gas >= 0

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
    assert isinstance(actor.code, Cid)
    assert isinstance(actor.head, Cid)
    assert isinstance(actor.nonce, int)
    assert isinstance(actor.balance, str)

@pytest.mark.integration
def test_get_actor_failure():
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _get_actor(faulty_connector, "f05")

