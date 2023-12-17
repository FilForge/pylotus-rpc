from dataclasses import dataclass

@dataclass
class Address:
    """
    Represents an address in the Filecoin network.

    Attributes:
    - address_value: A string representing the value of the address.
    """
    address_value: str