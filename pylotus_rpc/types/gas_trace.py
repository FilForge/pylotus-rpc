from dataclasses import dataclass
from typing import List, Any, Dict, Union, Optional
from .loc import Loc

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
    TotalGas: int
    ComputeGas: int
    StorageGas: int
    TotalVirtualGas: int
    VirtualComputeGas: int
    VirtualStorageGas: int
    TimeTaken: int
    Extra: Any
    Callers: List[int]

    @staticmethod
    def from_json(data: Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]) -> 'GasTrace':
        """
        Deserialize a dictionary (from parsed JSON) into a GasTrace object.

        Args:
        - data: A dictionary representation of the GasTrace object.

        Returns:
        An instance of the GasTrace class.
        """
        # Treating Location as optional; if not present, it defaults to an empty list
        location_data = data.get("Location", [])
        locations = [Loc.from_json(loc) for loc in location_data]

        # Treating Callers as optional; if not present or not a list, it defaults to an empty list
        callers = data.get("Callers", [])
        if not isinstance(callers, list):
            callers = []

        return GasTrace(
            Name=data["Name"],
            Location=locations,
            TotalGas=data.get("tg", 0),
            ComputeGas=data.get("cg", 0),
            StorageGas=data.get("sg", 0),
            TotalVirtualGas=data.get("TotalVirtualGas", 0),
            VirtualComputeGas=data.get("VirtualComputeGas", 0),
            VirtualStorageGas=data.get("VirtualStorageGas", 0),
            TimeTaken=data.get("tt", 0),
            Extra=data.get("Extra", 0),
            Callers=callers
        )
