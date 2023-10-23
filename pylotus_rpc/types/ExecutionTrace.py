from dataclasses import dataclass, field
from typing import List, Optional
from .Message import Message
from .MessageReceipt import MessageReceipt
from .GasTrace import GasTrace

@dataclass
class ExecutionTrace:
    """
    Represents the execution trace for a message in Filecoin/Lotus.
    """
    Msg: Message
    MsgRct: MessageReceipt
    Error: Optional[str] = None
    Duration: int
    GasCharges: List[GasTrace] = field(default_factory=list)
    Subcalls: List["ExecutionTrace"] = field(default_factory=list)
