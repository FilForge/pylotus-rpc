from pylotus_rpc.methods import state
from pylotus_rpc.methods import chain
from typing import Optional, List, Tuple, Dict
from .types.tip_set import Tipset
from .types.message import Message
from .types.cid import Cid
from .types.invocation_result import InvocationResult
from .types.actor import Actor
from .types.state_compute_output import StateComputeOutput
from .types.actor_state import ActorState
from .types.active_sector import ActiveSector
from .types.block_header import BlockHeader
from .http_json_rpc_connector import HttpJsonRpcConnector

class LotusClient:

    def __init__(self, connector: HttpJsonRpcConnector):
        self.connector = connector
        self.State = self.State(connector)
        self.Chain = self.Chain(connector)

    class Chain:
        
        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def get_chain_head(self) -> Tipset:
            return chain._get_chain_head(self.connector)

        def get_block(self, cid: str) -> BlockHeader:
            return chain._get_block(self.connector, cid)
        
        def read_obj(self, cid: str) -> str:
            return chain._read_obj(self.connector, cid)
                                   

    class State:

        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def miner_available_balance(self, address: str, tipset: Optional[Tipset] = None) -> int:
            return state._miner_available_balance(self.connector, address, tipset)

        def miner_active_sectors(self, address: str, tipset: Optional[Tipset] = None) -> List[ActiveSector]:
            return state._miner_active_sectors(self.connector, address, tipset)

        def storage_market_deal(self, deal_id: int, tipset: Optional[Tipset] = None) -> dict:
            return state._storage_market_deal(self.connector, deal_id, tipset)

        def market_participants(self, tipset: Optional[Tipset] = None) -> List[Dict]:
            return state._market_participants(self.connector, tipset)

        def market_deals(self, tipset: Optional[Tipset] = None) -> dict:
            return state._market_deals(self.connector, tipset)

        def market_balance(self, address: str, tipset: Optional[Tipset] = None) -> int:
            return state._market_balance(self.connector, address, tipset)

        def lookup_id(self, address: str, tipset: Optional[Tipset] = None) -> str:
            return state._lookup_id(self.connector, address, tipset)

        def list_miners(self, tipset: Optional[Tipset] = None) -> List[str]:
            return state._list_miners(self.connector, tipset)            

        def list_messages(self, to_addr: str, from_addr: str, epoch: int, tipset: Optional[Tipset] = None) -> List[Cid]:
            return state._list_messages(self.connector, to_addr, from_addr, epoch, tipset)
        
        def read_state(self, actor_id: str, tipset: Optional[Tipset] = None) -> ActorState:
            return state._read_state(self.connector, actor_id, tipset)
        
        def account_key(self, address: str, tipset: Optional[Tipset] = None) -> Cid:
            return state._account_key(self.connector, address, tipset)
                
        def list_actors(self, tipset: Optional[Tipset] = None) -> List[str]:
            return state._list_actors(self.connector, tipset)
        
        def get_actor(self, actor_id: str, tipset: Optional[Tipset] = None) -> Actor:
            return state._get_actor(self.connector, actor_id, tipset)
        
        def state_call(self, message: Message, tipset: Optional[Tipset] = None) -> InvocationResult:
            return state._state_call(self.connector, message, tipset)
        
        def changed_actors(self, cid1: str, cid2 : str) -> List[Actor]:
            return state._changed_actors(self.connector, cid1, cid2)
        
        def circulating_supply(self, tipset: Optional[Tipset] = None) -> int:
            return state._circulating_supply(self.connector, tipset)
        
        def state_compute(self, epoch: int, messages: List[Message], tipset: Optional[Tipset] = None) -> StateComputeOutput:
            return state._state_compute(self.connector, epoch, messages, tipset)
        
        def deal_provider_collateral_bounds(
                self, 
                padded_piece_size: int, 
                is_verified: bool, 
                tipset: Optional[Tipset] = None) -> Tuple[Optional[int], Optional[int]]:
            return state._deal_provider_collateral_bounds(self.connector, padded_piece_size, is_verified, tipset)

        def decode_params(self, actor_id: str, method_num: int, params: str, tipset: Optional[Tipset] = None) -> dict:
            return state._decode_params(self.connector, actor_id, method_num, params, tipset)
                                    
        def get_randomness_from_beacon(self, domain_tag: int, epoch: int, random_bytes: str, tipset: Optional[Tipset] = None) -> str:
            return state._get_randomness_from_beacon(self.connector, domain_tag, epoch, random_bytes, tipset)

