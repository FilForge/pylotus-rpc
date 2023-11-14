from dataclasses import dataclass
from typing import List
from .Cid import Cid
from .InvocationResult import InvocationResult

@dataclass
class ComputeStateOutput:
    """
    Represents the output of a compute state operation.

    Attributes:
    - Root: The CID of the root of the state tree.
    - Trace: A list of `InvocationResult` objects representing the invocation results.
    """

    Root: Cid
    Trace: List[InvocationResult]

