# PyLotus-RPC

PyLotus-RPC is a Python client library for interacting with the Lotus JSON-RPC API. It provides a convenient way to communicate with a Lotus node from your Python applications.

This codebase is still a WIP, all of the Filecoin.StateXXXX calls have been implemented, but others are being added slowly over time.


## Installation

Installation from PyPi

```shell
pip install pylotus-rpc
```

Here are the usage instructions for the `LotusClient` class and its methods in your Python code, which interacts with an API for blockchain data management:

# LotusClient Usage Instructions

The `LotusClient` class in Python allows interaction with a blockchain API to manage data related to blocks, transactions, and various state-related information.

## Initialization

First, create an instance of `HttpJsonRpcConnector` with the API endpoint URL and then initialize the `LotusClient` with this connector.

```python
from pylotus_rpc import LotusClient, HttpJsonRpcConnector

connector = HttpJsonRpcConnector(api_url='https://api.example.com')
client = LotusClient(connector)
```

## Using Chain Methods

You can fetch block messages, tipsets, and other block-related data using the `Chain` class.

```python
# Fetch block messages by CID
block_messages = client.Chain.get_block_messages(block_cid='your_block_cid_here')

# Get specific tipset
tipset = client.Chain.get_tip_set(tipset_key=[{'/': 'your_tipset_key_here'}])

# Fetch the chain head
chain_head = client.Chain.get_chain_head()

# Get specific block information
block_info = client.Chain.get_block(cid='your_block_cid_here')

# Read object data by CID
object_data = client.Chain.read_obj(cid='your_block_cid_here')
```

## Using State Methods

The `State` class provides methods to access detailed node, sector, and state information.

```python
# Wait for a message with specified CID, confidence, and limit
message_lookup = client.State.wait_msg_limited(cid='your_cid_here', confidence=3, limit=100)

# Fetch the status of a verifier in the blockchain
verifier_status = client.State.verifier_status(address='your_verifier_address_here')

# Get miner power details
miner_power = client.State.miner_power(address='your_miner_address_here')

# List all active sectors for a miner
active_sectors = client.State.miner_active_sectors(address='your_miner_address_here')
```

Each of these methods interacts with the blockchain to retrieve or manage data based on your specific needs.

## Error Handling

Always handle potential exceptions from network issues or data errors:

```python
try:
    block_info = client.Chain.get_block(cid='your_block_cid_here')
except Exception as e:
    print(f"An error occurred: {e}")
```


```


