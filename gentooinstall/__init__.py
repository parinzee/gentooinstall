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

# --config option
parser.add_argument(
    "--config",
    action="store",
    help="Optional JSON file or url that can be passed in to do an UNATTENDED install.",
)

# no-ntp option
parser.add_argument(
    "--no-ntp",
    action="store_true",
    help="Disables using NTP to sync the time. Use this if you have set the time manually.",
)

# no-optimal-mirror-api
parser.add_argument(
    "--no-optimal-mirror",
    action="store_true",
    help="Disables using 3rd party api to find optimal mirror.",
)

# If --config is specified, then we will overwrite values within the inital storage object

# Keep the args in our storage
arguments = parser.parse_args()
storage.args["no_ntp"] = arguments.no_ntp
storage.args["no_optimal_mirror"] = arguments.no_optimal_mirror


def run_as_module():
    """
    Running this program as a module, so this and __main__ will act as entry point.
    """

    # Before running the app check if we have root permissions.
    if os.geteuid() != 0:
        raise PermissionError("You need to be root to run this script")

    execute()
