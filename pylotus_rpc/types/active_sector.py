from dataclasses import dataclass
from typing import List, Optional
from .cid import Cid

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ActiveSector:
    sector_number: int
    seal_proof: int
    sealed_cid: Cid
    deal_ids: Optional[List[int]]
    activation: int
    expiration: int
    deal_weight: int
    verified_deal_weight: int
    initial_pledge: int
    expected_day_reward: int
    expected_storage_pledge: int
    replaced_sector_age: int
    replaced_day_reward: int
    sector_key_cid: Optional[Cid]
    simple_qa_power: bool

    @staticmethod
    def from_dict(data: dict) -> 'ActiveSector':
        # Convert types as necessary
        return ActiveSector(
            sector_number=data.get('SectorNumber'),
            seal_proof=data.get('SealProof'),
            sealed_cid=Cid.from_dict(data['SealedCID']),
            deal_ids=data.get('DealIDs') if data.get('DealIDs') is not None else None,
            activation=data.get('Activation'),
            expiration=data.get('Expiration'),
            deal_weight=int(data.get('DealWeight', 0)),
            verified_deal_weight=int(data.get('VerifiedDealWeight', 0)),
            initial_pledge=int(data.get('InitialPledge', 0)),
            expected_day_reward=int(data.get('ExpectedDayReward', 0)),
            expected_storage_pledge=int(data.get('ExpectedStoragePledge', 0)),
            replaced_sector_age=data.get('ReplacedSectorAge', 0),
            replaced_day_reward=int(data.get('ReplacedDayReward', 0)),
            sector_key_cid=Cid.from_dict(data['SectorKeyCID']) if data.get('SectorKeyCID') is not None else None,
            simple_qa_power=data.get('SimpleQAPower', False)
        )

