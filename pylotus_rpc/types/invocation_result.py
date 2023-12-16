from dataclasses import dataclass
from typing import Dict, Any, Optional
from .cid import Cid
from .message import Message
from .message_receipt import MessageReceipt
from .message_gas_cost import MessageGasCost
from .execution_trace import ExecutionTrace

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
    msg: Message  # The actual message associated with this invocation
    msg_cid: Optional[Cid] = None  # The CID (Content Identifier) of the message
    msg_receipt: Optional[MessageReceipt] = None  # The receipt of the message providing details of the message's outcome
    gas_cost: Optional[MessageGasCost] = None  # The gas cost details associated with this invocation
    execution_trace: Optional[ExecutionTrace] = None  # Trace that provides insight into the internal steps taken during the invocation
    duration: Optional[int] = None  # The total duration (likely in milliseconds) of the invocation.
    error: Optional[str] = None  # Any error encountered during the invocation. None if no errors were encountered.

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'InvocationResult':
        # api error handling
        if 'error' in data:
            code = data["error"]["code"]
            msg = str(code) + ": " + data["error"]["message"]

            return InvocationResult(
                msg=msg,
                duration=0,
                error=msg
            )
        
        # Extracting the relevant information from the JSON data
        if "result" in data:
            result_data = data["result"]
        else:
            result_data = data

        msg_cid = Cid(result_data["MsgCid"])
        msg = Message.from_json(result_data["Msg"])
        msg_rct = MessageReceipt.from_json(result_data["MsgRct"])
        gas_cost = MessageGasCost.from_json(result_data["GasCost"])
        execution_trace = ExecutionTrace.from_json(result_data["ExecutionTrace"])
        duration = result_data["Duration"]
        error = result_data.get("Error", None)  # It's optional so we provide a default value

        # Create and return the InvocationResult instance
        return InvocationResult(
            msg_cid=msg_cid,
            msg=msg,
            msg_receipt=msg_rct,
            gas_cost=gas_cost,
            execution_trace=execution_trace,
            duration=duration,
            error=error
        )