from dataclasses import dataclass, field
from typing import Dict
from .cid import Cid

@dataclass
class ActorState:
    balance: int
    code: Cid
    dct_state: Dict

    @staticmethod
    def from_dict(dct):
        return ActorState(
            balance=dct.get('Balance', None),
            code=Cid.from_dict(dct.get('Code', None)),
            dct_state=dct.get('State', None))