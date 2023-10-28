from dataclasses import dataclass
from typing import Dict, Any, Optional
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

    # Attributes without default values
    MsgCid: Cid  # The CID (Content Identifier) of the message
    Msg: Message  # The actual message associated with this invocation
    MsgRct: MessageReceipt  # The receipt of the message providing details of the message's outcome
    GasCost: MessageGasCost  # The gas cost details associated with this invocation
    ExecutionTrace: ExecutionTrace  # Trace that provides insight into the internal steps taken during the invocation
    Duration: int  # The total duration (likely in milliseconds) of the invocation.
    
    # Attributes with default values
    Error: Optional[str] = None  # Any error encountered during the invocation. None if no errors were encountered.

    @staticmethod
    def from_json(data: Dict[str, Any]) -> 'InvocationResult':
        # Extracting the relevant information from the JSON data
        result_data = data["result"]

        # Initialize each component from the dictionary
        msg_cid = Cid(result_data["MsgCid"])
        msg = Message.from_json(result_data["Msg"])
        msg_rct = MessageReceipt.from_json(result_data["MsgRct"])
        gas_cost = MessageGasCost.from_json(result_data["GasCost"])
        execution_trace = ExecutionTrace.from_json(result_data["ExecutionTrace"])
        duration = result_data["Duration"]
        error = result_data.get("Error", None)  # It's optional so we provide a default value

        # Create and return the InvocationResult instance
        return InvocationResult(
            MsgCid=msg_cid,
            Msg=msg,
            MsgRct=msg_rct,
            GasCost=gas_cost,
            ExecutionTrace=execution_trace,
            Duration=duration,
            Error=error
        )