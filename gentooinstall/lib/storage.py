"""
Simple module for storing arguments that can be accessed throughout the program
"""
from argparse import Namespace
from typing import Optional, TypedDict


class Drives(TypedDict):
    """
    Schema for the drives dictionary in Storage
    """

    boot: str
    root: str
    # If swap is enable this will be a path or text that says swapfile
    swap: Optional[str]


# Define schema for the Storage dict
class Storage(TypedDict):
    """
    Schema for the storage dictionary
    """

    args: Namespace
    mountpoint: str
    drives: Drives
    efi: bool


storage: Storage = {
    "args": Namespace(),
    "mountpoint": "/mnt/gentoo",
    "drives": {"root": "", "boot": "", "swap": None},
    "efi": False,
}
