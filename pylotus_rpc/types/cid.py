from dataclasses import dataclass

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


    @staticmethod
    def from_dict(dct):
        """
        Returns a Cid object from a dictionary representation.

        :param dct: A dictionary representing a Cid object.
        """
        return Cid(dct.get('/'))


    @staticmethod
    def dct_cids(lst_cids):
        """
        Returns a dictionary representation of the CIDs for JSON serialization.
        """
        return [{"/": cid} for cid in lst_cids]