from dataclasses import dataclass
from typing import Dict, Union

@dataclass
class MessageGasCost:
    """
    Represents the gas cost for a Filecoin message.

    Attributes:
    - Message: The CID of the message.
    - GasUsed: Amount of gas used.
    - BaseFeeBurn: Base fee burned.
    - OverEstimationBurn: Over-estimation burn.
    - MinerPenalty: Penalty to the miner.
    - MinerTip: Tip to the miner.
    - Refund: Amount refunded.
    - TotalCost: Total cost.
    """
    
    Message: str
    GasUsed: int
    BaseFeeBurn: int
    OverEstimationBurn: int
    MinerPenalty: int
    MinerTip: int
    Refund: int
    TotalCost: int

    @staticmethod
    def from_json(data: Dict[str, Union[str, int]]) -> 'MessageGasCost':
        """
        Deserialize a dictionary (from parsed JSON) into a MessageGasCost object.

        Args:
        - data: A dictionary representation of the MessageGasCost object.

        Returns:
        An instance of the MessageGasCost class.
        """
        return MessageGasCost(
            Message=data["Message"] if data["Message"] else "",
            GasUsed=int(data["GasUsed"]),
            BaseFeeBurn=int(data["BaseFeeBurn"]),
            OverEstimationBurn=int(data["OverEstimationBurn"]),
            MinerPenalty=int(data["MinerPenalty"]),
            MinerTip=int(data["MinerTip"]),
            Refund=int(data["Refund"]),
            TotalCost=int(data["TotalCost"])
        )


