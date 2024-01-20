from dataclasses import dataclass
from typing import List

@dataclass
class MinerPartition:
    """
    Represents a miner partition in the Filecoin network.

    Attributes:
        all_sectors (List[int]): A list of integers representing all sectors in the partition.
        faulty_sectors (List[int]): A list of integers representing sectors that are currently faulty.
        recovering_sectors (List[int]): A list of integers representing sectors that are in the process of recovery.
        live_sectors (List[int]): A list of integers representing sectors that are neither faulty nor terminated.
        active_sectors (List[int]): A list of integers representing sectors that are actively contributing to the miner's power.
    """
    all_sectors: List[int]
    faulty_sectors: List[int]
    recovering_sectors: List[int]
    live_sectors: List[int]
    active_sectors: List[int]

    @staticmethod
    def from_dict(dct):
        """
        Creates a MinerPartition instance from a dictionary.

        Args:
            dct (dict): A dictionary containing data of a miner partition.

        Returns:
            MinerPartition: An instance of MinerPartition.
        """
        return MinerPartition(
            all_sectors=dct.get("AllSectors", []),
            faulty_sectors=dct.get("FaultySectors", []),
            recovering_sectors=dct.get("RecoveringSectors", []),
            live_sectors=dct.get("LiveSectors", []),
            active_sectors=dct.get("ActiveSectors", [])
        )
