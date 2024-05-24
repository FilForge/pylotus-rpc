from dataclasses import dataclass
from typing import List, Dict, Any

from .message import Message
from .signed_message import SignedMessage
from .cid import Cid

@dataclass
class BlockMessages:
    """
    A representation of Block messages in the Filecoin blockchain.

    Attributes:
    - bls_messages: A list of BLS (Boneh-Lynn-Shacham) signature messages.
    - secpk_messages: A list of Secp256k1 signature messages.
    - cids: A list of content identifiers (CIDs) associated with the block messages.
    """
    bls_messages: List[Message]
    secpk_messages: List[SignedMessage]
    cids: List[Cid]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BlockMessages':
        """
        Deserialize a dictionary (from parsed JSON) into a BlockMessages object.

        Args:
        - data (dict): A dictionary representation of the BlockMessages object.

        Returns:
        - BlockMessages: An instance of the BlockMessages class.        
        """
        return BlockMessages(
            bls_messages=[Message.from_dict(msg) for msg in data['BlsMessages']],
            secpk_messages=[SignedMessage.from_dict(msg) for msg in data['SecpkMessages']],
            cids=[Cid(cid) for cid in data['Cids']]
        )
