import json
from dataclasses import dataclass, asdict

@dataclass
class DeadlineInfo:
    current_epoch: int
    period_start: int
    index: int
    open: int
    close: int
    challenge: int
    fault_cutoff: int
    wpost_period_deadlines: int
    wpost_proving_period: int
    wpost_challenge_window: int
    wpost_challenge_lookback: int
    fault_declaration_cutoff: int

    @staticmethod
    def from_dict(dct):
        return DeadlineInfo(
            current_epoch=dct.get("CurrentEpoch"),
            period_start=dct.get("PeriodStart"),
            index=dct.get("Index"),
            open=dct.get("Open"),
            close=dct.get("Close"),
            challenge=dct.get("Challenge"),
            fault_cutoff=dct.get("FaultCutoff"),
            wpost_period_deadlines=dct.get("WPoStPeriodDeadlines"),
            wpost_proving_period=dct.get("WPoStProvingPeriod"),
            wpost_challenge_window=dct.get("WPoStChallengeWindow"),
            wpost_challenge_lookback=dct.get("WPoStChallengeLookback"),
            fault_declaration_cutoff=dct.get("FaultDeclarationCutoff")
        )

    def __str__(self):
        return json.dumps(asdict(self), indent=4)
