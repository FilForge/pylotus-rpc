from dataclasses import dataclass, field
from .tip_set import Tipset

@dataclass
class HeadChange:
    """
    Represents a HeadChange in the Filecoin blockchain.

    A HeadChange is a change in the head of the blockchain.

    Attributes:
    - type: A string representing the type of the HeadChange.
    - val: A Tipset object representing the new head of the blockchain.
    """
    type: str
    val: Tipset = None

    @staticmethod
    def from_dict(data: dict) -> 'HeadChange':
        """
        Converts a dictionary representation of a HeadChange to a HeadChange object.

        :param data: Dictionary containing HeadChange details.
        :return: An instance of the HeadChange class.
        """
        return HeadChange(data["Type"], Tipset.from_dict(data["Val"]))
    

