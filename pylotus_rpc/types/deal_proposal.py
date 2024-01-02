from dataclasses import dataclass
from types import Cid

@dataclass
class DealProposal:
    piece_cid: Cid
    piece_size: int
    verified_deal: bool
    client_addr: str
    provider_addr: str
    label: str
    start_epoch: int
    end_epoch: int
    storage_price_per_epoch: int
    provider_collateral: int
    client_collateral: int
