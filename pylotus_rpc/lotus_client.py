from pylotus_rpc.methods import state
from pylotus_rpc.methods import chain
from pylotus_rpc.methods import net
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
from .types.block_messages import BlockMessages
from .types.wrapped_message import WrappedMessage
from .types.message_receipt import MessageReceipt
from .types.head_change import HeadChange
from .types.address_info import AddressInfo
from .types.nat_info import NatInfo

class LotusClient:

    def __init__(self, connector: HttpJsonRpcConnector):
        self.connector = connector
        self.State = self.State(connector)
        self.Chain = self.Chain(connector)
        self.Net = self.Net(connector)

    class Net:

        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def find_peer(self, peer_id: str) -> Dict:
            return net._find_peer(self.connector, peer_id)

        def connect(self, peer_id: str, addrs: List[str]) -> bool:
            return net._connect(self.connector, peer_id, addrs)

        def connectedness(self, peer_id: str) -> Dict:
            return net._connectedness(self.connector, peer_id)

        def disconnect(self, peer_id: str) -> bool:
            return net._disconnect(self.connector, peer_id)

        def block_remove(self, peers: List[str] = None, ip_addrs: List[str] = None, ip_subnets: List[str] = None) -> bool:
            return net._block_remove(self.connector, peers, ip_addrs, ip_subnets)

        def block_list(self) -> Dict:
            return net._block_list(self.connector)

        def block_add(self, peers: List[str] = None, ip_addrs: List[str] = None, ip_subnets: List[str] = None) -> bool:
            return net._block_add(self.connector, peers, ip_addrs, ip_subnets)

        def addrs_listen(self) -> AddressInfo:
            return net._addrs_listen(self.connector)

        def agent_version(self, peer_id: str) -> str:
            return net._agent_version(self.connector, peer_id)

        def peers(self) -> List[AddressInfo]:
            return net._peers(self.connector)

        def bandwidth_stats(self) -> Dict:
            return net._bandwidth_stats(self.connector)

        def auto_nat_status(self) -> NatInfo:
            return net._auto_nat_status(self.connector)

        def bandwidth_stats_by_peer(self) -> Dict:
            return net._bandwidth_stats_by_peer(self.connector)

        def bandwidth_stats_by_protocol(self) -> Dict:
            return net._bandwidth_stats_by_protocol(self.connector)

    class Chain:
        
        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def tip_set_weight(self, tipset_key: List[dict]) -> int:
            return chain._tip_set_weight(self.connector, tipset_key)

        def stat_obj(self, obj: Cid, base: Cid = None) -> Dict:
            return chain._stat_obj(self.connector, obj, base)

        def set_head(self, head: Tipset) -> None:
            return chain._set_head(self.connector, head)

        def notify(self) -> Dict:
            return chain._chain_notify(self.connector)

        def has_obj(self, cid: str) -> bool:
            return chain._has_obj(self.connector, cid)

        def get_randomness_from_tickets(self, domain_tag: int, epoch: int, random_bytes: str, tipset: Tipset) -> str:
            return chain._get_randomness_from_tickets(self.connector, domain_tag, epoch, random_bytes, tipset)

        def get_randomness_from_beacon(self, domain_tag: int, epoch: int, random_bytes: str, tipset: Optional[Tipset] = None) -> str:
            return chain._get_randomness_from_beacon(self.connector, domain_tag, epoch, random_bytes, tipset)

        def get_tipset_by_height(self, height: int, tipset_key: List[dict] = None) -> Tipset:
            return chain._get_tipset_by_height(self.connector, height, tipset_key)

        def get_path(self, start_tipset_key: List[dict], end_tipset_key: List[dict]) -> List[HeadChange]:
            return chain._get_path(self.connector, start_tipset_key, end_tipset_key)

        def get_parent_receipts(self, block_cid: str) -> List[MessageReceipt]:
            return chain._get_parent_receipts(self.connector, block_cid)

        def get_parent_messages(self, block_cid: str) -> List[WrappedMessage]:
            return chain._get_parent_messages(self.connector, block_cid)

        def get_node(self, node_path_selector: str) -> dict:
            return chain._get_node(self.connector, node_path_selector)

        def get_messages_in_tipset(self, tipset_key: List[dict]) -> List[Message]:
            return chain._get_messages_in_tipset(self.connector, tipset_key=tipset_key)

        def get_message(self, cid: str) -> Message:
            return chain._get_message(self.connector, cid)

        def get_genesis(self) -> Tipset:
            return chain._get_genesis(self.connector)

        def delete_obj(self, cid: str) -> bool:
            return chain._delete_obj(self.connector, cid)

        def export(self, chain_epoch: int, old_msg_skip: bool, tipset_key: str):
            return chain._export(self.connector, chain_epoch, old_msg_skip, tipset_key)

        def get_block_messages(self, block_cid: str) -> BlockMessages:
            return chain._get_block_messages(self.connector, block_cid)

        def get_tip_set(self, tipset_key: List[dict]) -> Tipset:
            return chain._get_tip_set(self.connector, tipset_key)

        def head(self) -> Tipset:
            return chain._head(self.connector)

        def get_block(self, cid: str) -> BlockHeader:
            return chain._get_block(self.connector, cid)
        
        def read_obj(self, cid: str) -> str:
            return chain._read_obj(self.connector, cid)
                                   

    class State:

        def __init__(self, connector: HttpJsonRpcConnector):
            self.connector = connector

        def wait_msg_limited(self, cid: str, confidence: int, limit: int) -> MessageLookup:
            return state._wait_msg_limited(self.connector, cid, confidence, limit)

        def wait_msg(self, cid: str, confidence: int) -> MessageLookup:
            return state._wait_msg(self.connector, cid, confidence)

        def verifier_status(self, address: str, tipset: Optional[Tipset] = None) -> int:
            return state._verifier_status(self.connector, address, tipset)

        def verified_registry_root_key(self, tipset: Optional[Tipset] = None) -> str:
            return state._verified_registry_root_key(self.connector, tipset)

        def verified_client_status(self, address: str, tipset: Optional[Tipset] = None) -> int:
            return state._verified_client_status(self.connector, address, tipset)

        def vm_circulating_supply_internal(self, tipset: Optional[Tipset] = None) -> Dict[str, int]:
            return state._vm_circulating_supply_internal(self.connector, tipset)

        def sector_pre_commit_info(self, address: str, sector_number: int, tipset: Optional[Tipset] = None) -> SectorPreCommitInfo:
            return state._sector_pre_commit_info(self.connector, address, sector_number, tipset)

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

        def market_storage_deal(self, deal_id: int, tipset: Optional[Tipset] = None) -> dict:
            return state._market_storage_deal(self.connector, deal_id, tipset)

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
        
        def call(self, message: Message, tipset: Optional[Tipset] = None) -> InvocationResult:
            return state._call(self.connector, message, tipset)
        
        def changed_actors(self, cid1: str, cid2 : str) -> List[Actor]:
            return state._changed_actors(self.connector, cid1, cid2)
        
        def circulating_supply(self, tipset: Optional[Tipset] = None) -> int:
            return state._circulating_supply(self.connector, tipset)
        
        def compute(self, epoch: int, messages: List[Message], tipset: Optional[Tipset] = None) -> StateComputeOutput:
            return state._compute(self.connector, epoch, messages, tipset)
        
        def deal_provider_collateral_bounds(
                self, 
                padded_piece_size: int, 
                is_verified: bool, 
                tipset: Optional[Tipset] = None) -> Tuple[Optional[int], Optional[int]]:
            return state._deal_provider_collateral_bounds(self.connector, padded_piece_size, is_verified, tipset)

        def decode_params(self, actor_id: str, method_num: int, params: str, tipset: Optional[Tipset] = None) -> dict:
            return state._decode_params(self.connector, actor_id, method_num, params, tipset)

        def get_randomness_from_tickets(self, domain_tag: int, epoch: int, random_bytes: str, tipset: Optional[Tipset] = None) -> str:
            # default to the chain head if not tipset was given
           if not tipset:
               tipset = chain._head(self.connector)
           return state._get_randomness_from_tickets(self.connector, domain_tag, epoch, random_bytes, tipset)

        def get_randomness_from_beacon(self, domain_tag: int, epoch: int, random_bytes: str, tipset: Optional[Tipset] = None) -> str:
            return state._get_randomness_from_beacon(self.connector, domain_tag, epoch, random_bytes, tipset)

