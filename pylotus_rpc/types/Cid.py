class Cid:
    """
    Represents a Content Identifier (CID)

    Attributes:
    - cid_id: A string representing the value of the CID.
    """

    def __init__(self, cid_id: str):
        """
        Initializes a new Cid object.

        :param cid_id: A string representing the value of the CID.
        """
        self.id = cid_id


    def __str__(self) -> str:
        return self.id


    @staticmethod
    def dct_cids(lst_cids):
        """
        Returns a dictionary representation of the CIDs for JSON serialization.
        """
        return [{"/": cid} for cid in lst_cids]