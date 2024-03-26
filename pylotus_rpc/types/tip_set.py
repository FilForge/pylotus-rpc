from dataclasses import dataclass, field
from typing import List
from .cid import Cid
from .block_header import BlockHeader

@dataclass
class Tipset:
    """
    Represents a Tipset in the Filecoin blockchain.

    A Tipset is a set of blocks with the same height, parents, and total weight.

    Attributes:
    - height: An integer representing the height of the Tipset in the blockchain.
    - cids: A list of Cid objects, representing the Content Identifiers of the blocks in the Tipset.
    - blocks: A list of BlockHeader objects, representing the blocks in the Tipset.
    """
    height: int
    cids: List[Cid] = field(default_factory=list)
    blocks: List[BlockHeader] = field(default_factory=list)

    def get_tip_set_key(self) -> List[dict]:
        """
        Returns a dictionary representation of the Tipset's CIDs for JSON serialization.
        """
        return [{"/": cid.id} for cid in self.cids]
