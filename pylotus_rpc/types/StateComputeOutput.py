from dataclasses import dataclass
from typing import List
from .Cid import Cid
from .InvocationResult import InvocationResult

@dataclass
class StateComputeOutput:
    """
    Represents the output of a compute state operation.

    Attributes:
    - root: The CID of the root of the state tree.
    - trace: A list of `InvocationResult` objects representing the invocation results.
    """

    root: Cid
    trace: List[InvocationResult]

    @staticmethod
    def from_dict(data: dict) -> 'StateComputeOutput':
        """
        Converts the given JSON dict into a ComputeStateOutput object.

        Parameters:
        - data: The JSON dict to convert.

        Returns:
        A ComputeStateOutput object.
        """
        root = Cid(data["Root"]["/"])
        trace = [InvocationResult.from_dict(invocation_result) for invocation_result in data["Trace"]]

        return StateComputeOutput(root=root,trace=trace)

