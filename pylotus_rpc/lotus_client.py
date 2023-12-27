from pylotus_rpc.methods import state
from pylotus_rpc.methods import chain
from typing import Optional, List
from .types.tip_set import Tipset
from .types.message import Message
from .types.cid import Cid
from .http_json_rpc_connector import HttpJsonRpcConnector

class LotusClient:

    def __init__(self, connector: HttpJsonRpcConnector):
        self.connector = connector
        self.State = self.State(connector)
        self.Chain = self.Chain(connector)

    class Chain:
        
        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def get_chain_head(self):
            return chain._get_chain_head(self.connector)

        def get_block(self, cid: str):
            return chain._get_block(self.connector, cid)
        
        def read_obj(self, cid: str):
            return chain._read_obj(self.connector, cid)
                                   

    class State:

        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def list_messages(self, to_addr: str, from_addr: str, epoch: int, tipset: Optional[Tipset] = None) -> List[Cid]:
            return state._list_messages(self.connector, to_addr, from_addr, epoch, tipset)
        
        def read_state(self, actor_id: str, tipset: Optional[Tipset] = None):
            return state._read_state(self.connector, actor_id, tipset)
        
        def account_key(self, address: str, tipset: Optional[Tipset] = None):
            return state._account_key(self.connector, address, tipset)
                
        def list_actors(self, tipset: Optional[Tipset] = None):
            return state._list_actors(self.connector, tipset)
        
        def get_actor(self, actor_id: str, tipset: Optional[Tipset] = None):
            return state._get_actor(self.connector, actor_id, tipset)
        
        def state_call(self, message: Message, tipset: Optional[Tipset] = None):
            return state._state_call(self.connector, message, tipset)
        
        def changed_actors(self, cid1: str, cid2 : str):
            return state._changed_actors(self.connector, cid1, cid2)
        
        def circulating_supply(self, tipset: Optional[Tipset] = None):
            return state._circulating_supply(self.connector, tipset)
        
        def state_compute(self, epoch: int, messages: List[Message], tipset: Optional[Tipset] = None):
            return state._state_compute(self.connector, epoch, messages, tipset)
        
        def deal_provider_collateral_bounds(self, padded_piece_size: int, is_verified: bool, tipset: Optional[Tipset] = None):
            return state._deal_provider_collateral_bounds(self.connector, padded_piece_size, is_verified, tipset)

        def decode_params(self, actor_id: str, method_num: int, params: str, tipset: Optional[Tipset] = None):
            return state._decode_params(self.connector, actor_id, method_num, params, tipset)
                                    
        def get_randomness_from_beacon(self, domain_tag: int, epoch: int, random_bytes: str, tipset: Optional[Tipset] = None):
            return state._get_randomness_from_beacon(self.connector, domain_tag, epoch, random_bytes, tipset)
