# pylint: disable=missing-module-docstring
import argparse
import os

from .lib.storage import storage
from .script import *

__version__ = "0.1.0"

# Initialize argument parser
parser = argparse.ArgumentParser(
    prog="gentooinstall",
    description="The program aimed to help both beginners and experienced users install gentoo.",
)

# no-info option
parser.add_argument(
    "--no-info",
    action="store_true",
    help="Disables explanations for steps from the Gentoo Handbook. NOT RECCOMENDED FOR BEGINNERS",
)

# Keep the args in our storage
storage["args"] = parser.parse_args()


def run_as_module():
    """
    Running this program as a module, so this and __main__ will act as entry point.
    """

    # Before running the app check if we have root permissions.
    if os.geteuid() != 0:
        raise PermissionError("You need to be root to run this script")

    script = Script()
    script.execute()
