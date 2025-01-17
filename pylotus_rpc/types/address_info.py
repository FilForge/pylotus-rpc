from dataclasses import dataclass
from typing import List

@dataclass
class AddressInfo:
    peer_id: str
    addrs: List[str]

    @staticmethod
    def from_dict(dct):
        return AddressInfo(
            peer_id=dct.get('ID', None),
            addrs=dct.get('Addrs', None))