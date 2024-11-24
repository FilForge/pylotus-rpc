import pytest
from pylotus_rpc.methods.chain import _get_block
from pylotus_rpc.http_json_rpc_connector import HttpJsonRpcConnector
from pylotus_rpc.types.block_header import BlockHeader
from pylotus_rpc.types.cid import Cid

from pylotus_rpc.methods.chain import (
    _head,
    _get_tip_set,
    _read_obj,
    _get_block_messages,
    _get_genesis,
    _get_message,
    _get_messages_in_tipset,
    _get_node,
    _get_parent_messages,
    _get_parent_receipts,
    _get_tipset_by_height,
    _get_path,
    _get_randomness_from_beacon,
    _get_randomness_from_tickets,
    _has_obj,
    _tip_set_weight
)

from pylotus_rpc.methods.state import (
    _read_state,
    _get_actor
)

@pytest.fixture
def setup_connector():
    host = "https://filfox.io/rpc/v0"
    return HttpJsonRpcConnector(host=host)

@pytest.fixture
def setup_connector_v1():
    host = "https://filfox.io/rpc/v1"
    return HttpJsonRpcConnector(host=host)

@pytest.fixture(scope="module")
def block_cid():
    # Use a known block CID for testing purposes. Replace this with an actual CID.
    return "bafy2bzacecljxqjgcw2ebuoo2se4hl7vck33civl5k6cuwj434fat7sh6oo3a"

@pytest.mark.integration
def test_tip_set_weight(setup_connector):
    tipset_key = _head(setup_connector).get_tip_set_key()
    result = _tip_set_weight(setup_connector, tipset_key)
    assert result is not None
    assert result > 0

@pytest.mark.integration
def test_has_obj(setup_connector):
    result = _has_obj(setup_connector, "bafy2bzaceawwl2d3byzcijj4arjwxnzawnuhlc4qn5gwuhagc4yzpntffomp6")
    assert result is True

@pytest.mark.integration
def test_get_randomness_from_tickets(setup_connector):
    tipset = _head(setup_connector)
    result = _get_randomness_from_tickets(setup_connector, 2, 10101, "Ynl0ZSBhcnJheQ==", tipset=tipset)
    assert result is not None
    assert len(result) > 0
    assert result == "Az/dMpZP1FcRNAnjkDKOaIeW4rPhDI+UGRu1nSqF+1A="


@pytest.mark.integration
def test_get_randomness_from_beacon(setup_connector):
    result = _get_randomness_from_beacon(setup_connector, 2, 10101, "Ynl0ZSBhcnJheQ==", tipset=None)
    assert result is not None
    assert len(result) > 0
    assert result == "Qg+/Ia8AQK+6Wf6rdET3tO3DYjZdDxMYAND/Mazu6Pc="

@pytest.mark.integration
def test_get_path(setup_connector):
    end_tipset = _head(setup_connector)
    start_tipset = _get_tipset_by_height(setup_connector, end_tipset.height - 3)
    lst_head_changes = _get_path(setup_connector, start_tipset.get_tip_set_key(), end_tipset.get_tip_set_key())
    assert lst_head_changes is not None
    assert len(lst_head_changes) == 3


@pytest.mark.integration
def test_get_tipset_by_height(setup_connector):
    tipset = _get_tipset_by_height(setup_connector, 3354396)
    assert tipset is not None
    assert tipset.height == 3354396


@pytest.mark.integration
def test_get_parent_receipts(setup_connector):
    test_tipset = _head(setup_connector)
    parent_receipts = _get_parent_receipts(setup_connector, test_tipset.cids[0].id)
    assert parent_receipts is not None
    assert len(parent_receipts) > 0


@pytest.mark.integration
def test_get_parent_messages(setup_connector):
    test_tipset = _head(setup_connector)
    parent_messages = _get_parent_messages(setup_connector, test_tipset.cids[0].id)
    assert parent_messages is not None
    assert len(parent_messages) > 0


@pytest.mark.integration
def test_get_node(setup_connector):
    test_tipset = _head(setup_connector)
    test_actor = _get_actor(setup_connector, "f05", tipset=test_tipset)
    node_path_selector = f"{test_actor.head.id}/6"
    dct_node_data = _get_node(setup_connector, node_path_selector=node_path_selector)
    assert dct_node_data is not None


@pytest.mark.integration
def test_get_messages_in_tipset(setup_connector):
    test_tipset = _head(setup_connector)
    messages = _get_messages_in_tipset(setup_connector, test_tipset.get_tip_set_key())
    assert messages is not None
    assert len(messages) > 0

@pytest.mark.integration
def test_get_message(setup_connector):
    # get the tipset
    test_tipset = _head(setup_connector)
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
    test_tipset = _head(setup_connector)
    first_block_cid = test_tipset.cids[0]
    block_messages = _get_block_messages(setup_connector, first_block_cid.id)
    assert block_messages is not None
    assert len(block_messages.bls_messages) > 0
    assert len(block_messages.secpk_messages) > 0


@pytest.mark.integration
def test_get_tip_set(setup_connector):
    test_tipset = _head(setup_connector)
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
def test_head_failure():
    # Let's use wrong port or token to force an error
    faulty_connector = HttpJsonRpcConnector('localhost', 9999, 'INVALID_TOKEN')
    
    with pytest.raises(HttpJsonRpcConnector.ApiCallError):
        _head(faulty_connector)


@pytest.mark.integration
def test_head_success(setup_connector):
    tipset = _head(setup_connector)
    
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
