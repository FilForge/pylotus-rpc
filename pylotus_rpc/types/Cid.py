from typing import List, Dict, Union

class Cid:
    # Assuming CIDs always have a single key "/", but this can be extended if needed
    def __init__(self, cid_value: str):
        self.cid_value = cid_value