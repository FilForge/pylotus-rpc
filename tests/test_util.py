import pytest

from pylotus_rpc.util.sector_util import decode_sectors

def test_decode_rle_sectors():
    rle_encoded_sectors = [0, 3, 5, 2]
    lst_sectors = decode_sectors(rle_encoded_sectors)
    assert lst_sectors == [0, 1, 2, 8, 9]
