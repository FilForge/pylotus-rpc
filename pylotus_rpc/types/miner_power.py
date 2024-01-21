from dataclasses import dataclass, asdict
import json

@dataclass
class Power:
    raw_byte_power: int
    quality_adj_power: int

@dataclass
class MinerPower:
    miner_power: Power
    total_power: Power
    has_min_power: bool

    @staticmethod
    def from_dict(dct):
        return MinerPower(
            miner_power=Power(
                raw_byte_power=int(dct["MinerPower"]["RawBytePower"]),
                quality_adj_power=int(dct["MinerPower"]["QualityAdjPower"])
            ),
            total_power=Power(
                raw_byte_power=int(dct["TotalPower"]["RawBytePower"]),
                quality_adj_power=int(dct["TotalPower"]["QualityAdjPower"])
            ),
            has_min_power=dct["HasMinPower"]
        )

    def __str__(self):
        return json.dumps(asdict(self), indent=4)