from dataclasses import dataclass

@dataclass
class DealState:
    sector_start_epoch: int
    last_updated_epoch: int
    slash_epoch: int
