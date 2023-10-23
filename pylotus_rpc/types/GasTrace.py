from dataclasses import dataclass
from decimal import Decimal
from typing import List, Any
from Loc import Loc

@dataclass
class GasTrace:
    """
    Represents detailed gas tracing information for a given call or operation.

    Attributes:
    - Name: The name or identifier of the trace.
    - Location: A list of locations (files, line numbers, functions) representing the trace's origin.
    - TotalGas: Total gas used.
    - ComputeGas: Gas used for computation.
    - StorageGas: Gas used for storage operations.
    - TotalVirtualGas: Total virtual gas used.
    - VirtualComputeGas: Virtual gas used for computation.
    - VirtualStorageGas: Virtual gas used for storage operations.
    - TimeTaken: Time taken for the operations, typically in nanoseconds.
    - Extra: Additional data or context associated with the trace.
    - Callers: List of caller identifiers.
    """

    Name: str
    Location: List[Loc]
    TotalGas: Decimal
    ComputeGas: Decimal
    StorageGas: Decimal
    TotalVirtualGas: Decimal
    VirtualComputeGas: Decimal
    VirtualStorageGas: Decimal
    TimeTaken: Decimal
    Extra: Any
    Callers: List[int]
