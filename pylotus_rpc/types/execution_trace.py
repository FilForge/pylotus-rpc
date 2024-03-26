from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union
from .message import Message
from .message_receipt import MessageReceipt
from .gas_trace import GasTrace

@dataclass
class ExecutionTrace:
    """
    Represents the execution trace for a message in Filecoin/Lotus.
    
    Attributes:
    - msg: The original message that was executed.
    - message_receipt: The receipt of the message execution.
    - duration: Duration of the execution.
    - error: Any error that occurred during execution, if any.
    - gas_charges: A list of gas traces for the execution.
    - sub_calls: Any subcalls made during the execution.
    """
    
    msg: Message
    msg_receipt: MessageReceipt
    duration: int
    error: Optional[str] = None
    gas_charges: List[GasTrace] = field(default_factory=list)
    sub_calls: List["ExecutionTrace"] = field(default_factory=list)

    @staticmethod
    def from_dict(data: Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]) -> 'ExecutionTrace':
        """
        Deserialize a dictionary (from parsed JSON) into an ExecutionTrace object.

        Args:
        - data: A dictionary representation of the ExecutionTrace object.

        Returns:
        An instance of the ExecutionTrace class.
        """
        
        gas_charges = data.get("GasCharges")
        if gas_charges is None:
            gas_charges = []
        else:
            gas_charges = [GasTrace.from_dict(gas_charge) for gas_charge in gas_charges]

        sub_calls = data.get("Subcalls")
        if sub_calls is None:
            sub_calls = []
        else:
            sub_calls = [ExecutionTrace.from_dict(subcall) for subcall in sub_calls]

        return ExecutionTrace(
            msg=Message.from_dict(data["Msg"]),
            msg_receipt=MessageReceipt.from_dict(data["MsgRct"]),
            duration=int(data.get("Duration", 0)),
            error=data.get("Error", None),
            gas_charges=gas_charges,
            sub_calls=sub_calls
        )