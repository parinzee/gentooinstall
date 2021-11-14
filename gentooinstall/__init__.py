# pylint: disable=missing-module-docstring
import argparse

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
