from dataclasses import dataclass
from .message import Message  
from .cid import Cid

@dataclass
class WrappedMessage:
    """
    A Filecoin message wrapped with its CID.

    Attributes:
        message (Message): The Filecoin message.
        cid (Cid): The Content Identifier (CID) for the message.
    """
    message: Message
    cid: Cid
