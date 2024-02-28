from typing import List

def add_rle_run(lst_sectors: List[int], sector_offset: int, sector_run_size: int):
    """
    Adds a run of sector numbers to the list of sectors based on the offset and size of the run.

    Args:
        lst_sectors (List[int]): The list of sector numbers to which the run will be added.
        sector_offset (int): The starting sector number of the run.
        sector_run_size (int): The number of consecutive sectors in the run.

    This function iterates from 0 up to `sector_run_size` and appends each sector number,
    starting from `sector_offset`, to `lst_sectors`.
    """
    for i in range(sector_run_size):
        lst_sectors.append(sector_offset + i)


# Encoded as an array of run-lengths, always starting with zeroes (absent values)
# E.g.: The set {0, 1, 2, 8, 9} is the bitfield 1110000011, and would be marshalled as [0, 3, 5, 2]
def decode_sectors(rle_enc: List[int]) -> List[int]:
    """
    Decodes a list of integers representing run-length encoded sector numbers into a list of sector numbers.

    Args:
        rle_enc (List[int]): The run-length encoded list of sector numbers. The list alternates between
                             starting offsets and lengths of runs, beginning with a starting offset.

    Returns:
        List[int]: A list of decoded sector numbers.

    This function decodes the run-length encoded data specified by `rle_enc` into a flat list of sector numbers.
    The decoding starts by initializing an empty list for the sectors. It then iterates over the encoded list,
    adding runs of 'on' sectors to the list of sectors based on the run size. It alternates between 'on' and 'off'
    states to accurately decode the RLE data into sector numbers.

    Note:
        The first value in `rle_enc` is treated as the initial offset for 'on' sectors.
        The function assumes the first run always represents 'on' sectors.
    """
    lst_sectors = []
    sectors_on = True
    sector_offset = rle_enc[0]

    for i in range(1, len(rle_enc)):
        sector_run_size = rle_enc[i]
        if sectors_on:
            add_rle_run(lst_sectors, sector_offset, sector_run_size)
        sector_offset += sector_run_size
        sectors_on = not sectors_on

    return lst_sectors
