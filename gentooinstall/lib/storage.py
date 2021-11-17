"""
Simple module for storing options that can be accessed throughout the program
"""
import json
import os
from typing import Optional, TypedDict
from urllib.parse import urlparse

import requests


class Args(TypedDict):
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


class Storage:
    """
    Storage class that will be responsible for storing all the data accessed in the program.
    They can be exported to a json file for reuse.
    They can be imported from a json file for reuse.
    """

    def __init__(self) -> None:
        """
        Initiates the Storage class
        """
        self.args: Args = {"no_info": False, "no_ntp": False}
        self.drives: Drives = {"root": "", "boot": "", "swap": None}
        self.mountpoint: str = "/mnt/gentoo"

        # Internal value to see if a config has been provided or not.
        self.config = False

    def export_config(self, path: str = "/gentooinstall.json") -> None:
        """
        Export the current Storage object into a JSON file located within the mountpoint
        """
        config = {
            "args": self.args,
            "drives": self.drives,
            "mountpoint": self.mountpoint,
        }
        # Make sure that the path specified startes with a /
        if not path.startswith("/"):
            path = "/" + path

        with open(f"{self.mountpoint}{path}", "w", encoding="UTF-8") as file:
            json.dump(config, file, sort_keys=True, indent=2)

    def import_config(self, import_path: str) -> None:
        """
        Import the storage options from a JSON file
        and overwrites the initial options.
        """
        # See if import_path is local path or a url.
        if urlparse(import_path).scheme:
            resp = requests.get(import_path)
            config = json.loads(resp.text)
        else:
            # Get the absolute path and decode the json
            full_import_path = os.path.abspath(import_path)
            with open(full_import_path, "r", encoding="UTF-8") as file:
                config = json.load(file)

        # Overwrite initial values
        self.args = config["args"]
        self.drives = config["drives"]
        self.mountpoint = config["mountpoint"]

        # Set internal variable that specifies we have a config
        self.config = True


storage = Storage()
