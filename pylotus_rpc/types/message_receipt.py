from dataclasses import dataclass
from typing import Any, Dict, Union

@dataclass
class MessageReceipt:
    """
    Represents a receipt for a Filecoin message.
    
    Attributes:
    - exit_code: The exit code after the message was processed.
    - return_value: Any return value from the message execution.
    - gas_used: The amount of gas used to process the message.
    """
    
    exit_code: int
    return_value: Any
    gas_used: int

    # TODO - rename this to from_dict
    @staticmethod
    def from_json(data: Dict[str, Union[int, Any]]) -> 'MessageReceipt':
        """
        Deserialize a dictionary (from parsed JSON) into a MessageReceipt object.

        Args:
        - data: A dictionary representation of the MessageReceipt object.

        Returns:
        An instance of the MessageReceipt class.
        """
        return MessageReceipt(
            exit_code=data["ExitCode"],
            return_value=data["Return"],
            gas_used=data.get("GasUsed",0)
        )