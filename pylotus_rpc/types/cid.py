from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Cid:
    """
    Represents a Content Identifier (CID)

    Attributes:
    - cid_id: A string representing the value of the CID.
    """
    id: str

    def __str__(self) -> str:
        return self.id


    def to_dict(self) -> Dict[str, str]:
        """
        Returns a dictionary representation of the CID for JSON serialization.
        """
        return {"/": self.id}


    @staticmethod
    def from_dict(dct) -> 'Cid':
        """
        Returns a Cid object from a dictionary representation.

        :param dct: A dictionary representing a Cid object.
        """
        return Cid(dct.get('/'))


    @staticmethod
    def format_cids_for_json(lst_cids: List[str]) -> List[Dict[str, str]]:
        """
        Formats a list of CID strings for JSON serialization.

        This method prepares CIDs for JSON serialization by converting each CID in the
        list into a dictionary with a single key-value pair, where the key is '/' and
        the value is the CID string. This format is commonly used in JSON representations
        of Filecoin messages and objects.

        Args:
            lst_cids: A list of CID strings to be formatted.

        Returns:
            A list of dictionaries, each representing a CID in the required JSON format.
        """
        return [{"/": cid} for cid in lst_cids]
