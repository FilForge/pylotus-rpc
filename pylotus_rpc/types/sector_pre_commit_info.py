from dataclasses import dataclass, asdict
from typing import List
from .cid import Cid
import json

@dataclass
class SectorPreCommitInfo:
    """
    A dataclass representing a sector's pre-commit information in Filecoin.

    Attributes:
        seal_proof (int): The proof type of the sector.
        sector_number (int): The number of the sector.
        sealed_cid (Cid): The CID of the sealed sector.
        seal_rand_epoch (int): The chain epoch at which the randomness for the seal proof was drawn.
        deal_ids (List[int]): A list of deal IDs included in the sector.
        expiration (int): The epoch at which the sector expires.
        replace_capacity (bool): A flag indicating if the sector is a replacement for capacity commitment.
        replace_sector_deadline (int): The deadline within which the replaced sector should be proven.
        replace_sector_partition (int): The partition of the replaced sector.
        replace_sector_number (int): The number of the replaced sector.

    Methods:
        from_json(str_json: str): Static method to create an instance from a JSON string.
        from_dict(dct): Static method to create an instance from a dictionary.
        to_dict(): Method to convert the instance to a dictionary.
    """

    seal_proof: int
    sector_number: int
    sealed_cid: Cid
    seal_rand_epoch: int
    deal_ids: List[int]
    expiration: int
    replace_capacity: bool
    replace_sector_deadline: int
    replace_sector_partition: int
    replace_sector_number: int

    @staticmethod
    def from_json(str_json: str):
        """Creates an instance of SectorPreCommitInfo from a JSON string."""
        return SectorPreCommitInfo.from_dict(json.loads(str_json))

    @staticmethod
    def from_dict(dct):
        """Creates an instance of SectorPreCommitInfo from a dictionary."""
        return SectorPreCommitInfo(
            seal_proof=dct.get("SealProof"),
            sector_number=dct.get("SectorNumber"),
            sealed_cid=Cid.from_dict(dct.get("SealedCID")),
            seal_rand_epoch=dct.get("SealRandEpoch"),
            deal_ids=dct.get("DealIDs"),
            expiration=dct.get("Expiration"),
            replace_capacity=dct.get("ReplaceCapacity"),
            replace_sector_deadline=dct.get("ReplaceSectorDeadline"),
            replace_sector_partition=dct.get("ReplaceSectorPartition"),
            replace_sector_number=dct.get("ReplaceSectorNumber")
        )

    def to_dict(self):
        """Converts the instance to a dictionary."""
        data_dict = asdict(self)
        data_dict['sealed_cid'] = self.sealed_cid.to_dict()
        return data_dict
