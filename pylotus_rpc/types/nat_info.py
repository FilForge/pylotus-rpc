from dataclasses import dataclass
from typing import List

@dataclass
class NatInfo:
    """
    Represents the NAT (Network Address Translation) status information for a Lotus node.
    
    Attributes:
        reachability (int): The reachability status of the node.
            1 = Public
            2 = Private
            3 = Unknown
        public_addrs (List[str]): List of public addresses associated with the node.
    """
    reachability: int
    public_addrs: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'NatInfo':
        """
        Creates a NatInfo instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing NAT status information.
            
        Returns:
            NatInfo: A new instance of NatInfo.
        """
        return cls(
            reachability=data['Reachability'],
            public_addrs=data['PublicAddrs']
        ) 