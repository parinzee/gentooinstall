"""
This module contains (higher level) functions to interact with the disk.
"""
from copy import deepcopy
from typing import List, cast

from .general import run_command


def dict_list_to_list(dict_list: List[dict]) -> List[list]:
    """
    Changes a list of a dict to a list of a list
    """
    main_list = []
    for dictionary in dict_list:
        temp = []
        for key in dictionary:
            temp.append(dictionary[key])
        main_list.append(temp)
    return main_list


def all_physical_disks() -> List[list]:
    """
    Returns all the physcial disk in the following form:
    [[name, size, label], [name,size,label]]
    """
    # We're typecasting to avoid mypy complaining
    out = cast(dict, run_command("lsblk --json -ldo name,size,label", True, True))
    blockdevices: list = out["blockdevices"]
    return dict_list_to_list(blockdevices)


def partitions_in_disk(path_to_disk: str) -> List[list]:
    """
    Returns all the partitions in the disk in the following form:
    [[name,size,fstype], [name,size,fstype]]
    """
    out = cast(
        dict,
        run_command(f"lsblk {path_to_disk} --json -no name,size,fstype", True, True),
    )
    partitions = out["blockdevices"][0]["children"]
    # Remove any children of the partitions
    for index, partition in enumerate(deepcopy(partitions)):
        if "children" in partition:
            partitions[index].pop("children")
    return dict_list_to_list(partitions)


def format_filesystem(path_to_part: str, fs_type: str) -> None:
    """
    Runs mkfs.fs_type to format a disk.
    """
    if fs_type == "swap":
        run_command(f"mkswap {path_to_part}")
    else:
        run_command(f"mkfs.{fs_type.lower()} {path_to_part}")
