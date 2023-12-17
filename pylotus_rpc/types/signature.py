from dataclasses import dataclass

@dataclass
class Signature:
    """
    Represents a cryptographic signature.

    Attributes:
    - type: An integer representing the signature type.
    - data: A string containing the signature data.
    """
    type: int
    data: str
