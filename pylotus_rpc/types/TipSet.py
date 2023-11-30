from typing import List
from .Cid import Cid
from .block_header import BlockHeader

class Tipset:
    """
    Represents a Tipset in the Filecoin blockchain.

    A Tipset is a set of blocks with the same height, parents, and total weight.

    Attributes:
    - height: An integer representing the height of the Tipset in the blockchain.
    - cids: A list of Cid objects, representing the Content Identifiers of the blocks in the Tipset.
    - blocks: A list of BlockHeader objects, representing the blocks in the Tipset.
    """

    def __init__(self, height: int, cids: List[Cid], blocks: List[BlockHeader]):
        """
        Initializes a new Tipset object.

        :param height: The height of the Tipset in the blockchain.
        :param cids: A list of Cid objects representing the Content Identifiers of the blocks in the Tipset.
        :param blocks: A list of BlockHeader objects representing the blocks in the Tipset.
        """
        self.height = height
        self.cids = cids
        self.blocks = blocks


    def dct_cids(self):
        """
        Returns a dictionary representation of the Tipset's CIDs for JSON serialization.
        """
        return [{"/": cid.id} for cid in self.cids]
