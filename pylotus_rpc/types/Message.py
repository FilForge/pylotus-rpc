from dataclasses import dataclass, field
from typing import Union

@dataclass
class Message:
    """
    A representation of a Filecoin message for transaction purposes.

    Attributes:
    - To: Destination address of the message.
    - From: Source address of the message.
    - Value: Amount of Filecoin being transferred in the message, represented as an int.
    - GasFeeCap: Maximum price per gas unit this message is willing to pay.
    - GasPremium: A fee related to message inclusion into a block.
    - Version: Protocol version, defaults to 0.
    - Nonce: A counter value for each message sent (generally used to order messages and prevent double spending).
    - GasLimit: Maximum amount of gas this message is allowed to use, defaults to 1000.
    - Method: The method being invoked on the target actor. Defaults to 0, which means it's just a value transfer.
    - Params: Any parameters being passed with the method. Default is an empty string.
    """

    To: str
    From: str
    Value: int
    GasFeeCap: int
    GasPremium: int
    Version: int = field(default=0)
    Nonce: int = field(default=0)
    GasLimit: int = field(default=1000)
    Method: int = field(default=0)
    Params: str = field(default="")

    def to_json(self) -> dict:
        """
        Serialize the Message object into a JSON-friendly dictionary for the Filecoin API.

        Returns:
        A dictionary representation of the Message object.
        """
        return {
            "Version": self.Version,
            "To": self.To,
            "From": self.From,
            "Nonce": self.Nonce,
            "Value": str(self.Value),  # Filecoin APIs typically expect stringified numbers for high precision
            "GasLimit": self.GasLimit,
            "GasFeeCap": str(self.GasFeeCap),  # Convert to string
            "GasPremium": str(self.GasPremium),  # Convert to string
            "Method": self.Method,
            "Params": self.Params
        }

