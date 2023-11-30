from dataclasses import dataclass
from typing import Any

@dataclass
class MessageReceipt:
    """
    Represents a receipt for a Filecoin message.
    
    Attributes:
    - ExitCode: The exit code after the message was processed.
    - Return: Any return value from the message execution.
    - GasUsed: The amount of gas used to process the message.
    """
    
    ExitCode: int
    Return: Any
    GasUsed: int


from dataclasses import dataclass
from typing import Any, Dict, Union

@dataclass
class MessageReceipt:
    """
    Represents a receipt for a Filecoin message.
    
    Attributes:
    - ExitCode: The exit code after the message was processed.
    - Return: Any return value from the message execution.
    - GasUsed: The amount of gas used to process the message.
    """
    
    ExitCode: int
    Return: Any
    GasUsed: int

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
            ExitCode=data["ExitCode"],
            Return=data["Return"],
            GasUsed=data.get("GasUsed",0)
        )