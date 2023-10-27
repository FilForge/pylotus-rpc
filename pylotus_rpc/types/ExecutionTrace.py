from dataclasses import dataclass, field
from typing import List, Optional
from .Message import Message
from .MessageReceipt import MessageReceipt
from .GasTrace import GasTrace

@dataclass
class ExecutionTrace:
    """
    Represents the execution trace for a message in Filecoin/Lotus.
    
    Attributes:
    - Msg: The original message that was executed.
    - MsgRct: The receipt of the message execution.
    - Duration: Duration of the execution.
    - Error: Any error that occurred during execution, if any.
    - GasCharges: A list of gas traces for the execution.
    - Subcalls: Any subcalls made during the execution.
    """
    
    Msg: Message
    MsgRct: MessageReceipt
    Duration: int
    Error: Optional[str] = None
    GasCharges: List[GasTrace] = field(default_factory=list)
    Subcalls: List["ExecutionTrace"] = field(default_factory=list)
