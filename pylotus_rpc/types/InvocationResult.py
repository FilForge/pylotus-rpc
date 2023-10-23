from dataclasses import dataclass
from typing import Optional
from .Cid import Cid
from .Message import Message
from .MessageReceipt import MessageReceipt
from .MessageGasCost import MessageGasCost
from .ExecutionTrace import ExecutionTrace

@dataclass
class InvocationResult:
    """
    Represents the result of an invocation in Filecoin/Lotus.
    
    This class captures the essential details of an invocation event including
    the message CID, the actual message, the message receipt which provides details
    on the outcome of the message, the gas cost associated with the invocation,
    an execution trace that gives insight into the internal steps taken during the
    invocation, any errors encountered, and the total duration of the invocation.
    """

    MsgCid: Cid  # The CID (Content Identifier) of the message
    Msg: Message  # The actual message associated with this invocation
    MsgRct: MessageReceipt  # The receipt of the message providing details of the message's outcome
    GasCost: MessageGasCost  # The gas cost details associated with this invocation
    ExecutionTrace: ExecutionTrace  # Trace that provides insight into the internal steps taken during the invocation
    Error: Optional[str] = None  # Any error encountered during the invocation. None if no errors were encountered.
    Duration: int  # The total duration (likely in milliseconds) of the invocation.
