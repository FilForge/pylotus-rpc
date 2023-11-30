from typing import List, Dict, Union
from .cid import Cid
from .Signature import Signature

class BlockHeader:
    """
    Represents the block header in the blockchain.
    
    Attributes:
    - miner: The address of the block miner.
    - ticket: Lottery ticket for leader election.
    - election_proof: Proof of leader election.
    - beacon_entries: Randomness beacon for the block.
    - win_post_proof: Winning post proof.
    - parents: CIDs of the block's parent blocks.
    - parent_weight: Parent weight of the block.
    - height: Height of the block in the blockchain.
    - parent_state_root: CID for the state tree of this block's parent.
    - parent_message_receipts: CID of the receipt tree for the parent.
    - messages: CID of the message list for this block.
    - bls_aggregate: Aggregated BLS signature.
    - timestamp: Block creation time.
    - block_sig: Block signature.
    - fork_signaling: Fork signaling number.
    - parent_base_fee: Parent base fee.
    """

    def __init__(self, 
                 miner: str,
                 ticket: Dict[str, str],
                 election_proof: Dict[str, Union[int, str]],
                 beacon_entries: List[Dict[str, Union[int, str]]],
                 win_post_proof: List[Dict[str, Union[int, str]]],
                 parents: List[Cid],
                 parent_weight: str,
                 height: int,
                 parent_state_root: Cid,
                 parent_message_receipts: Cid,
                 messages: Cid,
                 bls_aggregate: Signature,
                 timestamp: int,
                 block_sig: Signature,
                 fork_signaling: int,
                 parent_base_fee: str):
        self.miner = miner
        self.ticket = ticket
        self.election_proof = election_proof
        self.beacon_entries = beacon_entries
        self.win_post_proof = win_post_proof
        self.parents = parents
        self.parent_weight = parent_weight
        self.height = height
        self.parent_state_root = parent_state_root
        self.parent_message_receipts = parent_message_receipts
        self.messages = messages
        self.bls_aggregate = bls_aggregate
        self.timestamp = timestamp
        self.block_sig = block_sig
        self.fork_signaling = fork_signaling
        self.parent_base_fee = parent_base_fee

def dict_to_blockheader(data: Dict) -> BlockHeader:
    """
    Converts a dictionary representation of a block header to a BlockHeader object.

    :param data: Dictionary containing block header details.
    :return: An instance of the BlockHeader class.
    """
    parents = [Cid(item["/"]) for item in data["Parents"]]
    parent_state_root = Cid(data["ParentStateRoot"]["/"])
    parent_message_receipts = Cid(data["ParentMessageReceipts"]["/"])
    messages = Cid(data["Messages"]["/"])
    
    bls_aggregate = Signature(data["BLSAggregate"]["Type"], data["BLSAggregate"]["Data"])
    block_sig = Signature(data["BlockSig"]["Type"], data["BlockSig"]["Data"])
    
    return BlockHeader(
        miner=data["Miner"],
        ticket=data["Ticket"],
        election_proof=data["ElectionProof"],
        beacon_entries=data["BeaconEntries"],
        win_post_proof=data["WinPoStProof"],
        parents=parents,
        parent_weight=data["ParentWeight"],
        height=data["Height"],
        parent_state_root=parent_state_root,
        parent_message_receipts=parent_message_receipts,
        messages=messages,
        bls_aggregate=bls_aggregate,
        timestamp=data["Timestamp"],
        block_sig=block_sig,
        fork_signaling=data["ForkSignaling"],
        parent_base_fee=data["ParentBaseFee"]
    )
