from dataclasses import dataclass
from typing import List

@dataclass
class Deadline:
    """
    Represents a deadline in the context of Filecoin's mining and proving process.

    Attributes:
        post_submissions (List[int]): A list of integers representing the partition indexes that have submitted proofs.
        disputable_proof_count (int): The count of proofs that are currently eligible for dispute.

    Description:
        In Filecoin, miners are required to submit proofs for the sectors they are mining. These proofs are 
        submitted within specific time frames known as deadlines. This class represents information about these 
        deadlines, including which partitions have submitted their proofs and how many of these proofs can be disputed.
    """

    post_submissions: List[int]
    disputable_proof_count: int

    @staticmethod
    def from_dict(dct: dict) -> 'Deadline':
        """
        Creates a Deadline instance from a dictionary.

        Args:
            dct (dict): A dictionary with keys 'PostSubmissions' and 'DisputableProofCount'.

        Returns:
            Deadline: An instance of Deadline class initialized with values from the dictionary.

        Example:
            dct = {
                "PostSubmissions": [0],
                "DisputableProofCount": 1
            }
            deadline = Deadline.from_dict(dct)
        """
        return Deadline(
            post_submissions=dct.get("PostSubmissions", []),
            disputable_proof_count=dct.get("DisputableProofCount", 0)
        )
