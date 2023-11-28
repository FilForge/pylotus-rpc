import pytest
from pylotus_rpc.methods.chain import _get_block
from pylotus_rpc.HttpJsonRpcConnector import HttpJsonRpcConnector
from pylotus_rpc.types.BlockHeader import BlockHeader, dict_to_blockheader
from tests.test_common import parse_fullnode_api_info
from pylotus_rpc.methods.chain import (
    _get_chain_head
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
