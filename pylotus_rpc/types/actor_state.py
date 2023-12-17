from dataclasses import dataclass
from typing import Dict
from .cid import Cid

@dataclass
class ActorState:
    balance: int
    code: Cid
    state: Dict

    @staticmethod
    def from_dict(dct):
        return ActorState(
            balance=int(dct.get('Balance', None)),
            code=Cid.from_dict(dct.get('Code', None)),
            state=dct.get('State', None))