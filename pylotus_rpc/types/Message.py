from decimal import Decimal
from dataclasses import dataclass, field
from typing import Union

@dataclass
class Message:
    """A representation of a Filecoin message for transaction purposes.
    
    Attributes:
    - Version: Protocol version, defaults to 0.
    - To: Destination address of the message.
    - From: Source address of the message.
    - Nonce: A counter value for each message sent (generally used to order messages and prevent double spending).
    - Value: Amount of Filecoin being transferred in the message, represented as a Decimal for precision.
    - GasLimit: Maximum amount of gas this message is allowed to use, defaults to 1000.
    - GasFeeCap: Maximum price per gas unit this message is willing to pay.
    - GasPremium: A fee related to message inclusion into a block.
    - Method: The method being invoked on the target actor.
    - Params: Any parameters being passed with the method.
    """

    Version: int = field(default=0)
    To: str
    From: str
    Nonce: int = field(default=0)
    Value: Decimal
    GasLimit: int = field(default=1000)
    GasFeeCap: Decimal
    GasPremium: Decimal
    Method: int = field(default=0)
    Params: str = field(default="")

    @classmethod
    def from_floats(cls, to_address: str, from_address: str, value: float, gas_fee_cap: float, gas_premium: float) -> "Message":
        """Alternate constructor to create a Message instance using float values.
        
        Args:
        - to_address: The destination address of the message.
        - from_address: The source address of the message.
        - value: Amount of Filecoin being transferred.
        - gas_fee_cap: Maximum price per gas unit.
        - gas_premium: Fee related to message inclusion into a block.
        
        Returns:
        A Message instance with appropriate fields set.
        """
        return cls(
            To=to_address,
            From=from_address,
            Value=Decimal(value),
            GasFeeCap=Decimal(gas_fee_cap),
            GasPremium=Decimal(gas_premium)
        )
    