import pytest
import os

from pylotus_rpc.methods.net import (
    _addrs_listen,
    _agent_version,
    _auto_nat_status,
    _bandwidth_stats,
    _bandwidth_stats_by_peer,
    _bandwidth_stats_by_protocol,
    _block_list,
    _peers,
    _connectedness,
    _find_peer,
    _limit
)

from pylotus_rpc.http_json_rpc_connector import HttpJsonRpcConnector

@pytest.fixture
def connector():
    host = os.environ.get('LOTUS_GATEWAY', 'https://filfox.info/rpc/v0')
    return HttpJsonRpcConnector(host=host)

@pytest.mark.integration
def test_limit(connector):
    result = _limit(connector, "system")
    assert result is not None
    assert result['Memory'] > 0

@pytest.mark.integration
def test_block_list(connector):
    result = _block_list(connector)
    assert result is not None
    assert len(result) > 0

@pytest.mark.integration
def test_bandwidth_stats_by_protocol(connector):
    result = _bandwidth_stats_by_protocol(connector)
    assert result is not None
    assert len(result) > 0

@pytest.mark.integration
def test_bandwidth_stats_by_peer(connector):
    result = _bandwidth_stats_by_peer(connector)
    assert result is not None
    assert len(result) > 0

@pytest.mark.integration
def test_bandwidth_stats(connector):
    result = _bandwidth_stats(connector)
    assert result is not None
    assert result['TotalIn'] > 0
    assert result['TotalOut'] > 0

@pytest.mark.integration
def test_auto_nat_status(connector):
    result = _auto_nat_status(connector)
    assert result is not None
    assert result.reachability == 1
    assert result.public_addrs is not None
    assert len(result.public_addrs) > 0

@pytest.mark.integration
def test_agent_version(connector):
    peers = _peers(connector)
    result = _agent_version(connector, peers[0].peer_id)
    assert result is not None
    assert len(result) > 0

@pytest.mark.integration
def test_addrs_listen(connector):
    result = _addrs_listen(connector)
    assert result is not None
    
@pytest.mark.integration
def test_peers(connector):
    result = _peers(connector)
    assert result is not None
    assert len(result) > 0

@pytest.mark.integration
def test_connectedness(connector):
    peers = _peers(connector)
    result = _connectedness(connector, peers[0].peer_id)
    assert result is not None
    assert result == True

@pytest.mark.integration
def test_find_peer(connector):
    peers = _peers(connector)
    result = _find_peer(connector, peers[0].peer_id)
    assert result is not None