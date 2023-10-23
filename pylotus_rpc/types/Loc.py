from dataclasses import dataclass

@dataclass
class Loc:
    """
    Represents a location in the codebase, useful for tracing and debugging.

    Attributes:
    - File: The name of the file where the trace point is located.
    - Line: The line number of the trace point.
    - Function: The function in which the trace point is found.
    """
    
    File: str
    Line: int
    Function: str
