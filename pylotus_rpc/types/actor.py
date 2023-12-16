# actor.py

from .cid import Cid

class Actor:
    """
    Represents an Actor in the Filecoin network.

    Attributes:
    - code: A Cid representing the code of the Actor.
    - head: A Cid representing the head of the Actor.
    - nonce: An integer representing the nonce of the Actor.
    - balance: An int representing the balance of the Actor.
    """

    def __init__(self, code: Cid, head: Cid, nonce: int, balance: int):
        """
        Initializes a new Actor object.

        :param code: A Cid representing the code of the Actor.
        :param head: A Cid representing the head of the Actor.
        :param nonce: An integer representing the nonce of the Actor.
        :param balance: An int representing the balance of the Actor.
        """
        self.code = code
        self.head = head
        self.nonce = nonce
        self.balance = balance

    def __str__(self) -> str:
        return f"Code: {self.code}, Head: {self.head}, Nonce: {self.nonce}, Balance: {self.balance}"
