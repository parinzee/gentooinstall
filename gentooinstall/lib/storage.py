"""
Simple module for storing arguments that can be accessed throughout the program
"""
from argparse import Namespace
from typing import TypedDict


# Define schema for the Storage dict
class Storage(TypedDict):
    """
    Schema for the storage dictionary
    """

    args: Namespace
    mountpoint: str
    drives: str


storage: Storage = {
    "args": Namespace(),
    "mountpoint": "/mnt/gentoo",
    "drives": "",
}
