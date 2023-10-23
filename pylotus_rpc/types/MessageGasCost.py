from dataclasses import dataclass
from decimal import Decimal

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
    GasUsed: Decimal
    BaseFeeBurn: Decimal
    OverEstimationBurn: Decimal
    MinerPenalty: Decimal
    MinerTip: Decimal
    Refund: Decimal
    TotalCost: Decimal
