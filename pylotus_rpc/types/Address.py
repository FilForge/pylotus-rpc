class Address:
    """
    Represents an address in the Filecoin network.
    """

    def __init__(self, address: str):
        """
        Initializes a new Address object.

        :param address: A string representing the value of the address.
        """
        self.address_value = address
