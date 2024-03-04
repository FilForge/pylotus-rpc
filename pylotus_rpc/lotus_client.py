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
from .types.sector import Sector
from .types.block_header import BlockHeader
from .types.deadline import Deadline
from .types.miner_info import MinerInfo
from .types.sector_pre_commit_info import SectorPreCommitInfo
from .types.miner_partition import MinerPartition
from .http_json_rpc_connector import HttpJsonRpcConnector
from .types.miner_power import MinerPower
from .types.deadline_info import DeadlineInfo
from .types.message_lookup import MessageLookup

class LotusClient:

    def __init__(self, connector: HttpJsonRpcConnector):
        self.connector = connector
        self.State = self.State(connector)
        self.Chain = self.Chain(connector)

    class Chain:
        
        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def get_block_messages(self, block_cid: str) -> List[Cid]:
            return chain._get_block_messages(self.connector, block_cid)

        def get_tip_set(self, tipset_key: List[dict]) -> Tipset:
            return chain._get_tip_set(self.connector, tipset_key)

        def get_chain_head(self) -> Tipset:
            return chain._get_chain_head(self.connector)

        def get_block(self, cid: str) -> BlockHeader:
            return chain._get_block(self.connector, cid)
        
        def read_obj(self, cid: str) -> str:
            return chain._read_obj(self.connector, cid)
                                   

    class State:

        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def sector_partition(self, address: str, sector_number: int, tipset: Optional[Tipset] = None) -> Dict[str, int]:
            return state._sector_partition(self.connector, address, sector_number, tipset)

        def sector_get_info(self, miner_address: str, sector_number: int, tipset: Optional[Tipset] = None) -> Sector:
            return state._sector_get_info(self.connector, miner_address, sector_number, tipset)

        def sector_expiration(self, miner_address: str, sector_number: int, tipset: Optional[Tipset] = None) -> Dict[str, int]:
            return state._sector_expiration(self.connector, miner_address, sector_number, tipset)

        def search_message_limited(self, cid: str, limit: int) -> MessageLookup:
            return state._search_message_limited(self.connector, cid, limit)

        def search_message(self, cid: str) -> MessageLookup:
            return state._search_message(self.connector, cid)

        def replay(self, cid: str, tipset: Optional[Tipset] = None) -> InvocationResult:
            return state._replay(self.connector, cid, tipset)

        def network_version(self, tipset: Optional[Tipset] = None) -> int:
            return state._network_version(self.connector, tipset)

        def network_name(self) -> str:
            return state._network_name(self.connector)

        def miner_sectors(self, address: str, sector_list: List[int] = [], tipset: Optional[Tipset] = None) -> List[Sector]:
            return state._miner_sectors(self.connector, address, sector_list, tipset)

        def miner_sector_count(self, miner_address: str, tipset: Optional[Tipset] = None) -> Dict:
            return state._miner_sector_count(self.connector, miner_address, tipset)

        def miner_sector_allocated(self, miner_address: str, sector_number: int, tipset: Optional[Tipset] = None) -> bool:
            return state._miner_sector_allocated(self.connector, miner_address, sector_number, tipset)

        def miner_recoveries(self, address: str, tipset: Optional[Tipset] = None) -> List[int]:
            return state._miner_recoveries(self.connector, address, tipset)

        def miner_proving_deadline(self, address: str, tipset: Optional[Tipset] = None) -> DeadlineInfo:
            return state._miner_proving_deadline(self.connector, address, tipset)

        def miner_pre_commit_deposit_for_power(self, sector_size: int, duration: int, tipset: Optional[Tipset] = None) -> int:
            return state._miner_pre_commit_deposit_for_power(self.connector, sector_size, duration, tipset)

        def miner_power(self, address: str, tipset: Optional[Tipset] = None) -> MinerPower:
            return state._miner_power(self.connector, address, tipset)

        def miner_partitions(self, miner_address: str, deadline_index: int, tipset: Optional[Tipset] = None) -> List[MinerPartition]:
            return state._miner_partitions(self.connector, miner_address, deadline_index, tipset)
        
        def miner_initial_pledge_collateral(self, miner_address: str, sector_pre_commit_info: SectorPreCommitInfo, tipset: Optional[Tipset] = None) -> int:
            return state._miner_initial_pledge_collateral(self.connector, miner_address, sector_pre_commit_info, tipset)

        def miner_info(self, address: str, tipset: Optional[Tipset] = None) -> MinerInfo:
            return state._miner_info(self.connector, address, tipset)

        def miner_faults(self, address: str, tipset: Optional[Tipset] = None) -> int:
            return state._miner_faults(self.connector, address, tipset)

        def miner_deadlines(self, address: str, tipset: Optional[Tipset] = None) -> List[Deadline]:
            return state._miner_deadlines(self.connector, address, tipset)

        def miner_available_balance(self, address: str, tipset: Optional[Tipset] = None) -> int:
            return state._miner_available_balance(self.connector, address, tipset)

        def miner_active_sectors(self, address: str, tipset: Optional[Tipset] = None) -> List[Sector]:
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

