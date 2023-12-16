from dataclasses import dataclass, field
from typing import Union, Dict

@dataclass
class Message:
    """
    A representation of a Filecoin message for transaction purposes.

    Attributes:
    - to_addr: Destination address of the message.
    - from_addr: Source address of the message.
    - value: Amount of Filecoin being transferred in the message, represented as an int.
    - gas_fee_cap: Maximum price per gas unit this message is willing to pay.
    - gas_premium: A fee related to message inclusion into a block.
    - version: Protocol version, defaults to 0.
    - nonce: A counter value for each message sent (generally used to order messages and prevent double spending).
    - gas_limit: Maximum amount of gas this message is allowed to use, defaults to 1000.
    - method: The method being invoked on the target actor. Defaults to 0, which means it's just a value transfer.
    - params: Any parameters being passed with the method. Default is an empty string.
    """

    to_addr: str
    from_addr: str
    value: int
    gas_fee_cap: int
    gas_premium: int
    version: int = field(default=0)
    nonce: int = field(default=0)
    gas_limit: int = field(default=1000)
    method: int = field(default=0)
    params: str = field(default="")

    def to_json(self) -> dict:
        """
        Serialize the Message object into a JSON-friendly dictionary for the Filecoin API.

        Returns:
        A dictionary representation of the Message object.
        """
        return {
            "Version": self.version,
            "To": self.to_addr,
            "From": self.from_addr,
            "Nonce": self.nonce,
            "Value": str(self.value),  # Filecoin APIs typically expect stringified numbers for high precision
            "GasLimit": self.gas_limit,
            "GasFeeCap": str(self.gas_fee_cap),  # Convert to string
            "GasPremium": str(self.gas_premium),  # Convert to string
            "Method": self.method,
            "Params": self.params
        }


    @staticmethod
    def from_json(data: Dict[str, Union[str, int]]) -> 'Message':
        """
        Deserialize a dictionary (from parsed JSON) into a Message object.

        Args:
        - data: A dictionary representation of the Message object.

        Returns:
        An instance of the Message class.
        """
        return Message(
            to_addr=data["To"],
            from_addr=data["From"],
            value=int(data["Value"]),
            gas_fee_cap=int(data.get("GasFeeCap", 0)),  # Treat GasFeeCap as optional with a default value of 0            GasPremium=int(data["GasPremium"]),
            gas_premium=int(data.get("GasPremium",0)),  # Added GasPremium as optional with a default value of 0
            version=data.get("Version", 0),  # Using .get() to provide default values
            nonce=data.get("Nonce", 0),
            gas_limit=data.get("GasLimit", 1000),
            method=data.get("Method", 0),
            params=data.get("Params", "")
        )

