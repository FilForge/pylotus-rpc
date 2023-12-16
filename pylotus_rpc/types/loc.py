from dataclasses import dataclass
from typing import Dict, Union

@dataclass
class Loc:
    """
    Represents a location in the codebase, useful for tracing and debugging.

    Attributes:
    - file: The name of the file where the trace point is located.
    - line: The line number of the trace point.
    - function: The function in which the trace point is found.
    """
    
    file: str
    line: int
    function: str

    @staticmethod
    def from_json(data: Dict[str, Union[str, int]]) -> 'Loc':
        """
        Deserialize a dictionary (from parsed JSON) into a Loc object.

        Args:
        - data: A dictionary representation of the Loc object.

        Returns:
        An instance of the Loc class.
        """
        return Loc(
            file=data["File"],
            line=data["Line"],
            function=data["Function"]
        )
