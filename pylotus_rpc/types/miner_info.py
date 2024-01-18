from dataclasses import dataclass, asdict
from typing import List, Optional
import json

@dataclass
class BeneficiaryTerm:
    quota: str
    used_quota: str
    expiration: int

    @staticmethod
    def from_dict(data: dict):
        return BeneficiaryTerm(
            quota=data.get("Quota", ""),
            used_quota=data.get("UsedQuota", ""),
            expiration=data.get("Expiration", 0)
        )

@dataclass
class MinerInfo:
    owner: str
    worker: str
    new_worker: Optional[str]
    control_addresses: List[str]
    worker_change_epoch: int
    peer_id: str
    multiaddrs: List[str]
    window_post_proof_type: int
    sector_size: int
    window_post_partition_sectors: int
    consensus_fault_elapsed: int
    pending_owner_address: Optional[str]
    beneficiary: str
    beneficiary_term: Optional[BeneficiaryTerm]
    pending_beneficiary_term: Optional[str]

    def __str__(self) -> str:
        # Convert the dataclass instance to a dictionary and then to a JSON string
        return json.dumps(asdict(self), indent=4, sort_keys=True)

    @staticmethod
    def from_dict(data: dict):
        return MinerInfo(
            owner=data.get("Owner", ""),
            worker=data.get("Worker", ""),
            new_worker=data.get("NewWorker"),
            control_addresses=data.get("ControlAddresses", []),
            worker_change_epoch=data.get("WorkerChangeEpoch", -1),
            peer_id=data.get("PeerId", ""),
            multiaddrs=data.get("Multiaddrs", []),
            window_post_proof_type=data.get("WindowPoStProofType", 0),
            sector_size=data.get("SectorSize", 0),
            window_post_partition_sectors=data.get("WindowPoStPartitionSectors", 0),
            consensus_fault_elapsed=data.get("ConsensusFaultElapsed", -1),
            pending_owner_address=data.get("PendingOwnerAddress"),
            beneficiary=data.get("Beneficiary", ""),
            beneficiary_term=BeneficiaryTerm.from_dict(data["BeneficiaryTerm"]) if data.get("BeneficiaryTerm") else None,
            pending_beneficiary_term=data.get("PendingBeneficiaryTerm")
        )

