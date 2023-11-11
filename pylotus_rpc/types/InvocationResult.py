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

    # Attributes with default values
    Msg: Message  # The actual message associated with this invocation
    MsgCid: Optional[Cid] = None  # The CID (Content Identifier) of the message
    MsgRct: Optional[MessageReceipt] = None  # The receipt of the message providing details of the message's outcome
    GasCost: Optional[MessageGasCost] = None  # The gas cost details associated with this invocation
    ExecutionTrace: Optional[ExecutionTrace] = None  # Trace that provides insight into the internal steps taken during the invocation
    Duration: Optional[int] = None  # The total duration (likely in milliseconds) of the invocation.
    Error: Optional[str] = None  # Any error encountered during the invocation. None if no errors were encountered.

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'InvocationResult':
        # api error handling
        if 'error' in data:
            code = data["error"]["code"]
            msg = str(code) + ": " + data["error"]["message"]

            return InvocationResult(
                Msg=msg,
                Duration=0,
                Error=msg
            )
        
        # Extracting the relevant information from the JSON data
        result_data = data["result"]
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