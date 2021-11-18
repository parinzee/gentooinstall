"""
This module contains functions to do things with disks.
"""
from typing import List, cast

from .general import run_command


def all_physical_disks() -> List[list]:
    """
    Returns all the physcial disk in the following form
    [[name, size, label], [name,size,label]]
    """
    out = cast(dict, run_command("lsblk --json -ldo name,size,label", True, True))
    blockdevices: list = out["blockdevices"]
    disks = []
    # We need to change the dicts into lists
    for dictionary in blockdevices:
        temp = []
        for key in dictionary:
            temp.append(dictionary[key])
        disks.append(temp)
    return disks
