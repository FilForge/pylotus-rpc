from dataclasses import dataclass
from typing import List, Any, Dict, Union, Optional
from .loc import Loc

@dataclass
class GasTrace:
    """
    Represents detailed gas tracing information for a given call or operation.

    Attributes:
    - name: The name or identifier of the trace.
    - location: A list of locations (files, line numbers, functions) representing the trace's origin.
    - total_gas: Total gas used.
    - compute_gas: Gas used for computation.
    - storage_gas: Gas used for storage operations.
    - total_virtual_gas: Total virtual gas used.
    - virtual_compute_gas: Virtual gas used for computation.
    - virtual_storage_gas: Virtual gas used for storage operations.
    - time_taken: Time taken for the operations, typically in nanoseconds.
    - extra: Additional data or context associated with the trace.
    - callers: List of caller identifiers.
    """

    name: str
    location: List[Loc]
    total_gas: int
    compute_gas: int
    storage_gas: int
    total_virtual_gas: int
    virtual_compute_gas: int
    virtual_storage_gas: int
    time_taken: int
    extra: Any
    callers: List[int]

    @staticmethod
    def from_dict(data: Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]) -> 'GasTrace':
        """
        Deserialize a dictionary (from parsed JSON) into a GasTrace object.

        Args:
        - data: A dictionary representation of the GasTrace object.

        Returns:
        An instance of the GasTrace class.
        """
        # Treating Location as optional; if not present, it defaults to an empty list
        location_data = data.get("Location", [])
        locations = [Loc.from_dict(loc) for loc in location_data]

        # Treating Callers as optional; if not present or not a list, it defaults to an empty list
        callers = data.get("Callers", [])
        if not isinstance(callers, list):
            callers = []

        return GasTrace(
            name=data["Name"],
            location=locations,
            total_gas=data.get("tg", 0),
            compute_gas=data.get("cg", 0),
            storage_gas=data.get("sg", 0),
            total_virtual_gas=data.get("TotalVirtualGas", 0),
            virtual_compute_gas=data.get("VirtualComputeGas", 0),
            virtual_storage_gas=data.get("VirtualStorageGas", 0),
            time_taken=data.get("tt", 0),
            extra=data.get("Extra", 0),
            callers=callers
        )
