from dataclasses import dataclass
from .cid import Cid

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

    @staticmethod
    def from_dict(dct: dict) -> 'DealProposal':
        return DealProposal(
            piece_cid=Cid.from_dict(dct["PieceCID"]),
            piece_size=dct["PieceSize"],
            verified_deal=dct["VerifiedDeal"],
            client_addr=dct["Client"],
            provider_addr=dct["Provider"],
            label=dct["Label"],
            start_epoch=dct["StartEpoch"],
            end_epoch=dct["EndEpoch"],
            storage_price_per_epoch=int(dct["StoragePricePerEpoch"]),
            provider_collateral=int(dct["ProviderCollateral"]),
            client_collateral=int(dct["ClientCollateral"])
        )

