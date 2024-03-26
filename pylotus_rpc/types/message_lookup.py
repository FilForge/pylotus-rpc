from dataclasses import dataclass
from typing import List, Optional, Dict
from .message_receipt import MessageReceipt
from .cid import Cid
from .tip_set import Tipset

@dataclass
class MessageLookup:
    """
    Represents the lookup result of a Filecoin message including its receipt and associated tipset.

    Attributes:
        message_cid (Cid): The CID of the message that was looked up.
        message_receipt (MessageReceipt): The receipt of the message execution on the blockchain.
        return_dec (Optional[str]): The decoded return value of the message execution, if any.
        tip_set (Tipset): The tipset in which the message was included.
        height (int): The blockchain height at which the message was executed.

    Methods:
        from_dict: Creates an instance of MessageLookup from a dictionary representation.
    """

    message_cid: Cid
    message_receipt: MessageReceipt
    return_dec: Optional[str]
    tip_set: Tipset
    height: int

    @staticmethod
    def from_dict(data: Dict) -> 'MessageLookup':
        """
        Constructs an instance of MessageLookup from a dictionary, typically parsed from JSON.

        This static method facilitates the creation of a MessageLookup instance by parsing
        the necessary data from a structured dictionary. This is particularly useful when
        dealing with JSON data returned from an API call.

        Args:
            data (Dict): A dictionary containing the necessary keys and values to populate
                         the attributes of a MessageLookup instance.

        Returns:
            MessageLookup: An initialized MessageLookup instance based on the provided data.

        """
        return MessageLookup(
            message_cid=Cid.from_dict(data['Message']),
            message_receipt=MessageReceipt.from_dict(data['Receipt']),
            return_dec=data.get('ReturnDec'),
            tip_set=Tipset(data['Height'], [Cid(cid["/"]) for cid in data['TipSet']]),
            height=data['Height']
        )
