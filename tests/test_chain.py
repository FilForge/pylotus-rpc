import pytest
from pylotus_rpc.methods.chain import _get_block
from pylotus_rpc.http_json_rpc_connector import HttpJsonRpcConnector
from pylotus_rpc.types.block_header import BlockHeader
from pylotus_rpc.types.cid import Cid

from pylotus_rpc.methods.chain import (
    _get_chain_head,
    _get_tip_set,
    _read_obj,
    _get_block_messages,
    _get_genesis,
    _get_message,
    _get_messages_in_tipset,
    _get_node,
    _get_parent_messages
)

from pylotus_rpc.methods.state import (
    _read_state,
    _get_actor
)

@pytest.fixture
def setup_connector():
    host = "https://filfox.info/rpc/v1"
    return HttpJsonRpcConnector(host=host)


@pytest.fixture(scope="module")
def block_cid():
    # Use a known block CID for testing purposes. Replace this with an actual CID.
    return "bafy2bzacecljxqjgcw2ebuoo2se4hl7vck33civl5k6cuwj434fat7sh6oo3a"


@pytest.mark.integration
def test_get_parent_messages(setup_connector):
    test_tipset = _get_chain_head(setup_connector)
    parent_messages = _get_parent_messages(setup_connector, test_tipset.cids[0].id)
    assert parent_messages is not None
    assert len(parent_messages) > 0


@pytest.mark.integration
def test_get_node(setup_connector):
    test_tipset = _get_chain_head(setup_connector)
    test_actor = _get_actor(setup_connector, "f05", tipset=test_tipset)
    node_path_selector = f"{test_actor.head.id}/6"
    dct_node_data = _get_node(setup_connector, node_path_selector=node_path_selector)
    assert dct_node_data is not None


@pytest.mark.integration
def test_get_messages_in_tipset(setup_connector):
    test_tipset = _get_chain_head(setup_connector)
    messages = _get_messages_in_tipset(setup_connector, test_tipset.get_tip_set_key())
    assert messages is not None
    assert len(messages) > 0

@pytest.mark.integration
def test_get_message(setup_connector):
    # get the tipset
    test_tipset = _get_chain_head(setup_connector)
    # get the cid of the first block in the tipset
    first_block_cid = test_tipset.cids[0]
    # get all the messages for that block
    block_messages = _get_block_messages(setup_connector, first_block_cid.id)
    # redundant, but for testing, get the first message from get_message
    message_cid = block_messages.cids[0].id
    message = _get_message(setup_connector, message_cid.id)
    assert message is not None
    assert message.from_addr is not None
    assert message.to_addr is not None


@pytest.mark.integration
def test_get_genesis(setup_connector):
    tipset_genesis = _get_genesis(setup_connector)
    assert tipset_genesis is not None
    assert tipset_genesis.height == 0


@pytest.mark.integration
def test_get_block_messages(setup_connector):
    test_tipset = _get_chain_head(setup_connector)
    first_block_cid = test_tipset.cids[0]
    block_messages = _get_block_messages(setup_connector, first_block_cid.id)
    assert block_messages is not None
    assert len(block_messages.bls_messages) > 0
    assert len(block_messages.secpk_messages) > 0


@pytest.mark.integration
def test_get_tip_set(setup_connector):
    test_tipset = _get_chain_head(setup_connector)
    result_tipset = _get_tip_set(setup_connector, test_tipset.get_tip_set_key())
    assert result_tipset is not None
    assert result_tipset.height == test_tipset.height

@pytest.mark.integration
def test_read_obj(setup_connector):
    # test with the locked table data from the market actor at the current tipset
    result = _read_state(setup_connector, "f05")
    lt_cid = Cid.from_dict(result.state['LockedTable'])
    cbor_obj = _read_obj(setup_connector, lt_cid.id)
    assert cbor_obj is not None

@pytest.mark.integration
def test_get_chain_head_failure():
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _get_chain_head(faulty_connector)


@pytest.mark.integration
def test_get_chain_head_success(setup_connector):
    tipset = _get_chain_head(setup_connector)
    
    # Basic checks to see if the returned object is correctly formed
    assert isinstance(tipset.height, int)
    assert len(tipset.cids) > 0
    assert len(tipset.blocks) > 0

@pytest.mark.integration
def test_get_block(setup_connector, block_cid):
    block_header = _get_block(setup_connector, block_cid)
    
    # Assert that the returned object is an instance of BlockHeader
    assert isinstance(block_header, BlockHeader), "The returned object is not a BlockHeader instance"

    # checking the block height:
    expected_height = 3354396
    assert block_header.height == expected_height, f"Block height {block_header.height} does not match expected {expected_height}"
    
    # checking the miner address:
    expected_miner_address = "f02250603"
    assert block_header.miner == expected_miner_address, f"Miner address {block_header.miner} does not match expected {expected_miner_address}"
