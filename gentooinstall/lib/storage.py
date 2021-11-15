"""
Simple module for storing options that can be accessed throughout the program
"""
from argparse import Namespace
from typing import Optional, TypedDict


class Args(Namespace):
    # pylint: disable=too-few-public-methods
    """
    Schema for the args dictionary inside Storage
    """

    no_info: bool
    no_ntp: bool


class Drives(TypedDict):
    """
    Schema for the drives dictionary in Storage
    """

    boot: str
    root: str
    # If swap is enable this will be a path or text that says swapfile
    swap: Optional[str]


class Storage(TypedDict):
    """
    Schema for the storage dictionary
    """

    args: Args
    mountpoint: str
    drives: Drives
    efi: bool


storage: Storage = {
    "args": Args(no_info=False, no_ntp=False),
    "mountpoint": "/mnt/gentoo",
    "drives": {"root": "", "boot": "", "swap": None},
    "efi": False,
}
