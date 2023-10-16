class Address:
    # Address is a class that represents an address in the Filecoin network.
    def __init__(self, address_value: str):
        """
        Initializes a new Address object.

        :param address_value: A string representing the value of the address.
        """
        self.address_value = address_value

    def is_id_address(self):
        """
        Checks if the address is an ID-based address.

        :return: True if it's an ID-based address, False otherwise.
        """
        # Implement the logic to check if the address is an ID-based address.
        # For example, you can check if it starts with 'f' for mainnet addresses.
        return self.address_value.startswith('f')

    def is_actor_address(self):
        """
        Checks if the address is an actor-based address.

        :return: True if it's an actor-based address, False otherwise.
        """
        # Implement the logic to check if the address is an actor-based address.
        # You may need to define specific prefixes for actor addresses.
        # For example, 't' for testnet actor addresses.
        return self.address_value.startswith('t')
