from typing import Optional
from ..HttpJsonRpcConnector import HttpJsonRpcConnector
from ..types.BlockHeader import BlockHeader, dict_to_blockheader
from ..types.Cid import Cid
from ..types.Message import Message
from ..types.TipSet import Tipset
from ..types.Actor import Actor
from ..types.InvocationResult import InvocationResult
import json


def _changed_actors(connector: HttpJsonRpcConnector, cid1 : str, cid2 : str):
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateChangedActors",
        "params": Cid.dct_cids([cid1, cid2])
    }
    
    # TODO - this is a work in progress
    result = connector.execute(connector, payload, debug=True)
    


def _state_call(connector: HttpJsonRpcConnector, 
                message: Message, 
                tipset: Optional[Tipset] = None) -> InvocationResult:
    
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateCall",
        "params": [
            message.to_json(),
            tipset.dct_cids() if tipset else None,
        ]
    }
    
    dct_result = connector.execute(payload)
    invocation_result = InvocationResult.from_json(dct_result)
    return invocation_result
     
def _account_key(connector, address, tipset=None):
    # JSON-RPC payload for requesting the account key
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateAccountKey",
        "params": [
            address,
            tipset.dct_cids() if tipset else None,
        ]
    }

    result = connector.execute(payload)
    # Parse the account key
    address = Cid(result["result"])
    return address
    

def _get_actor(connector, actor_id, tipset=None):

    cids = None
    if tipset:
        cids = tipset.dct_cids()

    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateGetActor",
        "params": [
            actor_id,
            cids,
        ],
    }

    dct_result = connector.execute(payload)
    actor_data = dct_result['result']

    # Create Actor object using parsed data
    actor = Actor(
        Code=Cid(actor_data['Code']['/']),
        Head=Cid(actor_data['Head']['/']),
        Nonce=actor_data['Nonce'],
        Balance=actor_data['Balance'])

    return actor


# WARNING: This method takes an exceptionally long time to complete.
def _list_state_actors(connector, tipset):
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.StateListActors",
        "params": [
            tipset.dct_cids(),
        ]
    }

    # TODO - unfinished
    dct_result = connector.execute(payload)


def _get_chain_head(connector):
    # JSON-RPC payload for requesting the chain head
    payload = {
        "jsonrpc": "2.0",
        "method": "Filecoin.ChainHead",
    }

    dct_result = connector.execute(payload)

    # Parse the CIDs
    lst_cids = [Cid(cid["/"]) for cid in dct_result["result"]["Cids"]]

    # Parse block headers into BlockHeader objects
    lst_block_headers = [dict_to_blockheader(dct) for dct in dct_result["result"]["Blocks"]]
    height = dct_result["result"]["Height"]

    # construct and return a Tipset        
    return Tipset(height, lst_cids, lst_block_headers)

