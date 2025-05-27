# PyLotus-RPC

PyLotus-RPC is a Python client library for interacting with the Lotus JSON-RPC API. It provides a convenient way to communicate with Filecoin nodes from your Python applications.

This codebase is still a WIP. All Filecoin.StateXXXX, Filecoin.ChainXXX, and Filecoin.NetXXX calls have been implemented. Other methods are being added over time.

<a href="https://filecoin.drips.network/app/projects/github/FilForge/pylotus-rpc" target="_blank"><img src="https://filecoin.drips.network/api/embed/project/https%3A%2F%2Fgithub.com%2FFilForge%2Fpylotus-rpc/support.png?background=light&style=github&text=project&stat=none" alt="Support pylotus-rpc on drips.network" height="20"></a>

## Installation

```shell
pip install pylotus-rpc
```

## Quick Start

The `LotusClient` provides access to Filecoin blockchain data through Chain, State, and Net APIs. All methods require an `HttpJsonRpcConnector` for communication with Lotus nodes.

### Basic Setup

```python
from pylotus_rpc import LotusClient, HttpJsonRpcConnector

# Connect to a public Filecoin node
connector = HttpJsonRpcConnector(host='https://api.node.glif.io/rpc/v0')
client = LotusClient(connector)

# Or connect to your local Lotus node with authentication
connector = HttpJsonRpcConnector(
    host='http://localhost:1234/rpc/v0',
    api_token='your_lotus_api_token'
)
client = LotusClient(connector)
```

## Chain Methods

Access blockchain data including blocks, tipsets, and messages.

```python
# Get the current chain head
chain_head = client.Chain.head()
print(f"Current height: {chain_head.height}")

# Get a specific block by CID
block_cid = "bafy2bzacedkoa5xstphncs3da4d6kpbdvbxlg5zkfgxsxhpbcsfmzfhtm7v3y"
block = client.Chain.get_block(cid=block_cid)

# Get messages in a block
block_messages = client.Chain.get_block_messages(block_cid=block_cid)

# Get a tipset by keys
tipset_key = [{'/': block_cid}]
tipset = client.Chain.get_tip_set(tipset_key=tipset_key)

# Read raw object data
object_data = client.Chain.read_obj(cid=block_cid)
```

## State Methods

Query Filecoin network state including miner information, deals, and verifiers.

```python
# Get miner power and information
miner_address = "f01000"
miner_power = client.State.miner_power(address=miner_address)
miner_info = client.State.miner_info(address=miner_address)

# Get active sectors for a miner
active_sectors = client.State.miner_active_sectors(address=miner_address)

# Wait for message confirmation
message_cid = "bafy2bzacedq..."
message_lookup = client.State.wait_msg_limited(
    cid=message_cid, 
    confidence=3, 
    limit=100
)

# Check verifier status
verifier_address = "f1..."
verifier_status = client.State.verifier_status(address=verifier_address)

# Get network version and genesis info
network_version = client.State.network_version()
genesis = client.Chain.get_genesis()
```

## Network Methods

Monitor and manage network connections, bandwidth, and peer information.

```python
# Get network statistics
stats = client.Net.stat(scope="system")
print(f"Total bandwidth in: {stats['TotalIn']}")

# Get address information
addr_info = client.Net.addrs_listen()
print(f"Listening addresses: {addr_info}")

# Check NAT status
nat_info = client.Net.auto_nat_status()

# Set network limits (requires write permissions)
limits = {
    "Memory": 1024 * 1024 * 1024,  # 1GB
    "Streams": 100
}
success = client.Net.set_limit("libp2p", limits)
```

## Error Handling

Handle API errors using the specific `ApiCallError` exception:

```python
from pylotus_rpc.http_json_rpc_connector import HttpJsonRpcConnector

ApiCallError = HttpJsonRpcConnector.ApiCallError

try:
    block_info = client.Chain.get_block(cid="invalid_cid")
except ApiCallError as e:
    print(f"API call failed: {e.method} - {e.message} (code: {e.code})")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Filecoin Concepts

- **CID**: Content Identifier, a unique hash identifying blocks, messages, and data
- **Tipset**: A set of blocks at the same height in the blockchain
- **Miner**: Storage provider in the Filecoin network
- **Sector**: Unit of storage committed by miners
- **Message**: Transactions and state changes in Filecoin

## License:

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

```
