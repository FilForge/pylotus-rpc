class Signature:
    """
    Represents a cryptographic signature.

    Attributes:
    - type: An integer representing the signature type.
    - data: A string containing the signature data.
    """

    def __init__(self, type_: int, data: str):
        """
        Initializes a new Signature object.

        :param type_: An integer representing the signature type.
        :param data: A string containing the signature data.
        """
        self.type = type_
        self.data = data
