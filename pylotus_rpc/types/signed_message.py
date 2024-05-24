from dataclasses import dataclass, field
from typing import Dict, Any
from .message import Message
from .signature import Signature

@dataclass
class SignedMessage(Message):
    """
    A representation of a signed Filecoin message for transaction purposes.

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
    - signature: The cryptographic signature for the message, ensuring authenticity and integrity.
    """
    signature: Signature = field(default_factory=lambda: Signature(signer="", signature_value=""))

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'SignedMessage':
        """
        Deserialize a dictionary (from parsed JSON) into a SignedMessage object.

        This method first verifies the presence of required keys in the dictionary,
        then constructs an instance of SignedMessage and populates its fields.

        Args:
        - data (dict): A dictionary representation of the SignedMessage object.

        Returns:
        - SignedMessage: An instance of the SignedMessage class.

        Raises:
        - ValueError: If the 'Signature' key is not present in the data dictionary.

        Example:
            signed_msg_dict = {
                'Message': {...},
                'Signature': {...}
            }
            signed_message = SignedMessage.from_dict(signed_msg_dict)
        """
        # Verify the 'Signature' key is present in the data dictionary
        if 'Signature' not in data:
            raise ValueError("Missing 'Signature' key in data dictionary.")

        # Deserialize Message and Signature from the provided data
        message = Message.from_dict(data['Message'])
        signature = Signature.from_dict(data['Signature'])

        return SignedMessage(
            to_addr=message.to_addr,
            from_addr=message.from_addr,
            value=message.value,
            gas_fee_cap=message.gas_fee_cap,
            gas_premium=message.gas_premium,
            version=message.version,
            nonce=message.nonce,
            gas_limit=message.gas_limit,
            method=message.method,
            params=message.params,
            signature=signature
        )
