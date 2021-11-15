# pylint: disable=missing-module-docstring
import argparse
import os

from rich.traceback import install

from .lib.installer import *
from .lib.storage import storage

__version__ = "0.1.0"

# Install rich as traceback handler
install()

# Initialize argument parser
parser = argparse.ArgumentParser(
    prog="gentooinstall",
    description="The program aimed to help both beginners and experienced users install gentoo.",
)

# no-info option
# Turns off informative things
parser.add_argument(
    "--no-info",
    action="store_true",
    help="Disables explanations for steps from the Gentoo Handbook. NOT RECCOMENDED FOR BEGINNERS",
)

# no-info option
# Script will not use ntp to sync the time
parser.add_argument(
    "--no-ntp",
    action="store_true",
    help="Disables using NTP to sync the time. Use this if you have set the time manually.",
)


# Keep the args in our storage
arguments = parser.parse_args()
storage["args"].no_info = arguments.no_info
storage["args"].no_ntp = arguments.no_ntp


def run_as_module():
    """
    Running this program as a module, so this and __main__ will act as entry point.
    """

    # Before running the app check if we have root permissions.
    if os.geteuid() != 0:
        raise PermissionError("You need to be root to run this script")

    execute()
