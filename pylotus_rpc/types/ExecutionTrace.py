from dataclasses import dataclass, field
from typing import List, Optional, Dict, Union
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

    @staticmethod
    def from_json(data: Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]) -> 'ExecutionTrace':
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
            gas_charges = [GasTrace.from_json(gas_charge) for gas_charge in gas_charges]

        subcalls = data.get("Subcalls")
        if subcalls is None:
            subcalls = []
        else:
            subcalls = [ExecutionTrace.from_json(subcall) for subcall in subcalls]

        return ExecutionTrace(
            Msg=Message.from_json(data["Msg"]),
            MsgRct=MessageReceipt.from_json(data["MsgRct"]),
            Duration=int(data.get("Duration", 0)),
            Error=data.get("Error", None),
            GasCharges=gas_charges,
            Subcalls=subcalls
        )


# Example usage would look like:
# execution_trace = ExecutionTrace.from_json(json_data)
