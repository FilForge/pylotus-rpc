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

    @staticmethod
    def from_dict(data: dict) -> 'Signature':
        """
        Deserialize a dictionary (from parsed JSON) into a Signature object.

        Args:
        - data: A dictionary representation of the Signature object.

        Returns:
        An instance of the Signature class.
        """
        return Signature(
            type=data["Type"],
            data=data["Data"]
        )