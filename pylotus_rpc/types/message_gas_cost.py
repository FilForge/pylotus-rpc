from dataclasses import dataclass
from typing import Dict, Union

@dataclass
class MessageGasCost:
    """
    Represents the gas cost for a Filecoin message.

    Attributes:
    - message: The CID of the message.
    - gas_used: Amount of gas used.
    - base_fee_burn: Base fee burned.
    - over_estimation_burn: Over-estimation burn.
    - miner_penalty: Penalty to the miner.
    - miner_tip: Tip to the miner.
    - refund: Amount refunded.
    - total_cost: Total cost.
    """
    
    message: str
    gas_used: int
    base_fee_burn: int
    over_estimation_burn: int
    miner_penalty: int
    miner_tip: int
    refund: int
    total_cost: int

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
            message=data["Message"] if data["Message"] else "",
            gas_used=int(data["GasUsed"]),
            base_fee_burn=int(data["BaseFeeBurn"]),
            over_estimation_burn=int(data["OverEstimationBurn"]),
            miner_penalty=int(data["MinerPenalty"]),
            miner_tip=int(data["MinerTip"]),
            refund=int(data["Refund"]),
            total_cost=int(data["TotalCost"])
        )


