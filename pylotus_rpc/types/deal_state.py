from dataclasses import dataclass

@dataclass
class DealState:
    sector_start_epoch: int
    last_updated_epoch: int
    slash_epoch: int
    verified_claim: int

    @staticmethod
    def from_dict(dct: dict) -> 'DealState':
        return DealState(
            sector_start_epoch=dct.get("SectorStartEpoch", -1),
            last_updated_epoch=dct.get("LastUpdatedEpoch", -1),
            slash_epoch=dct.get("SlashEpoch", -1),
            verified_claim=dct.get("VerifiedClaim", 0)
        )
