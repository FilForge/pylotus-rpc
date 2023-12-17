# actor.py
from dataclasses import dataclass
from .cid import Cid

@dataclass
class Actor:
    """
    Represents an Actor in the Filecoin network.

    Attributes:
    - code: A Cid representing the code of the Actor.
    - head: A Cid representing the head of the Actor.
    - nonce: An integer representing the nonce of the Actor.
    - balance: An int representing the balance of the Actor.
    """
    code: Cid
    head: Cid
    nonce: int
    balance: int

    def __str__(self) -> str:
        return f"Code: {self.code}, Head: {self.head}, Nonce: {self.nonce}, Balance: {self.balance}"
