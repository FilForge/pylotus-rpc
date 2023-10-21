# Actor.py

from decimal import Decimal
from .Cid import Cid

class Actor:
    """
    Represents an Actor in the Filecoin network.

    Attributes:
    - Code: A Cid representing the code of the Actor.
    - Head: A Cid representing the head of the Actor.
    - Nonce: An integer representing the nonce of the Actor.
    - Balance: A Decimal representing the balance of the Actor.
    """

    def __init__(self, Code: Cid, Head: Cid, Nonce: int, Balance: str):
        """
        Initializes a new Actor object.

        :param Code: A Cid representing the code of the Actor.
        :param Head: A Cid representing the head of the Actor.
        :param Nonce: An integer representing the nonce of the Actor.
        :param Balance: A string (to be converted to Decimal) representing the balance of the Actor.
        """
        self.Code = Code
        self.Head = Head
        self.Nonce = Nonce
        self.Balance = Decimal(Balance)

    def __str__(self) -> str:
        return f"Code: {self.Code}, Head: {self.Head}, Nonce: {self.Nonce}, Balance: {self.Balance}"
