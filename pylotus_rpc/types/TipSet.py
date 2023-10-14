from typing import List
from .Cid import Cid
from .BlockHeader import BlockHeader

class Tipset:
    def __init__(self, height: int, cids: List[Cid], blocks: List[BlockHeader]):
        self.height = height
        self.cids = cids
        self.blocks = blocks
